# Bloomberg React Native Timeline

## Registration

- App name: Bloomberg: Business News Daily
- App Store ID: 281941097
- iOS bundle ID: com.bloomberg.Bloomberg
- Android package: com.bloomberg.android.plus
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Bloomberg --format json` did not return the official Bloomberg consumer news app in the current localized results.
- Public App Store URL and Apple iTunes lookup for App Store ID `281941097` returned app name `Bloomberg: Business News Daily`, seller `Bloomberg Finance LP`, bundle ID `com.bloomberg.Bloomberg`, current US listed version `6.58.1`, and release date `2026-05-16T18:11:31Z`.
- App Store URL: `https://apps.apple.com/us/app/bloomberg-business-news-daily/id281941097`.
- Android package sources identify package `com.bloomberg.android.plus`.
- Aiting Android history URL identified: `https://www.aiting.com/bloomberg/com.bloomberg.android.plus/versions`, which returned HTTP `200`.
- APKPure `.net` versions URL for package `com.bloomberg.android.plus` returned HTTP `410 Gone`.
- APKPure `.com` versions URL returned HTTP `403`.
- AndroidAPKsFree guessed old versions URL for package `com.bloomberg.android.plus` returned HTTP `404`.
- APKMirror history URL returned HTTP `403` for automated fetches.

## Next Step

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 281941097`.
- iOS version list result: failed because App Store license is required.
- iOS license attempt for bundle ID `com.bloomberg.Bloomberg` returned app not found.
- Raw iOS version-list error: `reports/bloomberg/version-list-error.json`
- Android Aiting catalog fetched on 2026-05-26 with `fetch_aiting_versions.py`.
- Android entries available from Aiting sources: 5
- Oldest Android versionCode in the Aiting catalog: `3042781` (`5.58.0.3042781.7b196c06c`)
- Newest Android versionCode in the Aiting catalog: `4315110` (`6.19.0.4315110.19bd92161`)
- Raw Android version catalog: `reports/bloomberg/android-version-list.json`
- Aiting currently exposes a limited visible old-version catalog and does not expose publish dates in the current parser.

## Next Step

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 5
- Unique package SHA-256 hashes: 5
- Android package source: Aiting visible catalog.
- Android RN markers detected: yes, in every sampled APK.
- Exposed Android JS bundle path: `assets/index.android.bundle`
- Android reports: `reports/bloomberg/android-versions.csv`, `reports/bloomberg/android-ranges.csv`, and `reports/bloomberg/android-transitions.csv`.

## Provisional Ranges

| Platform | RN inference | Confidence | First sampled version | Last sampled version | Catalog rows |
| --- | --- | --- | --- | --- | --- |
| Android | 0.61.x | medium | 5.58.0.3042781.7b196c06c (`3042781`) | 5.58.0.3042781.7b196c06c (`3042781`) | 1 |
| Android | 0.74.x-0.76.x | medium | 5.98.0.3930355.fd19b588e (`3930355`) | 6.19.0.4315110.19bd92161 (`4315110`) | 4 |

## Open Gaps

- iOS version-list access is blocked by license requirements, so the Android evidence has not been reconciled against iOS builds.
- Aiting exposes only 5 visible Bloomberg entries and does not expose publish dates in the current parser; the `0.61.x` to `0.74.x-0.76.x` transition is source-limited, not an exact boundary.
