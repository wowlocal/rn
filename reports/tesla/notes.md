# Tesla React Native Timeline

## Registration

- App name: Tesla
- App Store ID: 582007913
- iOS bundle ID: com.teslamotors.TeslaApp
- Android package: com.teslamotors.tesla
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Tesla --format json` did not return the official Tesla app in the current localized results.
- Public App Store URL and Apple iTunes lookup for App Store ID `582007913` returned app name `Tesla`, seller `Tesla, Inc.`, bundle ID `com.teslamotors.TeslaApp`, and current US listed version `4.57.0`.
- App Store URL: `https://apps.apple.com/us/app/tesla/id582007913`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.teslamotors.tesla`.
- Android package sources identify package `com.teslamotors.tesla`.
- APKPure history page identified: `https://apkpure.net/tesla/com.teslamotors.tesla/versions`.
- The guessed AndroidAPKsFree old versions URL for package `com.teslamotors.tesla` returned HTTP 404.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 582007913`.
- iOS version list result: failed because App Store license is required.
- iOS license attempt for bundle ID `com.teslamotors.TeslaApp` returned app not found.
- Raw iOS version-list error: `reports/tesla/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `4094` (`4.54.0-4094`)
- Newest Android versionCode in the APKPure catalog: `4306` (`4.57.0-4306`)
- Raw Android version catalog: `reports/tesla/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.
- Android versionCode values are not fully monotonic with APKPure source dates in the fetched catalog, so Android summaries order by versionCode first and keep source dates as context.

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Unique package SHA-256 hashes: 3
- Android package source: APKPure visible catalog.
- Android RN markers detected: yes, in every sampled APK/XAPK.
- Exposed Android JS bundle path: `assets/index.android.bundle`
- Package hash validation found eight XAPK rows with the same SHA-256 as the current `4.57.0-4306` package (`0dc65f8137af...`): `4.54.0-4094`, `4.54.5-4133`, `4.55.5-4193`, `4.55.6-4229`, `4.55.7-4234`, `4.56.1-4255`, `4.56.5-4281`, and `4.57.0-4306`.
- Those duplicated XAPK rows also contain embedded XAPK manifest metadata reporting `version_code` `4306` and `version_name` `4.57.0-4306`, so they are source-quality findings rather than independent historical builds.
- Android reports: `reports/tesla/android-versions.csv`, `reports/tesla/android-ranges.csv`, and `reports/tesla/android-transitions.csv`.

## Provisional Ranges

| Platform | RN inference | Confidence | First sampled version | Last sampled version | Catalog rows |
| --- | --- | --- | --- | --- | --- |
| Android | 0.79.x | medium | 4.54.0-4094 (`4094`), APKPure date `2026-03-06` | 4.54.0-4094 (`4094`), APKPure date `2026-03-06` | 1 |
| Android | 0.82.x or newer | low | 4.54.3-4107 (`4107`), APKPure date `2026-03-02` | 4.54.3-4107 (`4107`), APKPure date `2026-03-02` | 1 |
| Android | 0.79.x | medium | 4.54.5-4133 (`4133`), APKPure date `2026-03-11` | 4.57.0-4306 (`4306`), APKPure date `2026-05-14` | 8 |

## Open Gaps

- iOS version-list access is blocked by license requirements, so the Android evidence has not been reconciled against iOS builds.
- APKPure exposes only 10 visible Tesla entries and returned duplicated current-package payloads for most older XAPK rows; adjacent rows are not exact transition boundaries.
- Standalone APK `4.54.3-4107` conflicts with adjacent XAPK rows by inferring `0.82.x or newer` with low confidence while surrounding versionCode rows infer `0.79.x` with medium confidence. Treat it as a package-format/source anomaly pending manual review.
- `4.55.0-4166` is labeled `APK,XAPK` by the source but the downloaded `.xapk` has APK contents at the ZIP root. The analyzer now handles root-level APK content in non-`.apk` package files.
