# Shopify React Native Timeline

## Registration

- App name: Shopify
- App Store ID: 371294472
- iOS bundle ID: com.jadedpixel.shopify
- Android package: com.shopify.mobile
- Status: needs_manual_review
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
- Android entries available from APKPure sources after direct-page expansion: 24
- Oldest Android versionCode in the APKPure catalog: `193814` (`10.2543.0`)
- Newest Android versionCode in the APKPure catalog: `281050` (`10.2620.0`)
- Raw Android version catalog: `reports/shopify/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 24
- Android package source: APKPure visible version catalog plus parseable APKPure direct download pages
- Android RN markers detected: yes, in every sampled XAPK.
- Exposed Android JS bundle path: `assets/index.android.bundle`
- Exposed React Native native-library metadata includes `libreactnative.so`, `libhermesvm.so`, `libhermestooling.so`, and `libjsi.so`.
- Android reports: `reports/shopify/android-versions.csv`, `reports/shopify/android-ranges.csv`, and `reports/shopify/android-transitions.json`.
- iOS sampling was not performed because Android confirmed React Native markers and the Android source limitation should be resolved first.

## Boundary Refinement

- Android catalog expansion added parseable APKPure direct pages back to `10.2543.0 (193814)`.
- APKPure direct pages for `10.2606.1` and `10.2607.1` narrowed the observed marker-change window to `10.2605.0 (220449)` -> `10.2606.1 (223088)`.
- Direct APKPure URLs for `10.2606.0`, `10.2607.0`, and older `10.2542.0` through `10.2538.0` did not expose parseable current download metadata with the existing catalog fetcher and were not used as evidence.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.79.x | medium | 10.2543.0 (`193814`), APKPure date `2025-10-27` | 10.2605.0 (`220449`), APKPure date `2026-02-04` | 8 |
| Android | 0.60.x | medium | 10.2606.1 (`223088`), APKPure date `2026-02-11` | 10.2620.0 (`281050`), APKPure date `2026-05-21` | 16 |

## Open Gaps

- APKPure remains sparse before `10.2543.0`, and `10.2606.0` is not currently parseable through the APKPure direct-page fetcher.
- The apparent Android transition from `0.79.x` to `0.60.x` is not trustworthy enough to report as a definitive app-wide RN downgrade. Treat it as a marker-visibility or source-gap boundary until stronger evidence is available.
- Exact RN patch versions are not recovered from the visible Android package markers; report Android bands with confidence.
- iOS version-list metadata exists, but iOS packages were not sampled because Android source limitations need resolution first.
- Disk cleanup was not performed after Android sampling because `apks/shopify` used about 3.3 GiB and the filesystem still had 227 GiB available.

## Next Step

Manual review is needed to access a complete, signature-verified Android source around `10.2605.0` -> `10.2606.1` and older versions before treating the marker change as a reliable app-wide RN timeline. Until then, move to the next candidate app.
