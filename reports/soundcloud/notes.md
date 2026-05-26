# SoundCloud React Native Timeline

## Registration

- App name: SoundCloud: The Music You Love
- App Store ID: 336353151
- iOS bundle ID: com.soundcloud.TouchApp
- Android package: com.soundcloud.android
- Status: version_list_fetched
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

## Next Step

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

## Next Step

Sample the visible Android APKPure catalog first because Android packages should expose RN markers more directly if present.
