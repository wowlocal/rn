# Shop React Native Timeline

## Registration

- App name: Shop
- App Store ID: 1223471316
- iOS bundle ID: com.jadedlabs.arrive
- Android package: com.shopify.arrive
- Status: needs_manual_review
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
- Android entries available from APKPure sources: 27
- Oldest Android versionCode in the APKPure catalog: `3319531` (`2.231.0`)
- Newest Android versionCode in the APKPure catalog: `3451748` (`2.253.0`)
- Raw Android version catalog: `reports/shop/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page; direct APKPure version pages expanded the parseable catalog through `2.231.0`.
- Direct APKPure page probing included `2.212.0`, but that page did not expose parseable download metadata.

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

## Source-Limited Boundary Refinement

- Android boundary refinement date: 2026-05-26
- Android packages downloaded and analyzed after refinement: 27
- Android package source: APKPure visible catalog plus parseable APKPure direct version pages.
- All 27 sampled XAPKs expose `assets/index.android.bundle` and React Native native-library metadata including `libreactnative.so`.
- The current analyzer reports a source-limited Android transition from `2.239.0` (`3372633`, APKPure date `2026-02-11`) to `2.240.0` (`3376891`, APKPure date `2026-02-19`).
- Treat this transition as source-limited rather than exact because APKPure does not demonstrate a complete package history before or around the sampled window.
- Android reports after refinement: `reports/shop/android-versions.csv`, `reports/shop/android-ranges.csv`, `reports/shop/android-transitions.csv`, and `reports/shop/android-transitions.json`.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.79.x | medium | 2.231.0 (`3319531`), APKPure date `2025-11-12` | 2.239.0 (`3372633`), APKPure date `2026-02-11` | 11 |
| Android | 0.81.x | high | 2.240.0 (`3376891`), APKPure date `2026-02-19` | 2.253.0 (`3451748`), APKPure date `2026-05-20` | 16 |

## Open Gaps

- APKPure remains sparse before `2.231.0`; missing older Android versions are source limitations, not evidence that those releases did not exist.
- iOS version-list access remains blocked by App Store license/app-not-found failures, so no iOS cross-check is available.
- Disk cleanup was not performed after Android sampling because `apks/shop` used about 3.1 GiB and the filesystem still had 224 GiB available.

## Next Step

Manual review should use a complete or signature-verified Android source to confirm whether `2.239.0` and `2.240.0` are truly adjacent around the RN upgrade, then sample targeted iOS builds only if iOS access becomes available.
