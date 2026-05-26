# Pinterest React Native Timeline

## Registration

- App name: Pinterest
- App Store ID: 429047995
- iOS bundle ID: pinterest
- Android package: com.pinterest
- Status: done
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
- Public RN usage source: Pinterest Engineering's `Supporting React Native at Pinterest` article (`https://medium.com/pinterest-engineering/supporting-react-native-at-pinterest-f8c2233f90e6`) says Pinterest supported RN in the native iOS and Android apps and shipped the RN Topic Picker to 100%.

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

## Sampling And Refinement

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 12
- Android package source: AndroidAPKsFree visible catalog
- Android RN markers detected: no, not in sampled APKs from 12.18.0 (`12188010`) through 14.8.0 (`14088010`).
- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 50
- iOS RN markers detected: yes.
- iOS RN bundle path: `Payload/Pinterest.app/ReactNative/Assets/main.jsbundle`.
- Boundary refinement reached exact App Store adjacency for all observed iOS RN changes.
- Current reports: `reports/pinterest/ios-versions.csv`, `reports/pinterest/ranges.csv`, `reports/pinterest/transitions.json`, `reports/pinterest/android-versions.csv`, and `reports/pinterest/android-ranges.csv`.

## Final Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| iOS | unknown | low | initial build (`1`) | 6.36.1 (`1`) | 10 |
| iOS | <=0.59.x | medium | 6.37 (`4`) | 8.12.1 (`4`) | 10 |
| iOS | 0.60.x | medium | 8.13 (`4`) | 8.17 (`3`) | 5 |
| iOS | 0.61.x | medium | 8.18 (`3`) | 8.26 (`4`) | 5 |
| iOS | 0.63.x | medium | 8.27 (`4`) | 10.40 (`2`) | 16 |
| iOS | unknown | low | 10.41 (`2`) | 14.19 (`2`) | 4 |
| Android | unknown | unknown | 12.18.0 (`12188010`) | 14.8.0 (`14088010`) | 12 |

## Exact iOS Transitions

- unknown -> `<=0.59.x`: 6.36.1 (`823969700`) -> 6.37 (`824087289`)
- `<=0.59.x` -> `0.60.x`: 8.12.1 (`835482395`) -> 8.13 (`835496563`)
- `0.60.x` -> `0.61.x`: 8.17 (`835859903`) -> 8.18 (`836059322`)
- `0.61.x` -> `0.63.x`: 8.26 (`836781122`) -> 8.27 (`837241595`)
- `0.63.x` -> unknown: 10.40 (`853081184`) -> 10.41 (`853214823`)

## Residual Notes

- AndroidAPKsFree only covers 12.18.0 through 14.8.0 and did not expose the older Android window where RN may have been present.
- APKMirror likely has a richer Android history but automated fetches returned a Cloudflare challenge.
- Disk cleanup was not performed after refinement because `ipas/pinterest` used about 4.7 GiB, `apks/pinterest` used about 1.1 GiB, and the filesystem still had about 209 GiB available.

## Next Step

Move to the next candidate app. Revisit Android only if an older, trusted, parseable package source becomes available.
