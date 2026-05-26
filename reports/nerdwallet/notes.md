# NerdWallet React Native Timeline

## Registration

- App name: NerdWallet: Smart Money App
- App Store ID: 1174471607
- iOS bundle ID: org.reactjs.native.example.MobileCreditCards
- Android package: com.mobilecreditcards
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search NerdWallet --format json` did not return the official NerdWallet finance app in the current localized results.
- Apple iTunes lookup for App Store ID `1174471607` returned app name `NerdWallet: Smart Money App`, seller `Nerdwallet, Inc.`, bundle ID `org.reactjs.native.example.MobileCreditCards`, current US listed version `14.19.0`, and release date `2026-05-13T15:38:33Z`.
- App Store URL: `https://apps.apple.com/us/app/nerdwallet-smart-money-app/id1174471607`.
- Google Play identifies Android package `com.mobilecreditcards` and returned HTTP `200`.
- Uptodown versions URL identified: `https://nerdwallet.en.uptodown.com/android/versions?utm_source=main` returned HTTP `200`.
- APKPure Android history URL checked: `https://apkpure.net/nerdwallet-personal-finance/com.mobilecreditcards/versions` returned HTTP `410`.
- APKCombo old versions URL checked: `https://apkcombo.com/nerdwallet/com.mobilecreditcards/old-versions/` returned HTTP `410`.
- AndroidAPKsFree guessed old versions URL for package `com.mobilecreditcards` returned HTTP `404`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 1174471607`.
- iOS version list result: failed because App Store license is required.
- Bundle-ID iOS version list fetch for `org.reactjs.native.example.MobileCreditCards` returned app not found.
- Raw iOS version-list errors: `reports/nerdwallet/version-list-error.json` and `reports/nerdwallet/version-list-bundle-error.json`
- Android Uptodown catalog fetched on 2026-05-26 with `fetch_uptodown_versions.py`.
- Android entries available from Uptodown sources: 20
- Oldest Uptodown source date in the catalog: `2024-10-10` (`12.1.0`)
- Newest Uptodown source date in the catalog: `2026-02-13` (`12.10.1`)
- Raw Android version catalog: `reports/nerdwallet/android-version-list.json`
- Source-specific Uptodown catalog: `reports/nerdwallet/android-version-list-uptodown.json`
- Uptodown exposes page-specific version IDs, not verified Android manifest versionCodes.
- Uptodown rows point at download pages; direct package download support may require decoding page-specific download tokens.

## Next Step

Try to resolve a direct Uptodown package download for one visible Android row, or move to the next candidate if direct downloads remain blocked.
