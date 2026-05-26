# Skype React Native Timeline

## Registration
- App name: Skype
- App Store ID: 304878510
- iOS bundle ID: com.skype.skype
- Android package: com.skype.raider
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence
- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- Skype consumer service and apps are retired as of 2025-05-05.
- Current Apple iTunes lookup for App Store ID 304878510 returns no result.
- Current Google Play URL for package com.skype.raider returns 404.
- Historical iOS identifier sources identify App Store ID 304878510 and bundle ID com.skype.skype for Skype for iPhone.
- APKPure identifies Android package com.skype.raider and exposes package history URL https://apkpure.net/skype/com.skype.raider/versions.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 304878510`.
- iOS external version IDs available: 185
- Oldest iOS external version ID: `822306851`
- Newest iOS external version ID: `874426597`
- Raw iOS version list: `reports/skype/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `1250181076` (`8.132.0.201`)
- Newest Android versionCode in the APKPure catalog: `1250186747` (`8.150.0.125`)
- Raw Android version catalog: `reports/skype/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Android package source: APKPure visible catalog
- Android RN markers detected: yes, in every sampled package.
- Exposed React Native native-library metadata includes `libfabricjni.so`, `libhermes.so`, `libhermes_executor.so`, `libjsi.so`, `libreactnativejni.so`, `libturbomodulejsijni.so`, and `libyoga.so`.
- Bundle path detected: `assets/index.android.bundle`
- Current Android RN inference: `0.74.x-0.76.x`, medium confidence.
- Android reports: `reports/skype/android-versions.csv`, `reports/skype/android-ranges.csv`, and empty `reports/skype/android-transitions.json`.
- iOS sampling was not performed in this pass because Android APKs exposed direct bundle and native-library evidence.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | 0.74.x-0.76.x | medium | 8.132.0.201 (`1250181076`), APKPure date `2024-11-11` | 8.150.0.125 (`1250186747`), APKPure date `2025-05-05` | 10 |

## Open Gaps

- APKPure remains sparse/source-limited and exposes only 10 visible rows across the sampled window.
- Current public Apple lookup and Google Play lookup no longer resolve the retired consumer Skype app.
- iOS version IDs are available, but iOS IPAs were not sampled in this Android-first pass.
- No RN transition was observed in the accessible Android package window.
- Disk cleanup was not performed after Android sampling because `apks/skype` used about 728 MiB and the filesystem still had 215 GiB available.

## Next Step
Manual review should use a more complete Android package history or targeted iOS IPA samples to identify whether RN transition boundaries exist outside the visible APKPure window.
