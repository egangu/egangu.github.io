#!/usr/bin/env python3
"""Store a durable Google Analytics page-view total for the Jekyll site.

The site reads the resulting JSON at build time, so a temporary Google
Analytics outage cannot turn the visible counter into an error placeholder.
This program only replaces the snapshot after receiving and validating a new
report from the Google Analytics Data API.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Callable, Mapping
from urllib import error, parse, request
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ANALYTICS_SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
TOKEN_URL = "https://oauth2.googleapis.com/token"
DATA_API_BASE_URL = "https://analyticsdata.googleapis.com/v1beta"
DEFAULT_START_DATE = date(2026, 10, 3)
SITE_HOSTNAME = "egangu.github.io"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "_data" / "visits.json"


class VisitsError(RuntimeError):
    """A failure that must leave the previous visits snapshot intact."""


class ConfigurationError(VisitsError):
    """The workflow does not have the information needed to query GA4."""


class AuthenticationError(VisitsError):
    """Google OAuth authentication could not be completed."""


class AnalyticsResponseError(VisitsError):
    """The Analytics Data API returned an unusable report."""


class SnapshotSafetyError(VisitsError):
    """A surprising zero response would discard a known GA4 count."""


def base64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def load_service_account(raw_json: str | None) -> dict[str, str]:
    """Read the service-account secret without exposing any secret values."""

    if not raw_json:
        raise ConfigurationError("GA4_SERVICE_ACCOUNT_JSON is required")
    try:
        credentials = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ConfigurationError("GA4_SERVICE_ACCOUNT_JSON is not valid JSON") from exc

    if not isinstance(credentials, dict):
        raise ConfigurationError("GA4_SERVICE_ACCOUNT_JSON must contain an object")

    required = ("client_email", "private_key")
    missing = [
        name
        for name in required
        if not isinstance(credentials.get(name), str) or not credentials[name].strip()
    ]
    if missing:
        raise ConfigurationError("GA4 service account is missing required credentials")

    return {
        "client_email": credentials["client_email"],
        "private_key": credentials["private_key"],
    }


def sign_rs256(message: bytes, private_key: str) -> bytes:
    """Sign a JWT payload with OpenSSL without placing the key in command text."""

    key_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, prefix="ga4-key-"
        ) as key_file:
            key_file.write(private_key)
            key_path = key_file.name
        completed = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", key_path],
            input=message,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise AuthenticationError("OpenSSL is unavailable for GA4 authentication") from exc
    finally:
        if key_path:
            try:
                os.unlink(key_path)
            except FileNotFoundError:
                pass

    if completed.returncode != 0 or not completed.stdout:
        raise AuthenticationError("Could not sign the GA4 service-account assertion")
    return completed.stdout


def build_service_account_assertion(
    credentials: Mapping[str, str],
    now: datetime,
    signer: Callable[[bytes, str], bytes] = sign_rs256,
) -> str:
    """Build the one-hour OAuth assertion used by a Google service account."""

    issued_at = int(now.timestamp())
    header = base64url(json.dumps({"alg": "RS256", "typ": "JWT"}, separators=(",", ":")).encode())
    claims = {
        "iss": credentials["client_email"],
        "scope": ANALYTICS_SCOPE,
        "aud": TOKEN_URL,
        "iat": issued_at,
        "exp": issued_at + 3600,
    }
    encoded_claims = base64url(json.dumps(claims, separators=(",", ":")).encode())
    unsigned_assertion = f"{header}.{encoded_claims}".encode("ascii")
    signature = base64url(signer(unsigned_assertion, credentials["private_key"]))
    return f"{unsigned_assertion.decode('ascii')}.{signature}"


def request_json(http_request: request.Request) -> dict[str, Any]:
    """Send a request and turn transport failures into secret-free errors."""

    try:
        with request.urlopen(http_request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
    except error.HTTPError as exc:
        raise AnalyticsResponseError(f"Google Analytics request failed (HTTP {exc.code})") from exc
    except error.URLError as exc:
        raise AnalyticsResponseError("Could not connect to Google Analytics") from exc
    except TimeoutError as exc:
        raise AnalyticsResponseError("Google Analytics request timed out") from exc

    try:
        parsed = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise AnalyticsResponseError("Google Analytics returned invalid JSON") from exc
    if not isinstance(parsed, dict):
        raise AnalyticsResponseError("Google Analytics returned an invalid response")
    return parsed


def fetch_access_token(
    credentials: Mapping[str, str],
    now: datetime,
    *,
    signer: Callable[[bytes, str], bytes] = sign_rs256,
    request_json_fn: Callable[[request.Request], dict[str, Any]] = request_json,
) -> str:
    assertion = build_service_account_assertion(credentials, now, signer)
    body = parse.urlencode(
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        }
    ).encode("ascii")
    token_request = request.Request(
        TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    response = request_json_fn(token_request)
    token = response.get("access_token")
    if not isinstance(token, str) or not token:
        raise AuthenticationError("Google OAuth did not return an access token")
    return token


def validate_property_id(property_id: str) -> None:
    if not property_id.isdecimal():
        raise ConfigurationError("GA4_PROPERTY_ID must be a numeric GA4 property ID")


def configured_start_date(raw_value: str | None) -> date:
    if not raw_value:
        return DEFAULT_START_DATE
    try:
        return date.fromisoformat(raw_value)
    except ValueError as exc:
        raise ConfigurationError("GA4_START_DATE must use YYYY-MM-DD") from exc


def configured_hostname(raw_value: str | None) -> str:
    hostname = SITE_HOSTNAME if raw_value is None else raw_value
    if not hostname or hostname != hostname.strip() or any(
        character in hostname for character in "/?#"
    ):
        raise ConfigurationError("GA4_HOSTNAME must be a hostname without a URL scheme or path")
    return hostname


def fetch_page_views(
    access_token: str,
    property_id: str,
    start_date: date,
    end_date: date,
    hostname: str = SITE_HOSTNAME,
    *,
    request_json_fn: Callable[[request.Request], dict[str, Any]] = request_json,
) -> dict[str, Any]:
    validate_property_id(property_id)

    report_body = {
        "dateRanges": [{"startDate": start_date.isoformat(), "endDate": end_date.isoformat()}],
        "metrics": [{"name": "screenPageViews"}],
        "limit": "1",
        "dimensionFilter": {
            "filter": {
                "fieldName": "hostName",
                "stringFilter": {"matchType": "EXACT", "value": hostname},
            }
        },
    }
    report_request = request.Request(
        f"{DATA_API_BASE_URL}/properties/{property_id}:runReport",
        data=json.dumps(report_body, separators=(",", ":")).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    return request_json_fn(report_request)


def is_empty_run_report(report: Mapping[str, Any]) -> bool:
    """Recognize GA4's observed minimal response for a property with no data."""

    if report.get("kind") != "analyticsData#runReport":
        return False
    metadata = report.get("metadata")
    if not isinstance(metadata, dict):
        return False
    report_time_zone = metadata.get("timeZone")
    if (
        not isinstance(report_time_zone, str)
        or not report_time_zone
        or report_time_zone != report_time_zone.strip()
    ):
        return False
    try:
        ZoneInfo(report_time_zone)
    except ZoneInfoNotFoundError:
        return False
    if "metricHeaders" in report or "dimensionHeaders" in report:
        return False
    rows = report.get("rows")
    if rows not in (None, []):
        return False
    row_count = report.get("rowCount")
    return row_count is None or (type(row_count) is int and row_count == 0)


def parse_page_view_count(report: Mapping[str, Any]) -> int:
    """Extract one non-negative, whole-number aggregate from a GA4 report."""

    if "error" in report:
        raise AnalyticsResponseError("Google Analytics returned an API error")
    if is_empty_run_report(report):
        return 0
    metric_headers = report.get("metricHeaders")
    if (
        not isinstance(metric_headers, list)
        or len(metric_headers) != 1
        or not isinstance(metric_headers[0], Mapping)
        or metric_headers[0].get("name") != "screenPageViews"
        or metric_headers[0].get("type") != "TYPE_INTEGER"
    ):
        raise AnalyticsResponseError("Google Analytics report has unexpected metric headers")
    dimension_headers = report.get("dimensionHeaders")
    if dimension_headers not in (None, []):
        raise AnalyticsResponseError("Google Analytics report has unexpected dimension headers")
    rows = report.get("rows")
    row_count = report.get("rowCount")
    if row_count is not None and (type(row_count) is not int or row_count < 0):
        raise AnalyticsResponseError("Google Analytics report has an invalid row count")
    if row_count is not None and row_count > 1:
        raise AnalyticsResponseError("Google Analytics report may be truncated")
    if rows is None:
        if row_count in (None, 0):
            return 0
        raise AnalyticsResponseError("Google Analytics report is missing rows")
    if rows == []:
        if row_count not in (None, 0):
            raise AnalyticsResponseError("Google Analytics report is incomplete")
        return 0
    if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
        raise AnalyticsResponseError("Google Analytics report does not contain one aggregate row")
    if row_count not in (None, 1):
        raise AnalyticsResponseError("Google Analytics report is incomplete")
    metric_values = rows[0].get("metricValues")
    if (
        not isinstance(metric_values, list)
        or len(metric_values) != 1
        or not isinstance(metric_values[0], dict)
    ):
        raise AnalyticsResponseError("Google Analytics report does not contain a page-view count")
    value = metric_values[0].get("value")
    if not isinstance(value, str) or not value.isdecimal():
        raise AnalyticsResponseError("Google Analytics returned an invalid page-view count")
    return int(value)


def snapshot_for(
    count: int, start_date: date, end_date: date, now: datetime
) -> dict[str, Any]:
    if count < 0:
        raise AnalyticsResponseError("Google Analytics returned a negative page-view count")
    updated_at = now.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "count": count,
        "metric": "page_views",
        "source": "ga4",
        "counted_from": start_date.isoformat(),
        "through": end_date.isoformat(),
        "updated_at": updated_at,
    }


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    """Replace the snapshot atomically so a failed write cannot corrupt it."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}."
        ) as temporary_file:
            json.dump(payload, temporary_file, ensure_ascii=False, indent=2)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
            temporary_path = temporary_file.name
        os.replace(temporary_path, path)
    finally:
        if temporary_path:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass


def existing_positive_ga4_count(path: Path) -> int | None:
    """Return a prior GA4 count when it is safe to use as a zero-value guard."""

    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    if (
        not isinstance(existing, dict)
        or existing.get("source") != "ga4"
        or type(existing.get("count")) is not int
        or existing["count"] <= 0
    ):
        return None
    return existing["count"]


def previous_shanghai_day(now: datetime | None = None) -> date:
    current_time = now or datetime.now(ZoneInfo("Asia/Shanghai"))
    return current_time.astimezone(ZoneInfo("Asia/Shanghai")).date() - timedelta(days=1)


def update_snapshot(
    credentials: Mapping[str, str],
    property_id: str,
    output_path: Path,
    *,
    start_date: date = DEFAULT_START_DATE,
    end_date: date | None = None,
    now: datetime | None = None,
    token_fetcher: Callable[[Mapping[str, str], datetime], str] = fetch_access_token,
    hostname: str = SITE_HOSTNAME,
    report_fetcher: Callable[[str, str, date, date, str], Mapping[str, Any]] = fetch_page_views,
) -> dict[str, Any]:
    """Query GA4 and write a new snapshot only after all validation succeeds."""

    timestamp = now or datetime.now(timezone.utc)
    through = end_date or previous_shanghai_day(timestamp)
    if through < start_date:
        raise ConfigurationError("The GA4 reporting end date precedes the start date")
    validate_property_id(property_id)

    access_token = token_fetcher(credentials, timestamp)
    report = report_fetcher(access_token, property_id, start_date, through, hostname)
    empty_report = is_empty_run_report(report)
    count = parse_page_view_count(report)
    if empty_report and count == 0 and existing_positive_ga4_count(output_path) is not None:
        raise SnapshotSafetyError("refusing to replace an existing GA4 count with an empty report")
    snapshot = snapshot_for(count, start_date, through, timestamp)
    atomic_write_json(output_path, snapshot)
    return snapshot


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("dates must use YYYY-MM-DD") from exc


def main(argv: list[str] | None = None, environ: Mapping[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="JSON snapshot path")
    parser.add_argument("--start-date", type=parse_date, help="Reporting start date (overrides GA4_START_DATE)")
    parser.add_argument("--through", type=parse_date, help="Report end date (defaults to yesterday in Asia/Shanghai)")
    arguments = parser.parse_args(argv)
    environment = environ if environ is not None else os.environ

    try:
        credentials = load_service_account(environment.get("GA4_SERVICE_ACCOUNT_JSON"))
        property_id = environment.get("GA4_PROPERTY_ID", "")
        start_date = arguments.start_date or configured_start_date(environment.get("GA4_START_DATE"))
        hostname = configured_hostname(environment.get("GA4_HOSTNAME"))
        snapshot = update_snapshot(
            credentials,
            property_id,
            arguments.output,
            start_date=start_date,
            end_date=arguments.through,
            hostname=hostname,
        )
    except VisitsError as exc:
        print(f"Visits snapshot was not updated: {exc}", file=sys.stderr)
        return 1

    print(f"Updated visits snapshot through {snapshot['through']}: {snapshot['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
