# Artsy React Native Timeline

## Registration

- App name: Artsy: Buy & Sell Fine Art
- App Store ID: 703796080
- iOS bundle ID: net.artsy.artsy
- Android package: net.artsy.app
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Artsy --format json` returned App Store ID `703796080`, bundle ID `net.artsy.artsy`, app name `Artsy: Buy & Sell Fine Art`, and current listed version `9.9.0`.
- Apple iTunes lookup for App Store ID `703796080` returned app name `Artsy: Buy & Sell Fine Art`, seller `Art.sy Inc.`, bundle ID `net.artsy.artsy`, current US listed version `9.9.0`, and release date `2026-05-20T17:57:36Z`.
- App Store URL: `https://apps.apple.com/us/app/artsy-buy-sell-fine-art/id703796080`.
- Android package sources identify package `net.artsy.app`.
- APKPure Android history URL identified: `https://apkpure.net/artsy-buy-resell-artworks/net.artsy.app/versions` returned HTTP `200`.
- APKCombo old versions URL identified: `https://apkcombo.com/artsy-buy-sell-fine-art/net.artsy.app/old-versions/` returned HTTP `200`.
- Uptodown versions URL identified: `https://artsy.en.uptodown.com/android/versions?utm_source=main` returned HTTP `200`.
- AndroidAPKsFree guessed old versions URL for package `net.artsy.app` returned HTTP `404`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 703796080`.
- iOS external versions available: 292
- Oldest iOS external version ID: `23362671`
- Newest iOS external version ID: `885363722`
- Raw iOS version list: `reports/artsy/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `2026022618` (`9.0.1`)
- Newest Android versionCode in the APKPure catalog: `2026052012` (`9.9.0`)
- Raw Android version catalog: `reports/artsy/android-version-list.json`
- Source-specific APKPure catalog: `reports/artsy/android-version-list-apkpure.json`
- APKPure currently exposes a limited visible history on the fetched page.
- Android APKCombo fetch rejected decoded variant payloads that were not HTTP(S) URLs; error log: `reports/artsy/android-version-list-apkcombo-error.txt`

## Initial Sampling

- Android sampling downloaded and analyzed all 10 visible APKPure XAPK rows from versionCode `2026022618` (`9.0.1`) through `2026052012` (`9.9.0`).
- Android React Native markers were detected in every sampled row through Hermes/JSI/native-library metadata including `libreactnative.so`, `libjsi.so`, and `libhermes.so`.
- Android package hash validation found one unique XAPK payload across all 10 rows, and embedded manifest metadata reported versionName `9.9.0` and versionCode `2026052012` for every row. Treat these APKPure downloads as duplicated current-payload evidence, not historical builds.
- iOS sampling downloaded and analyzed 12 evenly spaced IPAs across external version IDs `23362671` through `885363722`.
- Broad iOS sample result: `1.0` through `7.2.0` remains RN unknown / not detected by current markers.
- Broad iOS sample result: `8.5.0` is RN `0.66.x` with medium confidence.
- Broad iOS sample result: `8.25.0` is RN `0.69.x-0.70.x` with medium confidence.
- Broad iOS sample result: `8.51.0` is RN `0.71.x` with medium confidence.
- Broad iOS sample result: `8.78.0` is RN `0.74.x-0.76.x` with medium confidence.
- Broad iOS sample result: `9.9.0` is RN `0.81.x` with high confidence from `react-native-renderer` `19.1.0`.

## Boundary Refinement

- iOS boundary refinement expanded the sample to 65 analyzed IPAs.
- Decrypted expansion shows `7.3.5` through `7.3.9` all carry native RN/JSI/Yoga markers without version markers. The previous adjacent external version ID before `7.3.5` is `848143484`, which is not currently present under `ipas/artsy`.
- The App Store version list confirms exact adjacent transitions with zero known-list gaps:
- `7.3.9` -> `8.0.0`: native RN marker without version -> RN `0.66.x`
- `8.9.0` -> `8.10.0`: RN `0.66.x` -> RN `0.67.x-0.68.x`
- `8.12.4` -> `8.12.5`: RN `0.67.x-0.68.x` -> RN `0.69.x-0.70.x`
- `8.27.0` -> `8.28.0`: RN `0.69.x-0.70.x` -> RN `0.71.x`
- `8.56.0` -> `8.57.0`: RN `0.71.x` -> RN `0.74.x-0.76.x`
- `8.79.0` -> `8.80.0`: RN `0.74.x-0.76.x` -> RN `0.77.x`
- `8.83.0` -> `8.84.0`: RN `0.77.x` -> RN `0.79.x`
- `8.88.0` -> `8.89.0`: RN `0.79.x` -> RN `0.81.x`

## Decrypted iOS Evidence

- Decrypted iOS dump date: 2026-05-26.
- Dump tooling: `./dump_ios_ipa.py <ipa> --method frida-ipa-extract --all-binaries`; the wrapper installed through `ideviceinstaller` and recorded device context from `ideviceinfo`.
- Device context for accepted dump: iOS `16.7.7` (`20H330`), hardware model `D201AP`.
- `7.3.5` build `2022.04.22.16`, external ID `848346625`: source IPA SHA-256 `a5ae6a3c724dc14fae73a138d37ae15494ff71a42e9ebedd6ef925c7784cb953`, dumped IPA SHA-256 `41377f3891a7b264bf00f26c3b1d07695a690d49da9d4ba1bafc50b01e24a991`, dumped size `29195325`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `7.3.6` build `2022.05.11.16`, external ID `848649414`: source IPA SHA-256 `00a508aa5f0d254a8cf4a5a19e207a98866dc69449ca078d1e84137bc36649fe`, dumped IPA SHA-256 `16107b185266d798364838e17be2a06bbd4aa952d51e362d43338e87e339a318`, dumped size `29293805`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `7.3.7` build `2022.05.25.17`, external ID `849466717`: source IPA SHA-256 `d2e6b884680488843e3b00c4d4585c657d26ec740f7b215683116c1a95269a3d`, dumped IPA SHA-256 `b02d92a2141481dc352037ff2225f8425620fa4c89aad764d7670482680a6414`, dumped size `29584678`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `7.3.8` build `2022.05.29.23`, external ID `849500699`: source IPA SHA-256 `fe61c02ceacc2087d0da5056b8c468be3a40dccaca0c5482d1f9be327f30886f`, dumped IPA SHA-256 `96adf49ce8b86840208d9f641e7d1be6304fa4d2e55c5e06b32cea0a6870ff78`, dumped size `29574496`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `7.3.9` build `2022.06.03.16`, external ID `849701554`: source IPA SHA-256 `ce50723e36748b9a3248437f89058be5265536e51aa26654a640c3e7596f11ce`, dumped IPA SHA-256 `b4e66b6ce0f99f9521a896b6f8dcaca388bb350d4e0c12a2f45a769b689c543d`, dumped size `28538122`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `7.3.5` through `7.3.9` decrypted analysis finds no JS bundle or renderer marker, but the decrypted main executable contains native React Native, JSI, and Yoga markers with no Hermes or version-specific RN marker. These rows remain RN `unknown` with reason `native_rn_marker_without_version`.
- The immediate previous App Store external ID before `7.3.5` is `848143484`; it was not present in the local Artsy IPA set during this pass, so the earliest decrypted native RN evidence is `7.3.5` until that adjacent build is obtained and decrypted.
- Remaining encrypted code in the pre-8.0.0 decrypted dumps is limited to app extensions: `ArtsyWidgetExtension` and `BrazePushServiceExtension` remain encrypted, and `Artsy Stickers` has no `LC_ENCRYPTION_INFO` cryptid.
- `9.9.0` build `2026.05.20.12.45`, external ID `885363722`: source IPA SHA-256 `214aa25fb7007d998370952a3fd5851aef5609f86c26bbcc755fbd739ed892e3`, dumped IPA SHA-256 `70657a0db10807135ca95f83b80e3bba655e3a5d5b028d8969caffa1a08c7a0e`, dumped size `49097699`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `9.9.0` decrypted analysis preserves RN `0.81.x` with high confidence from `react-native-renderer` `19.1.0` and exposes native React Native, Hermes, JSI, and Yoga markers in decrypted code.
- Remaining encrypted code in `9.9.0` is limited to app extensions: `ArtsyWidgetExtension` and `BrazePushServiceExtension` remain encrypted. No encrypted non-extension Mach-O remained in the accepted latest dump.

## Result

- Status: `needs_manual_review`
- Reason: the iOS App Store version list yielded exact adjacent version-specific RN marker-band boundaries from `8.0.0` onward, and the accepted decrypted latest dump confirms the current `0.81.x` band. Accepted decrypted pre-boundary dumps now show native RN/JSI/Yoga markers from `7.3.5` through `7.3.9` without a version marker, so `7.3.9` -> `8.0.0` is the first exact transition to a version-specific `0.66.x` marker rather than proof of RN introduction. The adjacent previous external ID `848143484` still needs acquisition/decryption to test whether native RN markers start earlier. Android APKPure downloads confirm current React Native usage but are not used for historical boundaries because they duplicated the latest payload for historical rows.
