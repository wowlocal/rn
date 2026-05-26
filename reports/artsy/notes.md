# Artsy React Native Timeline

## Registration

- App name: Artsy: Buy & Sell Fine Art
- App Store ID: 703796080
- iOS bundle ID: net.artsy.artsy
- Android package: net.artsy.app
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Artsy --format json` returned App Store ID `703796080`, bundle ID `net.artsy.artsy`, app name `Artsy: Buy & Sell Fine Art`, and current listed version `9.9.0`.
- Apple iTunes lookup for App Store ID `703796080` returned app name `Artsy: Buy & Sell Fine Art`, seller `Art.sy Inc.`, bundle ID `net.artsy.artsy`, current US listed version `9.9.0`, and release date `2026-05-20T17:57:36Z`.
- App Store URL: `https://apps.apple.com/us/app/artsy-buy-sell-fine-art/id703796080`.
- Android package sources identify package `net.artsy.app`.
- APKPure Android history URL identified: `https://apkpure.net/artsy-buy-resell-artworks/net.artsy.app/versions` returned HTTP `200`.
- APKCombo old versions URL identified: `https://apkcombo.com/artsy-buy-sell-fine-art/net.artsy.app/old-versions/` returned HTTP `200`.
- Uptodown versions URL identified: `https://artsy.en.uptodown.com/android/versions?utm_source=main` returned HTTP `200`.
- AndroidAPKsFree guessed old versions URL for package `net.artsy.app` returned HTTP `404`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 703796080`.
- iOS external versions available: 292
- Oldest iOS external version ID: `23362671`
- Newest iOS external version ID: `885363722`
- Raw iOS version list: `reports/artsy/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `2026022618` (`9.0.1`)
- Newest Android versionCode in the APKPure catalog: `2026052012` (`9.9.0`)
- Raw Android version catalog: `reports/artsy/android-version-list.json`
- Source-specific APKPure catalog: `reports/artsy/android-version-list-apkpure.json`
- APKPure currently exposes a limited visible history on the fetched page.
- Android APKCombo fetch rejected decoded variant payloads that were not HTTP(S) URLs; error log: `reports/artsy/android-version-list-apkcombo-error.txt`

## Next Step

Sample the visible Android APKPure catalog first, then use the iOS version list to cross-check if Android exposes a usable RN timeline.
