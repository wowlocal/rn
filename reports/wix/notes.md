# Wix React Native Timeline

## Registration

- App name: Wix - Website Builder
- App Store ID: 1545924344
- iOS bundle ID: com.wix.admin
- Android package: com.wix.admin
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Wix --format json` returned App Store ID `1545924344`, bundle ID `com.wix.admin`, app name `Wix - Website Builder`, and current listed version `2.122966.0`.
- Apple iTunes lookup for App Store ID `1545924344` returned app name `Wix - Website Builder`, seller `WIX.COM, INC.`, bundle ID `com.wix.admin`, current US listed version `2.122966.0`, and release date `2026-05-19T12:40:37Z`.
- App Store URL: `https://apps.apple.com/us/app/wix-website-builder/id1545924344`.
- Android package sources identify package `com.wix.admin`.
- APKPure Android history URL identified: `https://apkpure.net/wix-owner-website-builder/com.wix.admin/versions` returned HTTP `200`.
- APKCombo old versions URL identified: `https://apkcombo.com/wix-owner/com.wix.admin/old-versions/` returned HTTP `200`.
- AndroidAPKsFree guessed old versions URL for package `com.wix.admin` returned HTTP `404`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 1545924344`.
- iOS version list result: failed because App Store license is required.
- Bundle-ID iOS version list fetch for `com.wix.admin` also failed because App Store license is required.
- Raw iOS version-list errors: `reports/wix/version-list-error.json` and `reports/wix/version-list-bundle-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `130467` (`2.115937.0`)
- Newest Android versionCode in the APKPure catalog: `137496` (`2.122966.0`)
- Raw Android version catalog: `reports/wix/android-version-list.json`
- Source-specific APKPure catalog: `reports/wix/android-version-list-apkpure.json`
- APKPure currently exposes a limited visible history on the fetched page.
- Android APKCombo fetch rejected decoded variant payloads that were not HTTP(S) URLs; error log: `reports/wix/android-version-list-apkcombo-error.txt`

## Next Step

Sample the visible Android APKPure catalog first because iOS version-list access is blocked.
