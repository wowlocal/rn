# Shop React Native Timeline

## Registration

- App name: Shop
- App Store ID: 1223471316
- iOS bundle ID: com.jadedlabs.arrive
- Android package: com.shopify.arrive
- Status: sampled
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- Apple iTunes lookup for App Store ID `1223471316` resolved bundle ID `com.jadedlabs.arrive`, app name `Shop: All your favorite brands`, and current listed iOS version `2.253.0`.
- App Store URL: `https://apps.apple.com/us/app/shop-all-your-favorite-brands/id1223471316`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.shopify.arrive`.
- Android package history source identified: APKPure page for package `com.shopify.arrive`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `1223471316` and bundle ID `com.jadedlabs.arrive`.
- iOS version list result: failed because app ID lookup reports `license is required`, while bundle-ID lookup reports `app not found`.
- iOS license attempt: `ipatool purchase --bundle-identifier com.jadedlabs.arrive --format json` failed with `app not found`.
- Raw iOS version-list error: `reports/shop/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `3409799` (`2.246.0`)
- Newest Android versionCode in the APKPure catalog: `3451748` (`2.253.0`)
- Raw Android version catalog: `reports/shop/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Android package source: APKPure visible version catalog
- Android RN markers detected: yes, in every sampled XAPK.
- Exposed Android JS bundle path: `assets/index.android.bundle`
- Exposed renderer marker: `react-native-renderer 19.1.0`
- Exposed React Native native-library metadata includes `libreactnative.so`, `libhermes.so`, `libhermestooling.so`, and `libjsi.so`.
- Android reports: `reports/shop/android-versions.csv`, `reports/shop/android-ranges.csv`, and empty `reports/shop/android-transitions.json`.
- iOS sampling was not performed because iOS version-list access is blocked and Android packages exposed high-confidence RN markers.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.81.x | high | 2.246.0 (`3409799`), APKPure date `2026-03-31` | 2.253.0 (`3451748`), APKPure date `2026-05-20` | 10 |

## Open Gaps

- APKPure currently exposes only recent 2026 builds from `2.246.0` through `2.253.0`.
- iOS version-list access remains blocked by App Store license/app-not-found failures, so no iOS cross-check is available.
- Disk cleanup was not performed after Android sampling because `apks/shop` used about 1.3 GiB and the filesystem still had 226 GiB available.

## Next Step

Refine Android history if older APKPure direct pages or another signature-verified source can be accessed, then sample targeted iOS builds only if iOS access becomes available.
