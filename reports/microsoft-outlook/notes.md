# Microsoft Outlook React Native Timeline

## Registration

- App name: Microsoft Outlook
- App Store ID: 951937596
- iOS bundle ID: com.microsoft.Office.Outlook
- Android package: com.microsoft.office.outlook
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Microsoft Outlook --format json` returned App Store ID `951937596`, bundle ID `com.microsoft.Office.Outlook`, and current listed version `5.2619.0`.
- Apple iTunes lookup for App Store ID `951937596` returned app name `Microsoft Outlook`, seller `Microsoft Corporation`, bundle ID `com.microsoft.Office.Outlook`, and current listed version `5.2619.0`.
- App Store URL: `https://apps.apple.com/us/app/microsoft-outlook/id951937596`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.microsoft.office.outlook`.
- Android package history source identified: APKPure page for package `com.microsoft.office.outlook`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `951937596` and bundle ID `com.microsoft.Office.Outlook`.
- iOS version list result: failed because both app-ID and bundle-ID lookup returned Apple's generic unknown error.
- iOS license attempt: `ipatool purchase --bundle-identifier com.microsoft.Office.Outlook --format json` failed with `unsupported protocol scheme`.
- Raw iOS version-list error: `reports/microsoft-outlook/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android source date in the APKPure catalog: `2025-02-24` (`4.2504.2`, versionCode `82504829`)
- Newest Android source date in the APKPure catalog: `2026-05-23` (`5.2619.0`, versionCode `72619117`)
- Raw Android version catalog: `reports/microsoft-outlook/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.
- Android versionCode values are not monotonic with APKPure source dates in the fetched Outlook catalog, so date ordering must be reviewed when summarizing Android ranges.

## Next Step

Download and analyze the visible Android packages first; use iOS IPAs only if iOS version-list access becomes available.
