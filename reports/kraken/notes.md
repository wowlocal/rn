# Kraken React Native Timeline

## Registration

- App name: Kraken
- App Store ID: 1481947260
- iOS bundle ID: com.kraken.invest.app
- Android package: com.kraken.invest.app
- Status: skipped
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- Apple iTunes lookup for App Store ID `1481947260` returned app name `Kraken: Buy Crypto & Stocks`, seller `Payward, Inc.`, bundle ID `com.kraken.invest.app`, and current listed version `3.65.0`.
- App Store URL: `https://apps.apple.com/us/app/kraken-buy-crypto-stocks/id1481947260`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.kraken.invest.app`.
- Android package source: Google Play, AppBrain, and AppRecs identify package `com.kraken.invest.app`.
- APKPure history source check: tested `com.kraken.invest.app` APKPure history URLs returned HTTP `410 Gone`, so no APKPure Android version catalog is available at registration time.
- `ipatool search Kraken --format json` did not surface the finance app in the current localized search results; App Store ID was resolved from the public App Store URL and Apple iTunes lookup.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `1481947260` and bundle ID `com.kraken.invest.app`.
- iOS version list result: failed because app-ID lookup reports `license is required`, while bundle-ID lookup reports `app not found`.
- iOS license attempt: `ipatool purchase --bundle-identifier com.kraken.invest.app --format json` failed with `app not found`.
- Raw iOS version-list error: `reports/kraken/version-list-error.json`
- Android version list result: skipped because checked APKPure history URLs for `com.kraken.invest.app` returned HTTP `410 Gone`.

## Open Gaps

- RN usage was not verified because no iOS version history or usable Android package-history source is available through the current automated tools.
- Google Play confirms the Android package identity, but does not provide a downloadable historical APK catalog for this workflow.

## Next Step

None with the current automated sources; revisit only if iOS license access works or a usable Android package-history source for `com.kraken.invest.app` is found.
