# Salesforce React Native Timeline

## Registration

- App name: Salesforce
- App Store ID: 404249815
- iOS bundle ID: com.salesforce.chatter
- Android package: com.salesforce.chatter
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Salesforce --format json` returned App Store ID `404249815`, bundle ID `com.salesforce.chatter`, app name `Salesforce`, and current listed version `260.051`.
- Apple iTunes lookup for App Store ID `404249815` returned app name `Salesforce`, seller `salesforce.com`, bundle ID `com.salesforce.chatter`, current US listed version `260.051`, and release date `2026-05-14T17:18:32Z`.
- App Store URL: `https://apps.apple.com/us/app/salesforce/id404249815`.
- Android package sources identify package `com.salesforce.chatter`.
- APKPure Android history URL identified: `https://apkpure.net/salesforce/com.salesforce.chatter/versions`.
- APKCombo old versions URL identified: `https://apkcombo.com/salesforce/com.salesforce.chatter/old-versions/`.
- APKPure `.com` versions URL returned HTTP `403`, but the APKPure `.net` versions URL returned HTTP `200`.
- AndroidAPKsFree guessed old versions URL for package `com.salesforce.chatter` returned HTTP `404`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 404249815`.
- iOS version list result: failed because App Store license is required.
- iOS license attempt for bundle ID `com.salesforce.chatter` failed with unsupported protocol scheme.
- Bundle-ID iOS version list also failed because App Store license is required.
- Raw iOS version-list error: `reports/salesforce/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `256043000` (`256.043.0`)
- Newest Android versionCode in the APKPure catalog: `260050025` (`260.050.0`)
- Raw Android version catalog: `reports/salesforce/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Next Step

Sample the visible Android APKPure catalog first because iOS version-list access is blocked.
