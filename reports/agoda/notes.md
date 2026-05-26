# Agoda React Native Timeline

## Registration

- App name: Agoda: Cheap Flights & Hotels
- App Store ID: 440676901
- iOS bundle ID: com.agoda.consumer
- Android package: com.agoda.mobile.consumer
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- User-provided App Store URL: `https://apps.apple.com/ru/app/agoda-%D0%BE%D1%82%D0%B5%D0%BB%D0%B8-%D0%B8-%D0%B0%D0%B2%D0%B8%D0%B0%D0%B1%D0%B8%D0%BB%D0%B5%D1%82%D1%8B/id440676901`.
- Apple iTunes lookup for App Store ID `440676901` returned seller `Agoda Company Pte. Ltd.`, bundle ID `com.agoda.consumer`, and current listed version `14.19.0`.
- Google Play identifies Android package `com.agoda.mobile.consumer`.
- APKPure and AndroidAPKsFree also identify Android package `com.agoda.mobile.consumer`.
- APKPure history URL identified: `https://apkpure.net/agoda-cheap-flights-hotels/com.agoda.mobile.consumer/versions`.
- AndroidAPKsFree old versions URL identified: `https://androidapks.com/agoda/com-agoda-mobile-consumer/old/`.

## Version Lists

- iOS version list attempted on 2026-05-26 with `ipatool list-versions --app-id 440676901`.
- Bundle-ID iOS version list retry for `com.agoda.consumer` also failed.
- iOS version list result: failed with repeated Apple TLS handshake timeouts.
- Raw iOS version-list error: `reports/agoda/version-list-error.json`.
- APKPure catalog fetch returned a bot-cookie challenge for simple automated fetches; APKCombo returned HTTP `403`.
- AndroidAPKsFree catalog fetched on 2026-05-26 with `fetch_androidapksfree_versions.py`.
- Android entries available from AndroidAPKsFree sources: 35.
- Oldest AndroidAPKsFree versionCode: `82521` (`9.27.0`).
- Newest AndroidAPKsFree versionCode: `288069` (`12.18.0`).
- Raw Android version catalog: `reports/agoda/android-version-list.json`.
- Source-specific AndroidAPKsFree catalog: `reports/agoda/androidapksfree-version-list.json`.

## Android Sampling

- Android sampling date: 2026-05-26.
- Android packages downloaded and analyzed: 12.
- Android package source: AndroidAPKsFree visible old-version catalog.
- Sampled range: `9.27.0` (`82521`) through `12.18.0` (`288069`).
- Android RN markers detected: no.
- No sampled APK exposed React Native JS bundle paths, Hermes bytecode, React Native native libraries, or RN native metadata markers.
- Android reports: `reports/agoda/android-versions.csv`, `reports/agoda/android-ranges.csv`, `reports/agoda/android-transitions.json`, and source-specific `reports/agoda/androidapksfree-versions.csv`.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | unknown | unknown | 9.27.0 (`82521`) | 12.18.0 (`288069`) | 12 |

## Open Gaps

- AndroidAPKsFree is source-limited and stale for this app; it stops at May 2024, while Google Play/App Store show newer 2026 releases.
- APKPure web metadata exposes newer packages, but direct automated package downloads were blocked by Cloudflare during this run.
- iOS App Store historical version access is blocked by `ipatool` TLS handshake timeouts.

## Next Step

Revisit with restored iOS `ipatool` access or a downloadable current Android source before marking Agoda as `not_react_native_detected`.
