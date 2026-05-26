# Walmart React Native Timeline

## Registration

- App name: Walmart: Shopping & Savings
- App Store ID: 338137227
- iOS bundle ID: com.walmart.electronics
- Android package: com.walmart.android
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Walmart --format json` did not return the consumer Walmart shopping app in the current localized results.
- Public App Store URL and Apple iTunes lookup for App Store ID `338137227` returned app name `Walmart: Shopping & Savings`, seller `Walmart`, bundle ID `com.walmart.electronics`, and current US listed version `26.19.2`.
- App Store URL: `https://apps.apple.com/us/app/walmart-shopping-savings/id338137227`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.walmart.android`.
- Android package sources identify package `com.walmart.android`.
- APKPure history page identified: `https://apkpure.net/walmart-shopping-savings/com.walmart.android/versions`.
- AndroidAPKsFree old versions page identified: `https://androidapks.com/walmart/com-walmart-android/old/`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 338137227`.
- iOS version list result: failed because App Store license is required.
- iOS bundle-ID retry and license attempt for `com.walmart.electronics` returned app not found.
- Raw iOS version-list error: `reports/walmart/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `26120216` (`26.12.2`)
- Newest Android versionCode in the APKPure catalog: `26180118` (`26.18.1`)
- AndroidAPKsFree catalog fetched on 2026-05-26 with `fetch_androidapksfree_versions.py`.
- Android entries available from AndroidAPKsFree sources: 47
- Oldest AndroidAPKsFree versionCode: `21055104` (`21.5.5`)
- Newest AndroidAPKsFree versionCode: `24240019` (`24.24`)
- Merged raw Android version catalog: `reports/walmart/android-version-list.json`
- Raw AndroidAPKsFree source catalog: `reports/walmart/androidapksfree-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 25
- Android package sources: APKPure visible catalog and AndroidAPKsFree visible catalog
- Android RN markers detected: yes, only in version 21.5.5 (`21055104`).
- Version 21.5.5 exposes React Native native-library metadata including Hermes, JSI, `libreactnativejni.so`, and `libyoga.so`; inferred RN band is `0.74.x-0.76.x` with medium confidence.
- Sampled Android packages from 21.22 (`21220106`) through 26.18.1 (`26180118`) did not expose RN JS bundle or native-library markers.
- Android reports: `reports/walmart/android-versions.csv`, `reports/walmart/android-ranges.csv`, `reports/walmart/android-transitions.json`, and source-specific `reports/walmart/androidapksfree-versions.csv`.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.74.x-0.76.x | medium | 21.5.5 (`21055104`) | 21.5.5 (`21055104`) | 1 |
| Android | unknown | unknown | 21.22 (`21220106`) | 26.18.1 (`26180118`) | 24 |

## Open Gaps

- The RN disappearance window is source-adjacent in AndroidAPKsFree, 21.5.5 -> 21.22, but not exact because AndroidAPKsFree is source-limited.
- iOS version-list access is blocked by App Store licensing/app lookup failures.
- APKPure only exposes the 2026 window, where sampled packages have no RN markers.
- Disk cleanup was not performed after sampling because `apks/walmart` used about 2.7 GiB, `apks/walmart-androidapksfree` used about 1.2 GiB, and the filesystem still had ample free space.

## Next Step

Manual review should use a more complete trusted Android package history or restored iOS access to confirm whether RN existed in missing Android versions before 21.5.5 and to verify the disappearance boundary.
