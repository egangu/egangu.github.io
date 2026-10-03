# Visits snapshot

The sidebar renders `Visits` from `_data/visits.json` at build time. It makes no browser request to a counter service. The value is GA4 `screenPageViews` for `egangu.github.io`, including repeat views, from 2026-10-03 (when the new GA4 property was set up) through yesterday. It is not a unique visitor count and is not the old Busuanzi total. The old GA measurement ID was inaccessible from the current Google account, so historical counts are not carried over.

The **Update visits snapshot** GitHub Actions workflow runs daily at approximately 06:17 Asia/Shanghai and can also be run manually. API or authentication failures leave the last good snapshot intact. With no snapshot yet, the sidebar omits the counter instead of displaying a fabricated zero. The tooltip identifies the date covered by the data.

## One-time setup

1. In Google Analytics, open the GA4 property whose web stream has measurement ID `G-056GMH4WGW`. Copy its numeric **Property ID** from Admin → Property details. This is different from the `G-…` measurement ID.
2. In Google Cloud, enable the **Google Analytics Data API** in a project and create a service account for the snapshot job. This task needs no paid resource and no Google Cloud project IAM role.
3. In the GA4 property's **Property access management**, add the service account email as **Viewer**. This grants read access to the property's reports, so use a property dedicated to the homepage.
4. Create a JSON key for the service account. Store its contents as repository Actions secret `GA4_SERVICE_ACCOUNT_JSON`, and set repository Actions variable `GA4_PROPERTY_ID` to the numeric ID. Never commit the JSON key.
5. Run **Update visits snapshot** manually. Confirm `_data/visits.json` is committed, followed by a successful **Build and deploy site** run. The deployment listens for `workflow_run` because commits made by `GITHUB_TOKEN` do not trigger a `push` workflow.

With GitHub CLI, set the configuration from a local key file without printing it:

```sh
gh variable set GA4_PROPERTY_ID --repo egangu/egangu.github.io --body YOUR_NUMERIC_PROPERTY_ID
gh secret set GA4_SERVICE_ACCOUNT_JSON --repo egangu/egangu.github.io < /absolute/path/to/service-account.json
gh workflow run update-visits.yml --repo egangu/egangu.github.io --ref main
```

Optional repository variables `GA4_START_DATE` and `GA4_HOSTNAME` override the counting scope for a deliberate migration. The manual workflow's optional `through` input overrides the end date; use today's date only to bootstrap a newly created property, before yesterday has any data. That first snapshot may be zero and is a partial-day result. Daily runs return to yesterday. The exporter uses Python's standard library and OpenSSL, with no Python package installation.

## Verification and recovery

```sh
python3 -m unittest discover -s scripts/tests -v
```

Check a failed update's Actions log and restore API/key/Viewer access, then rerun it. Never replace a failed read with zero. A concurrent push to `main` causes the snapshot push to fail safely; rerun the workflow on the latest checkout. GitHub schedules may be delayed and are disabled for public repositories after 60 days without repository activity; a manual run is always available.

References: [GA4 Data API quickstart](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart), [metric schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema), [GitHub workflow triggers](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).
