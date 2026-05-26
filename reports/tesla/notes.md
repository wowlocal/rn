# Tesla React Native Timeline

## Registration

- App name: Tesla
- App Store ID: 582007913
- iOS bundle ID: com.teslamotors.TeslaApp
- Android package: com.teslamotors.tesla
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Tesla --format json` did not return the official Tesla app in the current localized results.
- Public App Store URL and Apple iTunes lookup for App Store ID `582007913` returned app name `Tesla`, seller `Tesla, Inc.`, bundle ID `com.teslamotors.TeslaApp`, and current US listed version `4.57.0`.
- App Store URL: `https://apps.apple.com/us/app/tesla/id582007913`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.teslamotors.tesla`.
- Android package sources identify package `com.teslamotors.tesla`.
- APKPure history page identified: `https://apkpure.net/tesla/com.teslamotors.tesla/versions`.
- The guessed AndroidAPKsFree old versions URL for package `com.teslamotors.tesla` returned HTTP 404.

## Next Step

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 582007913`.
- iOS version list result: failed because App Store license is required.
- iOS license attempt for bundle ID `com.teslamotors.TeslaApp` returned app not found.
- Raw iOS version-list error: `reports/tesla/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `4107` (`4.54.3-4107`)
- Newest Android versionCode in the APKPure catalog: `4306` (`4.57.0-4306`)
- Raw Android version catalog: `reports/tesla/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.
- Android versionCode values are not fully monotonic with APKPure source dates in the fetched catalog, so date ordering must be reviewed when summarizing Android ranges.

## Next Step

Sample the visible Android APKPure catalog first because iOS version-list access is blocked.
