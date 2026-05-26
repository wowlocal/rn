# SoundCloud React Native Timeline

## Registration

- App name: SoundCloud: The Music You Love
- App Store ID: 336353151
- iOS bundle ID: com.soundcloud.TouchApp
- Android package: com.soundcloud.android
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search SoundCloud --format json` returned App Store ID `336353151`, bundle ID `com.soundcloud.TouchApp`, localized app name `SoundCloud - музыка и звук`, and current listed version `8.61.0`.
- Apple iTunes lookup for App Store ID `336353151` returned app name `SoundCloud: The Music You Love`, seller `SoundCloud Global Limited & Co KG`, bundle ID `com.soundcloud.TouchApp`, current US listed version `8.61.0`, and release date `2026-05-18T15:50:45Z`.
- App Store URL: `https://apps.apple.com/us/app/soundcloud-the-music-you-love/id336353151`.
- Android package sources identify package `com.soundcloud.android`.
- APKPure Android history URL identified: `https://apkpure.net/sound-cloud-android-app/com.soundcloud.android/versions`.
- APKPure `.com` versions URL returned HTTP `403`, but the APKPure `.net` versions URL returned HTTP `200`.
- AndroidAPKsFree guessed old versions URL for package `com.soundcloud.android` returned HTTP `404`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 336353151`.
- iOS external version IDs available: 645
- Oldest iOS external version ID: `2053200`
- Newest iOS external version ID: `885918024`
- Raw iOS version list: `reports/soundcloud/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `348060` (`2026.03.27-release`)
- Newest Android versionCode in the APKPure catalog: `355060` (`2026.05.15-release`)
- Raw Android version catalog: `reports/soundcloud/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Unique package SHA-256 hashes: 1
- Android package source: APKPure visible catalog.
- Android RN markers detected: no.
- Package hash validation found all 10 downloaded XAPK rows share the same SHA-256 (`1d93f3f92ae6...`), so APKPure appears to be returning duplicated current-package payloads for historical rows.
- Android reports: `reports/soundcloud/android-versions.csv`, `reports/soundcloud/android-ranges.csv`, and `reports/soundcloud/android-transitions.json`.

## Initial iOS Sampling

- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 12
- Unique app builds analyzed: 12
- Sample strategy: 12 evenly spaced external version IDs from the 645-entry App Store version list, including oldest and newest available IDs.
- Sampled external version IDs: `2053200`, `646142647`, `821175753`, `830033295`, `836339520`, `844786541`, `854554263`, `860769428`, `867031169`, `873297043`, `878206270`, `885918024`.
- Sampled app versions: `1.0`, `3.1.0`, `5.1.0`, `5.47.0`, `5.97.0`, `5.149.0`, `6.15.1`, `7.16.0`, `7.44.0`, `8.5.0`, `8.32.0`, `8.62.0`.
- No sampled IPA contained a JS bundle, Hermes bytecode, or React Native-related filenames such as `ReactNative`, `react-native`, `Hermes`, `JSI`, `Yoga`, `.jsbundle`, or `.hbc`.
- Source IPA main executables are FairPlay encrypted, so native constants are not inspectable without install-and-dump evidence.
- iOS reports: `reports/soundcloud/versions.csv`, `reports/soundcloud/versions.json`, `reports/soundcloud/ranges.csv`, and `reports/soundcloud/timeline.json`.

## Decrypted iOS Evidence

- Decrypted iOS dump date: 2026-05-26.
- Dump tooling: `./dump_ios_ipa.py <ipa> --method frida-ipa-extract --all-binaries`; the wrapper installed through `ideviceinstaller` and recorded device context from `ideviceinfo`.
- Device context for accepted dumps: iOS `16.7.7` (`20H330`), hardware model `D201AP`.
- `7.44.0` build `1248257`, external ID `867031169`: source IPA SHA-256 `5b150e725c4720bdab390e40d7c9e80bfd194c3de924b75eef0caab3e330e1cd`, dumped IPA SHA-256 `5fb5569546388ffb83c4e1da21656d60d6721f35c00ff09fdfdfe7fdd90b5cfd`, dumped size `155338831`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `main_only_decrypted`.
- `8.5.0` build `1251600`, external ID `873297043`: source IPA SHA-256 `1d4356c110841b36957cc4c7073ab9fb4638dfcb9abb48467a9a63cece0e52e6`, dumped IPA SHA-256 `9cf85a00792e4329d6f7cc5a01cb6ca7ad9fdd0e93521e8bb3ea9478908190f0`, dumped size `131693998`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `main_only_decrypted`.
- `8.32.0` build `1254310`, external ID `878206270`: source IPA SHA-256 `44c4f99ec67602e69e44a95fb36106952ee5994772da1e33585439ce9edea4b5`, dumped IPA SHA-256 `92906b5526add6a009cdfd7d4ef54e3b711b5dc877e71598224347bb0d08ef8e`, dumped size `135160679`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `main_only_decrypted`.
- Latest sampled `8.62.0` build `1259079`, external ID `885918024`: source IPA SHA-256 `1206f887e06b98ae137bd0c75a6953d5bfe299f8a18567ae2d575f95f128f4b9`, dumped IPA SHA-256 `343239acbacbfc891f0dc9bc9d8def5814a697f96f5ac42f7256e360b519b999`, dumped size `129522844`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `main_only_decrypted`.
- Decrypted analysis for `7.44.0`, `8.5.0`, `8.32.0`, and `8.62.0` finds no JS bundle, Hermes bytecode, renderer marker, native Hermes marker, or native Yoga marker. The decrypted main executable contains a native React Native marker in all four dumps; `7.44.0`, `8.5.0`, and `8.32.0` also expose native JSI markers. The rows remain RN `unknown` with reason `native_rn_marker_without_version`.
- Remaining encrypted non-extension code is limited to Watch app binaries such as `Payload/SoundCloud.app/Watch/SCWatch.app/Frameworks/SwiftSoundCloud.framework/SwiftSoundCloud`, `Payload/SoundCloud.app/Watch/SCWatch.app/Frameworks/Atomics.framework/Atomics` in `8.32.0`, and `Payload/SoundCloud.app/Watch/SCWatch.app/SCWatch`. App extensions also remain encrypted.

## Result

Marked `needs_manual_review` because accepted decrypted iOS dumps confirm native React Native markers from `7.44.0` through `8.62.0`, but no JS bundle, renderer marker, or version-specific RN marker is recoverable. Visible Android samples remain duplicated current-package payloads with no RN markers. If more iOS work is needed, the next targeted older probe is `7.16.0` (external ID `860769428`), not a broad history dump.
