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
- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 12
- iOS reports: `reports/shopify/versions.csv`, `reports/shopify/ranges.csv`, and `reports/shopify/transitions.json`.
- iOS RN markers detected: yes, in every sampled IPA through `Payload/Shopify.app/main.jsbundle`.
- iOS source IPAs expose Hermes bytecode and React Native JS markers. Sampled rows from `9.2523.0` through `10.2605.0` infer RN `0.79.x` with renderer `19.0.0`; sampled rows from `10.2606.0` through `10.2621.0` infer RN `0.82.x or newer` with low confidence because `ReactNativeVersion` is present but no renderer marker is exposed.

## Boundary Refinement

- Android catalog expansion added parseable APKPure direct pages back to `10.2543.0 (193814)`.
- APKPure direct pages for `10.2606.1` and `10.2607.1` narrowed the observed marker-change window to `10.2605.0 (220449)` -> `10.2606.1 (223088)`.
- Direct APKPure URLs for `10.2606.0`, `10.2607.0`, and older `10.2542.0` through `10.2538.0` did not expose parseable current download metadata with the existing catalog fetcher and were not used as evidence.
- Targeted iOS sampling resolved the same marker-change area exactly in the App Store external-version list: `10.2605.0 (220442)`, external ID `882018171`, RN `0.79.x` -> `10.2606.0 (222553)`, external ID `882242969`, RN `0.82.x or newer`.
- The iOS result contradicts the Android source-limited `0.60.x` inference after `10.2606.1`, so the Android post-boundary rows should be treated as marker/source-limited rather than a real app-wide RN downgrade.

## Decrypted iOS Evidence

- Latest sampled iOS build `10.2621.0` build `282789`, external ID `886020173`: source IPA SHA-256 `6c6d1900c8c3ff5e0a9fbfc557d9132ed42e9b1defd44772a2f8564eb580e72a`, dumped IPA SHA-256 `2551b069355a4e9168dfd959551ebc4fc31f99d904d1f0dbf2e4bd9083c62e07`, dumped size `97696350`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `main_only_decrypted`.
- `10.2621.0` decrypted analysis preserves the JS-bundle inference `0.82.x or newer`, Hermes bytecode version `98`, and native React Native/Hermes/JSI/Yoga markers in the decrypted main executable. No renderer or exact RN version marker was found.
- Per-Mach-O inventory for `10.2621.0`: 26 Mach-Os total; main executable and 14 loaded app/framework binaries decrypted; 11 executables remain encrypted. Remaining encrypted non-extension executables are limited to the bundled watch app and watch frameworks. Extension/watch attach was not pursued because the main app already exposes RN evidence and the unresolved version marker is in the main `main.jsbundle` inference path.

## iOS Ranges

| Platform | RN guess | Renderer | Confidence | Start | End | Builds |
|---|---|---|---|---|---|---:|
| iOS | 0.79.x | 19.0.0 | medium | 9.2523.0 (`138977`), external ID `875389859` | 10.2605.0 (`220442`), external ID `882018171` | 8 |
| iOS | 0.82.x or newer | unknown | low | 10.2606.0 (`222553`), external ID `882242969` | 10.2621.0 (`282789`), external ID `886020173` | 4 |

## Android Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.79.x | medium | 10.2543.0 (`193814`), APKPure date `2025-10-27` | 10.2605.0 (`220449`), APKPure date `2026-02-04` | 8 |
| Android | 0.60.x | medium | 10.2606.1 (`223088`), APKPure date `2026-02-11` | 10.2620.0 (`281050`), APKPure date `2026-05-21` | 16 |

## Open Gaps

- APKPure remains sparse before `10.2543.0`, and `10.2606.0` is not currently parseable through the APKPure direct-page fetcher.
- iOS sampling has not been extended before `9.2523.0`, so older Shopify RN adoption or earlier upgrade boundaries remain outside the current package window.
- The apparent Android transition from `0.79.x` to `0.60.x` conflicts with iOS evidence and is not trustworthy enough to report as a definitive app-wide RN downgrade. Treat it as a marker-visibility or source-gap boundary until stronger Android evidence is available.
- Exact RN patch versions are not recovered from the visible Android package markers; report Android bands with confidence.
- Exact RN patch versions are also not recovered from the latest iOS rows because no `react-native-renderer` marker is exposed after `10.2606.0`.
- Disk cleanup was not performed after Android sampling because `apks/shopify` used about 3.3 GiB and the filesystem still had 227 GiB available.

## Next Step

Manual review should use a complete, signature-verified Android source around `10.2605.0` -> `10.2606.1` to explain the Android/iOS marker conflict. If more Shopify depth is needed, sample older iOS rows before `9.2523.0` rather than broad-downloading the full 508-version history.
