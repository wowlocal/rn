# SoundCloud React Native Timeline

## Registration

- App name: SoundCloud: The Music You Love
- App Store ID: 336353151
- iOS bundle ID: com.soundcloud.TouchApp
- Android package: com.soundcloud.android
- Status: not_react_native_detected
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
- All sampled IPA main executables are FairPlay encrypted, so native constants are not inspectable.
- iOS reports: `reports/soundcloud/versions.csv`, `reports/soundcloud/versions.json`, `reports/soundcloud/ranges.csv`, and `reports/soundcloud/timeline.json`.

## Result

Marked `not_react_native_detected` because no React Native markers were found in the broad iOS sample or the visible Android sample.
