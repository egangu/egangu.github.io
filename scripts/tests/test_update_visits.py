import base64
import json
from datetime import date, datetime, timezone
from pathlib import Path
import tempfile
import unittest

from scripts import update_visits


def complete_report(value, *, row_count=1):
    report = {
        "metricHeaders": [{"name": "screenPageViews", "type": "TYPE_INTEGER"}],
        "metadata": {"timeZone": "Asia/Shanghai"},
    }
    if value is not None:
        report["rows"] = [{"metricValues": [{"value": value}]}]
    if row_count is not None:
        report["rowCount"] = row_count
    return report


EMPTY_RUN_REPORT = {
    "metadata": {"currencyCode": "CNY", "timeZone": "Asia/Shanghai"},
    "kind": "analyticsData#runReport",
}


class UpdateVisitsTests(unittest.TestCase):
    def test_service_account_assertion_has_expected_claims(self):
        credentials = {"client_email": "counter@example.iam.gserviceaccount.com", "private_key": "private"}
        issued = datetime(2026, 10, 3, 1, 2, 3, tzinfo=timezone.utc)
        assertion = update_visits.build_service_account_assertion(
            credentials, issued, signer=lambda _message, _key: b"signature"
        )

        header, claims, signature = assertion.split(".")
        self.assertEqual(signature, base64.urlsafe_b64encode(b"signature").rstrip(b"=").decode())
        decoded_header = json.loads(base64.urlsafe_b64decode(header + "=="))
        decoded_claims = json.loads(base64.urlsafe_b64decode(claims + "=="))
        self.assertEqual(decoded_header, {"alg": "RS256", "typ": "JWT"})
        self.assertEqual(decoded_claims["iss"], credentials["client_email"])
        self.assertEqual(decoded_claims["scope"], update_visits.ANALYTICS_SCOPE)
        self.assertEqual(decoded_claims["aud"], update_visits.TOKEN_URL)
        self.assertEqual(decoded_claims["exp"] - decoded_claims["iat"], 3600)

    def test_fetch_page_views_requests_hostname_scoped_screen_page_views(self):
        captured = {}

        def respond(http_request):
            captured["url"] = http_request.full_url
            captured["headers"] = dict(http_request.header_items())
            captured["body"] = json.loads(http_request.data.decode("utf-8"))
            return complete_report("51")

        report = update_visits.fetch_page_views(
            "token", "123456", date(2020, 1, 1), date(2026, 10, 2), request_json_fn=respond
        )

        self.assertEqual(report["rows"][0]["metricValues"][0]["value"], "51")
        self.assertEqual(captured["url"], "https://analyticsdata.googleapis.com/v1beta/properties/123456:runReport")
        self.assertEqual(captured["headers"]["Authorization"], "Bearer token")
        self.assertEqual(captured["body"]["metrics"], [{"name": "screenPageViews"}])
        self.assertEqual(captured["body"]["limit"], "1")
        self.assertEqual(
            captured["body"]["dimensionFilter"]["filter"],
            {"fieldName": "hostName", "stringFilter": {"matchType": "EXACT", "value": "egangu.github.io"}},
        )

    def test_invalid_report_preserves_existing_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "visits.json"
            existing = '{"count": 41, "source": "ga4"}\n'
            output.write_text(existing, encoding="utf-8")

            with self.assertRaises(update_visits.AnalyticsResponseError):
                update_visits.update_snapshot(
                    {"client_email": "counter@example.com", "private_key": "private"},
                    "123456",
                    output,
                    end_date=date(2026, 10, 3),
                    now=datetime(2026, 10, 3, tzinfo=timezone.utc),
                    token_fetcher=lambda _credentials, _now: "token",
                    report_fetcher=lambda *_args: complete_report("41.5"),
                )

            self.assertEqual(output.read_text(encoding="utf-8"), existing)

    def test_successful_update_replaces_snapshot_with_validated_ga4_count(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "visits.json"
            output.write_text('{"count": 41}\n', encoding="utf-8")
            snapshot = update_visits.update_snapshot(
                {"client_email": "counter@example.com", "private_key": "private"},
                "123456",
                output,
                end_date=date(2026, 10, 3),
                now=datetime(2026, 10, 3, 8, 9, 10, 123, tzinfo=timezone.utc),
                token_fetcher=lambda _credentials, _now: "token",
                report_fetcher=lambda *_args: complete_report("52"),
            )

            self.assertEqual(
                snapshot,
                {
                    "count": 52,
                    "metric": "page_views",
                    "source": "ga4",
                    "counted_from": "2026-10-03",
                    "through": "2026-10-03",
                    "updated_at": "2026-10-03T08:09:10Z",
                },
            )
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), snapshot)

    def test_missing_credentials_fail_without_overwriting_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "visits.json"
            existing = '{"count": 41}\n'
            output.write_text(existing, encoding="utf-8")

            exit_code = update_visits.main(["--output", str(output)], environ={"GA4_PROPERTY_ID": "123456"})

            self.assertEqual(exit_code, 1)
            self.assertEqual(output.read_text(encoding="utf-8"), existing)

    def test_empty_valid_report_means_zero_but_error_or_truncated_reports_are_rejected(self):
        self.assertEqual(update_visits.parse_page_view_count(EMPTY_RUN_REPORT), 0)
        self.assertEqual(update_visits.parse_page_view_count(complete_report(None, row_count=0)), 0)
        self.assertEqual(update_visits.parse_page_view_count(complete_report(None, row_count=None)), 0)
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count({"error": {"code": 503}})
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count(complete_report(None, row_count=1))
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count(complete_report(None, row_count=2))
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count(complete_report("1", row_count=0))
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count({"rows": []})
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count(
                {"metricHeaders": [{"name": "screenPageViews", "type": "TYPE_FLOAT"}]}
            )
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count(complete_report("1", row_count="1"))
        with self.assertRaises(update_visits.AnalyticsResponseError):
            update_visits.parse_page_view_count(complete_report("1", row_count=True))
        self.assertEqual(update_visits.parse_page_view_count({**EMPTY_RUN_REPORT, "rows": []}), 0)
        self.assertEqual(update_visits.parse_page_view_count({**EMPTY_RUN_REPORT, "rowCount": 0}), 0)
        self.assertEqual(
            update_visits.parse_page_view_count({**EMPTY_RUN_REPORT, "rows": [], "rowCount": 0}), 0
        )

    def test_metric_header_validation_allows_additional_ga4_fields(self):
        report = complete_report("1")
        report["metricHeaders"][0]["futureField"] = "ignored"

        self.assertEqual(update_visits.parse_page_view_count(report), 1)

    def test_first_empty_run_report_writes_a_zero_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "visits.json"
            snapshot = update_visits.update_snapshot(
                {"client_email": "counter@example.com", "private_key": "private"},
                "123456",
                output,
                end_date=date(2026, 10, 3),
                now=datetime(2026, 10, 3, 8, 9, 10, tzinfo=timezone.utc),
                token_fetcher=lambda _credentials, _now: "token",
                report_fetcher=lambda *_args: EMPTY_RUN_REPORT,
            )

            self.assertEqual(snapshot["count"], 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["count"], 0)

    def test_empty_run_report_cannot_replace_an_existing_positive_ga4_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "visits.json"
            existing = '{"count": 51, "source": "ga4"}\n'
            output.write_text(existing, encoding="utf-8")

            with self.assertRaises(update_visits.SnapshotSafetyError):
                update_visits.update_snapshot(
                    {"client_email": "counter@example.com", "private_key": "private"},
                    "123456",
                    output,
                    end_date=date(2026, 10, 3),
                    now=datetime(2026, 10, 3, tzinfo=timezone.utc),
                    token_fetcher=lambda _credentials, _now: "token",
                    report_fetcher=lambda *_args: EMPTY_RUN_REPORT,
                )

            self.assertEqual(output.read_text(encoding="utf-8"), existing)

    def test_transport_failure_preserves_existing_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "visits.json"
            existing = '{"count": 41, "source": "ga4"}\n'
            output.write_text(existing, encoding="utf-8")

            def unavailable(*_args):
                raise update_visits.AnalyticsResponseError("Could not connect to Google Analytics")

            with self.assertRaises(update_visits.AnalyticsResponseError):
                update_visits.update_snapshot(
                    {"client_email": "counter@example.com", "private_key": "private"},
                    "123456",
                    output,
                    end_date=date(2026, 10, 3),
                    now=datetime(2026, 10, 3, tzinfo=timezone.utc),
                    token_fetcher=unavailable,
                )

            self.assertEqual(output.read_text(encoding="utf-8"), existing)

    def test_environment_configuration_defaults_and_overrides(self):
        self.assertEqual(update_visits.configured_start_date(None), date(2026, 10, 3))
        self.assertEqual(update_visits.configured_start_date(""), date(2026, 10, 3))
        self.assertEqual(update_visits.configured_start_date("2026-06-01"), date(2026, 6, 1))
        self.assertEqual(update_visits.configured_hostname(None), "egangu.github.io")
        self.assertEqual(update_visits.configured_hostname(""), "egangu.github.io")
        self.assertEqual(update_visits.configured_hostname("www.egangu.github.io"), "www.egangu.github.io")
        with self.assertRaises(update_visits.ConfigurationError):
            update_visits.configured_start_date("06-01-2026")
        with self.assertRaises(update_visits.ConfigurationError):
            update_visits.configured_start_date(" 2026-06-01")
        with self.assertRaises(update_visits.ConfigurationError):
            update_visits.configured_hostname("https://egangu.github.io")
        with self.assertRaises(update_visits.ConfigurationError):
            update_visits.configured_hostname(" egangu.github.io")
        with self.assertRaises(update_visits.ConfigurationError):
            update_visits.validate_property_id("123456 ")


if __name__ == "__main__":
    unittest.main()
