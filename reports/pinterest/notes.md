# Pinterest React Native Timeline

## Registration

- App name: Pinterest
- App Store ID: 429047995
- iOS bundle ID: pinterest
- Android package: com.pinterest
- Status: initial_sampling
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Pinterest --format json` returned App Store ID `429047995`, bundle ID `pinterest`, and current listed version `14.19`.
- Apple iTunes lookup for App Store ID `429047995` returned app name `Pinterest`, seller `Pinterest, Inc.`, bundle ID `pinterest`, and current US listed version `14.19`.
- App Store URL: `https://apps.apple.com/us/app/pinterest/id429047995`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.pinterest`.
- Android package sources identify package `com.pinterest`.
- APKPure current app page identified: `https://apkpure.net/pinterest/com.pinterest`; its `/versions` route currently returns HTTP 410.
- APKMirror history page identified: `https://www.apkmirror.com/apk/pinterest/pinterest/`; automated fetches currently return a Cloudflare challenge.
- AndroidAPKsFree old versions page identified: `https://androidapks.com/pinterest/com-pinterest/old/` and exposes direct historical APK download rows.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 429047995`.
- iOS external version IDs available: 645
- Oldest iOS external version ID: `3572654`
- Newest iOS external version ID: `885829462`
- Raw iOS version list: `reports/pinterest/version-list.json`
- Android catalog fetched on 2026-05-26 with `fetch_androidapksfree_versions.py`.
- Android entries available from AndroidAPKsFree sources: 50
- Oldest Android versionCode in the catalog: `12188010` (`12.18.0`)
- Newest Android versionCode in the catalog: `14088010` (`14.8.0`)
- Raw Android version catalog: `reports/pinterest/android-version-list.json`
- AndroidAPKsFree `Updated` dates are preserved as source context but not treated as release dates for ordering.
- APKPure and APKMirror did not provide an automated parseable history at this step.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 12
- Android package source: AndroidAPKsFree visible catalog
- Android RN markers detected: no, not in sampled APKs from 12.18.0 (`12188010`) through 14.8.0 (`14088010`).
- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 11
- iOS RN markers detected: yes.
- iOS app versions 6.43 and 8.3.1 expose `Payload/Pinterest.app/ReactNative/Assets/main.jsbundle` and infer RN `<=0.59.x`.
- iOS app version 9.42 exposes `Payload/Pinterest.app/ReactNative/Assets/main.jsbundle` and infers RN `0.63.x`.
- iOS samples through 6.22 did not expose a JS bundle; iOS samples 12.8 and 14.19 also did not expose a JS bundle.
- Current reports: `reports/pinterest/ios-versions.csv`, `reports/pinterest/ranges.csv`, `reports/pinterest/transitions.json`, `reports/pinterest/android-versions.csv`, and `reports/pinterest/android-ranges.csv`.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| iOS | unknown | low | initial build (`1`) | 6.22 (`3`) | 6 |
| iOS | <=0.59.x | medium | 6.43 (`3`) | 8.3.1 (`6`) | 2 |
| iOS | 0.63.x | medium | 9.42 (`3`) | 9.42 (`3`) | 1 |
| iOS | unknown | low | 12.8 (`4`) | 14.19 (`2`) | 2 |
| Android | unknown | unknown | 12.18.0 (`12188010`) | 14.8.0 (`14088010`) | 12 |

## Open Gaps

- The iOS RN introduction window is still broad: 6.22 (`821390341`) to 6.43 (`825777860`).
- The iOS RN upgrade window from `<=0.59.x` to `0.63.x` is still broad: 8.3.1 (`834596156`) to 9.42 (`845855528`).
- The iOS RN bundle-disappearance window is still broad: 9.42 (`845855528`) to 12.8 (`864203388`).
- AndroidAPKsFree only covers 12.18.0 through 14.8.0 and did not expose the older Android window where RN may have been present.
- APKMirror likely has a richer Android history but automated fetches returned a Cloudflare challenge.
- Disk cleanup was not performed after initial sampling because `ipas/pinterest` used under 1 GiB, `apks/pinterest` used about 1.1 GiB, and the filesystem still had ample free space.

## Next Step

Continue iOS boundary refinement around the three broad RN transition windows. Use Android only if an older, trusted, parseable package source becomes available.
