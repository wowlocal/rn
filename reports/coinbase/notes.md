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
- iOS IPAs downloaded and analyzed: 1
- Latest sampled iOS build `14.19.22` build `14190022`, external ID `885921388`: source IPA SHA-256 `42091f34e0830e46cab2e9aee34c642bc076d6274dbb5c3fadaa46cd58962237`, dumped IPA SHA-256 `630c465c4ec14fd8dd17fcfc8b7ae2a3b47406650c7d724e224a768223c75759`, dumped size `105486062`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `14.19.22` decrypted iOS analysis reports Hermes bytecode version `96`, RN `0.60.x` with medium confidence from JS markers, and native React Native/Hermes/JSI/Yoga markers in the decrypted main executable.
- Per-Mach-O inventory for `14.19.22`: 19 Mach-Os total; main executable and 14 loaded frameworks decrypted; 4 app-extension executables remain encrypted. No encrypted non-extension executables remain, and extension attach was not pursued because the main app already exposes RN evidence.
- iOS reports: `reports/coinbase/versions.csv`, `reports/coinbase/ranges.csv`, and `reports/coinbase/transitions.json`.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| iOS | 0.60.x | medium | 14.19.22 (`14190022`), external ID `885921388` | 14.19.22 (`14190022`), external ID `885921388` | 1 |
| Android | unknown, RN native metadata present | low | 14.1.27 (`140100270`), APKPure date `2026-01-14` | 14.19.22 (`141900220`), APKPure date `2026-05-21` | 19 |

## Open Gaps

- APKPure remains sparse before `14.1.27`; missing older Android versions are source limitations, not evidence that those releases did not exist.
- No Android RN transition was observed in the accessible package window.
- The Android RN version remains unknown because the Hermes bundle exposes `ReactNativeVersion` but no local renderer-version marker.
- iOS has only been sampled at the latest build, so iOS boundaries before `14.19.22` are not established.
- Disk cleanup was not performed after Android sampling because `apks/coinbase` used about 5.0 GiB and the filesystem still had 219 GiB available.

## Next Step

Manual review should use a more complete Android package history and targeted older iOS IPAs to determine whether an RN upgrade boundary exists before `14.1.27` / `14.19.22`. If Android version detail is needed, add a stronger Android Hermes signature or renderer extraction before assigning a version band.
