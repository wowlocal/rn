# Base: Formerly Coinbase Wallet React Native Timeline

## Registration

- App name: Base: Formerly Coinbase Wallet
- Former queue name: Coinbase Wallet
- App Store ID: 1278383455
- iOS bundle ID: org.toshi.distribution
- Android package: org.toshi
- Status: skipped
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md` as Coinbase Wallet.
- `ipatool search Coinbase Wallet --format json` returned App Store ID `1278383455`, bundle ID `org.toshi.distribution`, and localized app name `Base: Formerly Coinbase Wallet`.
- Apple iTunes lookup for App Store ID `1278383455` returned app name `Base: Built to Trade & Earn`, seller `Coinbase Wallet`, bundle ID `org.toshi.distribution`, and current listed version `29.96`.
- App Store URL: `https://apps.apple.com/us/app/base-built-to-trade-earn/id1278383455`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=org.toshi`.
- Android package source: Google Play, AppBrain, and WalletScrutiny identify package `org.toshi`.
- APKPure history source check: tested `org.toshi` APKPure history URLs returned HTTP `410 Gone`, so no APKPure Android version catalog is available at registration time.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `1278383455` and bundle ID `org.toshi.distribution`.
- iOS version list result: failed because both app-ID and bundle-ID lookup report `license is required`.
- iOS license attempt: `ipatool purchase --bundle-identifier org.toshi.distribution --format json` failed with `unsupported protocol scheme`.
- Raw iOS version-list error: `reports/coinbase-wallet/version-list-error.json`
- Android version list result: skipped because checked APKPure history URLs for `org.toshi` returned HTTP `410 Gone`.

## Open Gaps

- RN usage was not verified because no iOS version history or usable Android package-history source is available through the current automated tools.
- Google Play confirms the Android package identity, but does not provide a downloadable historical APK catalog for this workflow.

## Next Step

None with the current automated sources; revisit only if iOS license access works or a usable Android package-history source for `org.toshi` is found.
