# Meta Horizon React Native Timeline

## Registration

- App name: Meta Horizon
- App Store ID: 1366478176
- iOS bundle ID: com.oculus.twilight
- Android package: com.oculus.twilight
- Status: sampled
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md` as Meta Quest / Oculus / Horizon-related app.
- `ipatool search "Meta Horizon" --format json` resolved App Store ID `1366478176`, bundle ID `com.oculus.twilight`, and current listed iOS version `372.1`.
- App Store URL: `https://apps.apple.com/us/app/meta-horizon/id1366478176`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.oculus.twilight`.
- Android package history sources identified: APKMirror and APKPure pages for package `com.oculus.twilight`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `1366478176` and bundle ID `com.oculus.twilight`.
- iOS version list result: failed because `ipatool` reports `license is required`.
- iOS license attempt: `ipatool purchase --bundle-identifier com.oculus.twilight --format json` failed with `unsupported protocol scheme ""`.
- Raw iOS version-list error: `reports/meta-horizon/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `930594021` (`366.0.0.24.290`)
- Newest Android versionCode in the APKPure catalog: `975394013` (`372.0.1.34.252`)
- Raw Android version catalog: `reports/meta-horizon/android-version-list.json`
- APKMirror was identified as a potentially richer Android history source, but automated fetches returned a Cloudflare challenge. APKPure is usable but currently exposes a limited visible history on the fetched page.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Android package source: APKPure visible version catalog
- Android RN markers detected: yes, in every sampled APK.
- Exposed Android JS bundle path: `assets/TwilightBundle.js.hbc`
- Exposed React Native native-library metadata includes `libreactnative.so`, `libxplat_ReactNative_turbomodules_libsodium_libsodiumAndroid.so`, `libxplat_oculus_turbomodules_msysinstaller_MsysInstallerModuleAndroid.so`, and `libxplat_oculus_twilight_MsysJSIAndroid.so`.
- Android reports: `reports/meta-horizon/android-versions.csv`, `reports/meta-horizon/android-ranges.csv`, and empty `reports/meta-horizon/android-transitions.json`.
- iOS sampling was not performed because the iOS version list is blocked by the App Store license failure recorded above.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | <=0.59.x | medium | 366.0.0.24.290 (`930594021`), APKPure date `2026-04-08` | 372.0.1.34.252 (`975394013`), APKPure date `2026-05-20` | 10 |

## Open Gaps

- APKPure currently exposes only recent 2026 builds from `366.0.0.24.290` through `372.0.1.34.252`.
- APKMirror search results indicate older Meta Horizon/Meta Quest packages exist, but automated fetches returned a Cloudflare challenge.
- Exact RN patch versions are not recovered from the visible Android package markers; report the `<=0.59.x` band with medium confidence.
- Disk cleanup was not performed after initial sampling because `apks/meta-horizon` used about 766 MiB and the filesystem still had 232 GiB available.

## Next Step

Use a trusted APKMirror or other signature-verified source to fetch older Android packages, or mark the app as source-limited if no richer source is accessible.
