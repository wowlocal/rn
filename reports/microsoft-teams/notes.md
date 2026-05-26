# Microsoft Teams React Native Timeline

## Registration

- App name: Microsoft Teams
- App Store ID: 1113153706
- iOS bundle ID: com.microsoft.skype.teams
- Android package: com.microsoft.teams
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Microsoft Teams --format json` returned App Store ID `1113153706`, bundle ID `com.microsoft.skype.teams`, and current listed version `8.9.1`.
- Apple iTunes lookup for App Store ID `1113153706` returned app name `Microsoft Teams`, seller `Microsoft Corporation`, bundle ID `com.microsoft.skype.teams`, and current US listed version `8.9.0`.
- App Store URL: `https://apps.apple.com/us/app/microsoft-teams/id1113153706`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.microsoft.teams`.
- Android package history source identified: APKPure page for package `com.microsoft.teams`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `1113153706` and bundle ID `com.microsoft.skype.teams`.
- iOS version list result: failed because both app-ID and bundle-ID lookup returned Apple's generic unknown error.
- iOS license attempt: `ipatool purchase --bundle-identifier com.microsoft.skype.teams --format json` failed with an invalid HTML response.
- Raw iOS version-list error: `reports/microsoft-teams/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `2026015023` (`1416/1.0.0.2026015002`)
- Newest Android versionCode in the APKPure catalog: `2026082725` (`1416/1.0.0.2026082702`)
- Raw Android version catalog: `reports/microsoft-teams/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Android package source: APKPure visible catalog
- Android RN markers detected: yes, in every sampled package.
- Exposed React Native native-library metadata includes `libreactnative.so`, `libhermes.so`, `libhermestooling.so`, `libjsi.so`, and `libjsiasyncstorage.so`.
- Current Android RN inference: `0.60.x`, medium confidence.
- Android reports: `reports/microsoft-teams/android-versions.csv`, `reports/microsoft-teams/android-ranges.csv`, and empty `reports/microsoft-teams/android-transitions.json`.
- iOS sampling was not performed because iOS version-list access is blocked and Android packages exposed usable RN markers.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.60.x | medium | 1416/1.0.0.2026015002 (`2026015023`), APKPure date `2026-01-21` | 1416/1.0.0.2026082702 (`2026082725`), APKPure date `2026-05-11` | 10 |

## Open Gaps

- APKPure remains sparse/source-limited and exposes only 10 visible rows across the sampled window.
- iOS version-list access remains blocked by App Store errors, so no iOS cross-check is available.
- No RN transition was observed in the accessible Android package window.
- Disk cleanup was not performed after Android sampling because `apks/microsoft-teams` used about 2.2 GiB and the filesystem still had 215 GiB available.

## Next Step

Manual review should use a more complete Android package history or targeted iOS IPAs, if iOS version-list access becomes available, to identify whether an RN upgrade boundary exists outside the visible APKPure window.
