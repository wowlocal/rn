# Coinbase React Native Timeline

## Registration

- App name: Coinbase
- App Store ID: 886427730
- iOS bundle ID: com.vilcsak.bitcoin2
- Android package: com.coinbase.android
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Coinbase --format json` returned App Store ID `886427730`, bundle ID `com.vilcsak.bitcoin2`, and current listed version `14.19.22`.
- Apple iTunes lookup for App Store ID `886427730` returned app name `Coinbase: Buy Crypto & Stocks`, seller `Coinbase, Inc.`, bundle ID `com.vilcsak.bitcoin2`, and current listed version `14.19.22`.
- App Store URL: `https://apps.apple.com/us/app/coinbase-buy-crypto-stocks/id886427730`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.coinbase.android`.
- Android package history source identified: APKPure page for package `com.coinbase.android`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 886427730 --format json`.
- iOS external version IDs available: 555
- Oldest iOS external version ID: `596373720`
- Newest iOS external version ID: `885921388`
- Raw iOS version catalog: `reports/coinbase/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 19
- Oldest Android versionCode in the APKPure catalog: `140100270` (`14.1.27`)
- Newest Android versionCode in the APKPure catalog: `141900220` (`14.19.22`)
- Raw Android version catalog: `reports/coinbase/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page; direct APKPure version pages expanded the parseable catalog through `14.1.27`.
- Direct APKPure page probing included `14.0.4`, but that page did not expose parseable download metadata.

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 19
- Android package source: APKPure visible catalog plus parseable APKPure direct version pages.
- Android RN markers detected: yes, in every sampled XAPK.
- Exposed Android JS bundle path: `assets/index.android.bundle`
- Exposed React Native native-library metadata includes `libreactnative.so`, `libhermes.so`, `libhermestooling.so`, `libjsi.so`, and `libreact_codegen_reactnativekeyboardcontroller.so`.
- Analyzer refinement: `check_android_rn_versions.py` now inspects large primary `index.android.bundle` files and recognizes Hermes string-table markers without requiring a `get ` prefix.
- Current Android RN inference: RN present but version `unknown`, low confidence. `ReactNativeVersion` is present without a `react-native-renderer` marker, which is not specific enough to infer a `0.82.x or newer` band.
- Android reports: `reports/coinbase/android-versions.csv`, `reports/coinbase/android-ranges.csv`, and empty `reports/coinbase/android-transitions.json`.

## iOS Sampling

- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 12
- iOS source sampling found marker bands from RN `0.63.x` in `9.21.4` through RN `0.79.x` in `13.44.24`, then an exact App Store-list marker boundary to RN `0.60.x` at `13.45.27`.
- Pre-boundary iOS build `13.44.24` build `13440024`, external ID `880184267`: source IPA SHA-256 `344e436ac8c03638239bb5cd382a99f575d8cba23ffe841c9cacad90a4a64569`, dumped IPA SHA-256 `1db95622680f368e44a08a1e753bf7f8f18ea961c3aa10d401d7e94b98e4dea3`, dumped size `103964481`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- Boundary iOS build `13.45.27` build `13450027`, external ID `880359975`: source IPA SHA-256 `7d0c8c2e93b35e08ba38937e71a3b543db89e78b9ab78f61cc9d7b2a8d1ca4da`, dumped IPA SHA-256 `37c6592ef4de0a48affb7420caef613196f5b67859073c7542e03ca9f7ad6019`, dumped size `104300009`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- Latest sampled iOS build `14.19.22` build `14190022`, external ID `885921388`: source IPA SHA-256 `42091f34e0830e46cab2e9aee34c642bc076d6274dbb5c3fadaa46cd58962237`, dumped IPA SHA-256 `630c465c4ec14fd8dd17fcfc8b7ae2a3b47406650c7d724e224a768223c75759`, dumped size `105486062`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- Decrypted iOS analysis for the accepted pre-boundary row preserves RN `0.79.x` with renderer `19.0.0`, Hermes bytecode version `96`, and native React Native/Hermes/JSI/Yoga markers in the decrypted main executable.
- Decrypted iOS analysis for both accepted `0.60.x` rows reports Hermes bytecode version `96`, RN `0.60.x` with medium confidence from JS markers, and native React Native/Hermes/JSI/Yoga markers in the decrypted main executable.
- Per-Mach-O inventory for each accepted decrypted dump: 19 Mach-Os total; main executable and 14 loaded frameworks decrypted; 4 app-extension executables remain encrypted. No encrypted non-extension executables remain, and extension attach was not pursued because the main app already exposes RN evidence.
- iOS reports: `reports/coinbase/versions.csv`, `reports/coinbase/ranges.csv`, and `reports/coinbase/transitions.json`.

## iOS Transitions

- `9.21.4` -> `12.23.13`: RN `0.63.x` -> RN `0.71.x`, source-limited gap.
- `12.23.13` -> `13.21.10`: RN `0.71.x` -> RN `0.74.x-0.76.x`, source-limited gap.
- `13.21.10` -> `13.26.10`: RN `0.74.x-0.76.x` -> RN `0.77.x`, source-limited gap.
- `13.31.19` -> `13.41.21`: RN `0.77.x` -> RN `0.79.x`, source-limited gap.
- `13.44.24` build `13440024`, external ID `880184267` -> `13.45.27` build `13450027`, external ID `880359975`: exact App Store-list adjacency, RN `0.79.x` -> RN `0.60.x`.

## Provisional Ranges

| Platform | RN guess | Renderer | Confidence | Start | End | Builds |
|---|---|---|---|---|---|---:|
| iOS | 0.63.x | 16.13.0 | medium | 9.21.4 (`92104`), external ID `842088805` | 9.21.4 (`92104`), external ID `842088805` | 1 |
| iOS | 0.71.x | unknown | medium | 12.23.13 (`12230013`), external ID `866714202` | 12.23.13 (`12230013`), external ID `866714202` | 1 |
| iOS | 0.74.x-0.76.x | unknown | medium | 13.21.10 (`13210010`), external ID `875546596` | 13.21.10 (`13210010`), external ID `875546596` | 1 |
| iOS | 0.77.x | unknown | medium | 13.26.10 (`13260010`), external ID `876490192` | 13.31.19 (`13310019`), external ID `877462419` | 2 |
| iOS | 0.79.x | 19.0.0 | medium | 13.41.21 (`13410021`), external ID `879565881` | 13.44.24 (`13440024`), external ID `880184267` | 3 |
| iOS | 0.60.x | unknown | medium | 13.45.27 (`13450027`), external ID `880359975` | 14.19.22 (`14190022`), external ID `885921388` | 4 |
| Android | unknown, RN native metadata present | low | 14.1.27 (`140100270`), APKPure date `2026-01-14` | 14.19.22 (`141900220`), APKPure date `2026-05-21` | 19 |

## Open Gaps

- APKPure remains sparse before `14.1.27`; missing older Android versions are source limitations, not evidence that those releases did not exist.
- No Android RN transition was observed in the accessible package window.
- The Android RN version remains unknown because the Hermes bundle exposes `ReactNativeVersion` but no local renderer-version marker.
- Earlier iOS transitions remain source-limited because only representative rows were sampled before the exact `13.44.24` -> `13.45.27` boundary.
- The exact `0.79.x` -> `0.60.x` marker change now has decrypted main-app evidence on both sides. It is still unusual and should be treated as a package-evidence finding that may reflect marker visibility or bundle packaging, not necessarily a deliberate RN downgrade, until stronger source or upstream release evidence explains it.
- Disk cleanup was not performed after Android sampling because `apks/coinbase` used about 5.0 GiB and the filesystem still had 219 GiB available.

## Next Step

Manual review should use a more complete Android package history and targeted older iOS IPAs if exact pre-`13.44.24` boundaries are needed. The exact `13.44.24` -> `13.45.27` iOS boundary is now verified with decrypted main-app evidence on both sides; if Android version detail is needed, add a stronger Android Hermes signature or renderer extraction before assigning a version band.
