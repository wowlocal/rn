# NerdWallet React Native Timeline

## Registration

- App name: NerdWallet: Smart Money App
- App Store ID: 1174471607
- iOS bundle ID: org.reactjs.native.example.MobileCreditCards
- Android package: com.mobilecreditcards
- Status: registered
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

## Next Step

Fetch the iOS version list. If available, prefer iOS sampling because the App Store bundle ID itself indicates a React Native-origin app and the Android package-history sources are limited.
