# NerdWallet React Native Timeline

## Registration

- App name: NerdWallet: Smart Money App
- App Store ID: 1174471607
- iOS bundle ID: org.reactjs.native.example.MobileCreditCards
- Android package: com.mobilecreditcards
- Status: needs_manual_review
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

## Android Sampling

- Android sampling completed on 2026-05-26 from 10 source-limited Uptodown rows.
- The default Uptodown download button resolves to an Uptodown App Store installer/wrapper and is not valid NerdWallet package evidence.
- The analyzer now resolves the page's variants endpoint and uses `.../download/<source-id>-x` variant pages to download the actual NerdWallet APK/XAPK payloads.
- Embedded manifest metadata from `aapt dump badging` confirms sampled packages use package `com.mobilecreditcards` with manifest version names `11.29.0` through `14.3.0` and manifest versionCodes `123845` through `162034`.
- Sampled packages expose React Native evidence through `assets/index.android.bundle`, Hermes bytecode, and React Native native libraries including `libreactnativejni.so`, `libreactnative.so`, `libhermes.so`, `libjsi.so`, Fabric, TurboModule, and Yoga libraries.
- Rows `11.29.0` through `12.6.0` are RN `unknown` with low confidence because `ReactNativeVersion` appears without a renderer marker and is not specific enough for an Android Hermes RN band.
- Rows `12.10.1` through `14.3.0` infer RN `0.77.x` with medium confidence from `unstable_enableLogBox`, `DevMenu`, and absence of the RN 0.78 `experimental_LayoutConformance` marker.
- Uptodown source dates are non-monotonic against embedded manifest versionCode for the sampled rows, so Android boundaries are source-limited and not exact release-date transitions.
- Android reports: `reports/nerdwallet/android-versions.csv`, `reports/nerdwallet/android-versions.json`, `reports/nerdwallet/android-ranges.csv`, `reports/nerdwallet/android-ranges.json`, and `reports/nerdwallet/android-transitions.json`.

## Next Step

Move to the next candidate unless a better source for NerdWallet iOS history or a complete Android release catalog becomes available.
