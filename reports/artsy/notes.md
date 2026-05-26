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
- `7.3.9` build `2022.06.03.16`, external ID `849701554`: source IPA SHA-256 `ce50723e36748b9a3248437f89058be5265536e51aa26654a640c3e7596f11ce`, dumped IPA SHA-256 `b4e66b6ce0f99f9521a896b6f8dcaca388bb350d4e0c12a2f45a769b689c543d`, dumped size `28538122`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `7.3.9` decrypted analysis finds no JS bundle or renderer marker, but the decrypted main executable contains native React Native, JSI, and Yoga markers with no version-specific RN marker. The row remains RN `unknown` with reason `native_rn_marker_without_version`.
- Remaining encrypted code in `7.3.9` is limited to app extensions: `ArtsyWidgetExtension` and `BrazePushServiceExtension` remain encrypted, and `Artsy Stickers` has no `LC_ENCRYPTION_INFO` cryptid.

## Result

- Status: `needs_manual_review`
- Reason: the iOS App Store version list yielded exact adjacent version-specific RN marker-band boundaries from `8.0.0` onward, but the accepted decrypted `7.3.9` boundary dump shows native RN/JSI/Yoga markers without a version marker. Android APKPure downloads confirm current React Native usage but are not used for historical boundaries because they duplicated the latest payload for historical rows.
