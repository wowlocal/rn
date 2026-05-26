# Microsoft Outlook React Native Timeline

## Registration

- App name: Microsoft Outlook
- App Store ID: 951937596
- iOS bundle ID: com.microsoft.Office.Outlook
- Android package: com.microsoft.office.outlook
- Status: needs_manual_review
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

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Android package source: APKPure visible catalog
- Android RN markers detected: yes, through native-library metadata in every sampled package.
- Exposed React Native native-library metadata includes Hermes/JSI and either `libreactnative.so` or `libreactnativejni.so`.
- Bundle-like assets were present but did not expose usable React Native version markers such as `react-native-renderer` or `ReactNativeVersion`.
- Current Android RN inference: unknown version, low confidence.
- Android reports: `reports/microsoft-outlook/android-versions.csv`, `reports/microsoft-outlook/android-ranges.csv`, and empty `reports/microsoft-outlook/android-transitions.json`.
- iOS sampling was not performed because iOS version-list access is blocked.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | unknown | low | 4.2504.2 (`82504829`), APKPure date `2025-02-24` | 5.2619.0 (`72619117`), APKPure date `2026-05-23` | 10 |

## Open Gaps

- APKPure remains sparse/source-limited and exposes only 10 visible rows across the sampled window.
- iOS version-list access remains blocked by App Store errors, so no iOS cross-check is available.
- Android versionCode values are non-monotonic with source dates in this catalog, so source publish dates must be used when reviewing the Android timeline.
- No RN version boundary was observed because the sampled Android packages expose RN native libraries but no usable RN version markers.
- Disk cleanup was not performed after Android sampling because `apks/microsoft-outlook` used about 1.6 GiB and the filesystem still had 218 GiB available.

## Next Step

Manual review should use a more complete Android package history or targeted iOS IPAs, if iOS version-list access becomes available, to identify a RN version band or upgrade boundary.
