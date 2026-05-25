# Meta Horizon React Native Timeline

## Registration

- App name: Meta Horizon
- App Store ID: 1366478176
- iOS bundle ID: com.oculus.twilight
- Android package: com.oculus.twilight
- Status: needs_manual_review
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
- Android entries available from APKPure sources after direct-page expansion: 30
- Oldest Android versionCode in the APKPure catalog: `651148422` (`287.3.0.33.109`)
- Newest Android versionCode in the APKPure catalog: `975394013` (`372.0.1.34.252`)
- Raw Android version catalog: `reports/meta-horizon/android-version-list.json`
- APKMirror was identified as a potentially richer Android history source, but automated fetches returned a Cloudflare challenge. APKPure is usable but currently exposes a limited visible history on the fetched page.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 30
- Android package source: APKPure visible version catalog plus parseable APKPure direct download pages
- Android RN markers detected: yes, in every sampled APK.
- Exposed Android JS bundle path: `assets/TwilightBundle.js.hbc`
- Exposed React Native native-library metadata includes `libreactnative.so`, `libxplat_ReactNative_turbomodules_libsodium_libsodiumAndroid.so`, `libxplat_oculus_turbomodules_msysinstaller_MsysInstallerModuleAndroid.so`, and `libxplat_oculus_twilight_MsysJSIAndroid.so`.
- Android reports: `reports/meta-horizon/android-versions.csv`, `reports/meta-horizon/android-ranges.csv`, and `reports/meta-horizon/android-transitions.json`.
- iOS sampling was not performed because the iOS version list is blocked by the App Store license failure recorded above.

## Boundary Refinement

- Android catalog expansion added parseable APKPure direct pages back to `287.3.0.33.109 (651148422)`.
- Direct APKPure URLs discovered for some versions in search snippets, including `323.0.0.18.109`, `327.0.0.18.108`, `338.0.0.22.109`, `340.0.0.19.107`, and `357.0.1.30.337`, did not expose parseable current APKPure download metadata with the existing catalog fetcher and were not used as evidence.
- APKMirror search results indicate richer Android history, but automated fetches returned a Cloudflare challenge.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.78.x | high | 287.3.0.33.109 (`651148422`), APKPure date `2024-10-12` | 287.3.0.33.109 (`651148422`), APKPure date `2024-10-12` | 1 |
| Android | 0.60.x | medium | 341.0.0.17.107 (`806319963`), APKPure date `2025-10-15` | 349.2.0.46.104 (`844730700`), APKPure date `2025-12-16` | 11 |
| Android | <=0.59.x | medium | 360.0.0.23.322 (`892081967`), APKPure date `2026-03-04` | 372.0.1.34.252 (`975394013`), APKPure date `2026-05-20` | 18 |

## Open Gaps

- APKPure remains sparse: the first observed gap is `287.3.0.33.109 (651148422)` to `341.0.0.17.107 (806319963)`, and the second is `349.2.0.46.104 (844730700)` to `360.0.0.23.322 (892081967)`.
- The apparent Android transition from `0.60.x` to `<=0.59.x` is not trustworthy enough to report as a definitive app-wide RN downgrade. Treat it as a marker-visibility or source-gap boundary until stronger evidence is available.
- Exact RN patch versions are not recovered from the visible Android package markers except for the `0.78.x` high-confidence renderer marker in `287.3.0.33.109`.
- iOS version-list access remains blocked by App Store license failure, so no iOS cross-check is available.
- Disk cleanup was not performed after Android sampling because `apks/meta-horizon` used about 2.4 GiB and the filesystem still had more than 230 GiB available.

## Next Step

Manual review is needed to access trusted APKMirror or another signature-verified source for missing Android builds around the two source-limited gaps. Until then, move to the next candidate app.
