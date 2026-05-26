# Salesforce React Native Timeline

## Registration

- App name: Salesforce
- App Store ID: 404249815
- iOS bundle ID: com.salesforce.chatter
- Android package: com.salesforce.chatter
- Status: needs_manual_review
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
- APKPure package validation found one unique payload hash across all 10 fetched rows, and the embedded manifest metadata matched the current `260.050.0` package for every row. The APKPure catalog is retained as `reports/salesforce/android-version-list-apkpure.json` but is not used as the primary timeline source.
- Android APKCombo catalog fetched on 2026-05-26 with `fetch_apkcombo_versions.py`.
- Android entries available from APKCombo sources: 30
- Oldest Android versionCode in the APKCombo catalog: `250030032` (`250.030.0`)
- Newest Android versionCode in the APKCombo catalog: `260050025` (`260.050.0`)
- Raw primary Android version catalog: `reports/salesforce/android-version-list.json`
- Source-specific APKCombo catalog: `reports/salesforce/android-version-list-apkcombo.json`
- APKCombo exposes a limited visible old-version catalog, so Android boundaries remain source-limited.

## Android Sampling

- Downloaded and analyzed 10 evenly spaced APKCombo XAPK rows from versionCode `250030032` (`250.030.0`, source date 2024-08-19) through `260050025` (`260.050.0`, source date 2026-05-09).
- Package hash validation found 10 unique payload hashes across the 10 sampled APKCombo rows.
- No sampled Android package exposed React Native JS bundle or native-library markers.
- Bundle-like files under `assets/EclairNG/runtime-modules` and `assets/runtime-modules` are Salesforce chart/runtime assets, not React Native evidence.
- Android range summary: `250.030.0` through `260.050.0` is `unknown` with low confidence because no `react-native-renderer`, Hermes, React Native native-library, or React Native symbol markers were found.

## Result

- Status: `needs_manual_review`
- Reason: iOS version-list access is blocked and the available Android catalog is source-limited, despite no RN markers in the sampled APKCombo packages.
