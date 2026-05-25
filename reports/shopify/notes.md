# Shopify React Native Timeline

## Registration

- App name: Shopify
- App Store ID: 371294472
- iOS bundle ID: com.jadedpixel.shopify
- Android package: com.shopify.mobile
- Status: sampled
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search "Shopify" --format json` resolved App Store ID `371294472`, bundle ID `com.jadedpixel.shopify`, and current listed iOS version `10.2621.0`.
- App Store URL: `https://apps.apple.com/us/app/shopify-your-ecommerce-store/id371294472`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.shopify.mobile`.
- Android package history source identified: APKPure page for package `com.shopify.mobile`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions` through `check_rn_versions.py --list-versions-only`.
- iOS external version IDs available: 508
- Oldest iOS external version ID: `821337490`
- Newest iOS external version ID: `886020173`
- Raw iOS version list: `reports/shopify/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `237419` (`10.2611.0`)
- Newest Android versionCode in the APKPure catalog: `281050` (`10.2620.0`)
- Raw Android version catalog: `reports/shopify/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Android package source: APKPure visible version catalog
- Android RN markers detected: yes, in every sampled XAPK.
- Exposed Android JS bundle path: `assets/index.android.bundle`
- Exposed React Native native-library metadata includes `libreactnative.so`, `libhermesvm.so`, `libhermestooling.so`, and `libjsi.so`.
- Android reports: `reports/shopify/android-versions.csv`, `reports/shopify/android-ranges.csv`, and empty `reports/shopify/android-transitions.json`.
- iOS sampling was not performed because Android confirmed React Native markers and the Android source limitation should be resolved first.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.60.x | medium | 10.2611.0 (`237419`), APKPure date `2026-03-18` | 10.2620.0 (`281050`), APKPure date `2026-05-21` | 10 |

## Open Gaps

- APKPure currently exposes only recent 2026 builds from `10.2611.0` through `10.2620.0`.
- Exact RN patch versions are not recovered from the visible Android package markers; report the `0.60.x` band with medium confidence.
- Disk cleanup was not performed after initial sampling because `apks/shopify` used about 1.5 GiB and the filesystem still had 229 GiB available.

## Next Step

Refine Android history if older APKPure direct pages or another signature-verified source can be accessed, then sample targeted iOS builds only if Android evidence suggests an iOS boundary worth checking.
