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

## iOS Sampling

- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 20
- Unique iOS app version/build pairs analyzed: 19
- iOS RN markers detected: yes, in every sampled IPA.
- Bundle path detected: `Payload/Skype4Life.app/main.jsbundle`
- iOS reports: `reports/skype/versions.csv`, `reports/skype/ranges.csv`, `reports/skype/transitions.csv`, and matching JSON files.
- Oldest sampled iOS IPA: `8.1.46715` (`8.1.0.46715`, external ID `822306851`), inferred as RN `<=0.59.x` with medium confidence.
- Latest sampled iOS IPA: `8.150.3125` (`8.150.0.125`, external ID `874426597`), inferred as RN `0.71.x` with medium confidence.
- Exact iOS transition found: `8.82.403` (`8.82.0.403`, external ID `847669772`) RN `0.63.x` -> `8.83.408` (`8.83.0.408`, external ID `848201751`) RN `0.66.x`.
- Exact iOS transition found: `8.96.3409` (`8.96.0.409`, external ID `856507877`) RN `0.66.x` -> `8.97.3203` (`8.97.0.203`, external ID `856630693`) RN `0.71.x`.
- The early sampled transition from `8.1.46715` RN `<=0.59.x` to `8.79.92` RN `0.63.x` has a 91-ID known-list gap and should be treated as approximate.

## iOS Decrypted Evidence

- Accepted decrypted dump for latest iOS build `8.150.3125` (`8.150.0.125`, external ID `874426597`). The installed metadata matched the source IPA, the main executable has `cryptid 0`, and coverage is `loaded_app_decrypted`.
- Latest dump source SHA-256: `8050ae44b1169f4d7872697649042abef4849c074651e34407c0cef37bb8e639`
- Latest dump SHA-256: `1801c56b93db02cfdea44818d05e74f35efc0813e1c29402d91abb0f96e70d59`
- Accepted decrypted dump for first RN `0.71.x` iOS build `8.97.3203` (`8.97.0.203`, external ID `856630693`). The installed metadata matched the source IPA, the main executable has `cryptid 0`, and coverage is `loaded_app_decrypted`.
- Boundary dump source SHA-256: `ef3d494e688aaaf39bfa5a6b8ac7aaa9e3b308707b00b9c8ae32c1f55f406e33`
- Boundary dump SHA-256: `9817cb07cb5d4e6061c78126084c31ed1a43483829b22bd579d88bb816c7f7a8`
- Decrypted dump analysis exposed native React Native, JSI, and Yoga markers in both accepted dumps. Hermes native markers are present in the latest dump and absent in the `8.97.3203` dump, while the JS marker band remains RN `0.71.x`.
- Remaining encrypted Mach-O files are app extensions only; no encrypted non-extension binary remained in either accepted dump.
- App-extension decryption was not pursued because the main app bundle already exposes the RN evidence needed for the timeline.

## Android Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 10
- Android package source: APKPure visible catalog
- Android RN markers detected: yes, in every sampled package.
- Exposed React Native native-library metadata includes `libfabricjni.so`, `libhermes.so`, `libhermes_executor.so`, `libjsi.so`, `libreactnativejni.so`, `libturbomodulejsijni.so`, and `libyoga.so`.
- Bundle path detected: `assets/index.android.bundle`
- Current Android RN inference: `0.74.x-0.76.x`, medium confidence.
- Android reports: `reports/skype/android-versions.csv`, `reports/skype/android-ranges.csv`, and empty `reports/skype/android-transitions.json`.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| iOS | <=0.59.x | medium | 8.1.46715 (`8.1.0.46715`, external `822306851`) | 8.1.46715 (`8.1.0.46715`, external `822306851`) | 1 |
| iOS | 0.63.x | medium | 8.79.92 (`8.79.0.92`, external `845553986`) | 8.82.403 (`8.82.0.403`, external `847669772`) | 7 |
| iOS | 0.66.x | medium | 8.83.408 (`8.83.0.408`, external `848201751`) | 8.96.3409 (`8.96.0.409`, external `856507877`) | 7 |
| iOS | 0.71.x | medium | 8.97.3203 (`8.97.0.203`, external `856630693`) | 8.150.3125 (`8.150.0.125`, external `874426597`) | 4 |
| Android | 0.74.x-0.76.x | medium | 8.132.0.201 (`1250181076`), APKPure date `2024-11-11` | 8.150.0.125 (`1250186747`), APKPure date `2025-05-05` | 10 |

## Open Gaps

- APKPure remains sparse/source-limited and exposes only 10 visible Android rows across the sampled window.
- Current public Apple lookup and Google Play lookup no longer resolve the retired consumer Skype app.
- The iOS `<=0.59.x` -> `0.63.x` upgrade is only bounded by sampled endpoints, with 91 known external version IDs between them.
- Android latest source-limited inference (`0.74.x-0.76.x`) conflicts with iOS latest inference (`0.71.x`), so the platform timelines should remain separate.
- No RN transition was observed in the accessible Android package window.
- Disk cleanup was not performed after Skype sampling because `ipas/skype` used about 1.4 GiB, `apks/skype` used about 709 MiB, and the filesystem still had about 162 GiB available.

## Next Step
Manual review should use a more complete Android package history or additional old iOS IPA samples between external IDs `822306851` and `845553986` if the early `<=0.59.x` -> `0.63.x` transition boundary is needed.
