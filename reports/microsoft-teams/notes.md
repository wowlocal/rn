# Microsoft Teams React Native Timeline

## Registration

- App name: Microsoft Teams
- App Store ID: 1113153706
- iOS bundle ID: com.microsoft.skype.teams
- Android package: com.microsoft.teams
- Status: version_list_fetched
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

## Next Step

Download and analyze the visible Android packages first; use iOS IPAs only if iOS version-list access becomes available.
