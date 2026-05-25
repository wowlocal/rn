# Threads React Native Timeline

## Registration

- App name: Threads
- App Store ID: 6446901002
- iOS bundle ID: com.burbn.barcelona
- Android package: com.instagram.barcelona
- Status: sampled
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Threads --format json` resolved App Store ID `6446901002`, bundle ID `com.burbn.barcelona`, and current listed iOS version `431.0`.
- App Store URL: `https://apps.apple.com/us/app/threads/id6446901002`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.instagram.barcelona`.
- Android package history sources identified: APKMirror and APKPure pages for package `com.instagram.barcelona`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions` through `check_rn_versions.py --list-versions-only`.
- iOS external version IDs available: 182
- Oldest iOS external version ID: `855897532`
- Newest iOS external version ID: `885819877`
- Raw iOS version list: `reports/threads/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 11
- Oldest Android versionCode in the APKPure catalog: `504412928`
- Newest Android versionCode in the APKPure catalog: `510007506`
- Raw Android version catalog: `reports/threads/android-version-list.json`
- APKMirror was identified as a potentially richer Android history source, but automated fetches returned a Cloudflare challenge. APKPure is usable but currently exposes a limited visible history on the fetched page.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 11
- Android package source: APKPure visible version catalog plus one APKPure direct historical download page
- Android RN markers detected: yes, in `374.0.0.43.110 (504412928)` via native/package metadata listing `reactnativejni`, `react_featureflagsjni`, and `yoga`.
- Android samples from `400.0.0.38.68 (507007017)` through `430.0.0.46.79 (510007506)` did not expose React Native JS bundles or RN native-library metadata with the current analyzer.
- Android reports: `reports/threads/android-versions.csv`, `reports/threads/android-ranges.csv`, and `reports/threads/android-transitions.csv`.
- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 12
- Unique iOS builds analyzed: 12
- iOS sampled external version IDs: `855897532`, `860015214`, `863430462`, `865653252`, `867990482`, `870508385`, `873427556`, `875824747`, `878332041`, `879918641`, `882713754`, `885819877`
- iOS RN markers detected: no. All sampled iOS builds remain `unknown` from encrypted IPA inspection because no JS bundle markers were exposed.
- iOS reports: `reports/threads/versions.csv`, `reports/threads/ranges.csv`, and empty `reports/threads/transitions.json`.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | unknown, RN native metadata present | low | 374.0.0.43.110 (`504412928`), APKPure date `2025-04-01` | 374.0.0.43.110 (`504412928`), APKPure date `2025-04-01` | 1 |
| Android | unknown, no RN markers exposed | unknown | 400.0.0.38.68 (`507007017`), APKPure date `2025-09-28` | 430.0.0.46.79 (`510007506`), APKPure date `2026-05-19` | 10 |
| iOS | unknown | low | 289.0 (489338310), external ID `855897532`, IPA timestamp `2023-06-27T23:32:54` | 431.0.0 (979167741), external ID `885819877`, IPA timestamp `2026-05-25T02:25:36` | 12 |

## Open Gaps

- Android boundary refinement added APKPure page version `400.0.0.38.68 (507007017)`, which does not expose RN markers.
- Android has a source-limited marker-disappearance window between `374.0.0.43.110 (504412928)` and `400.0.0.38.68 (507007017)`.
- APKMirror may have more historical Android packages, but automated fetches returned a Cloudflare challenge.
- Exact RN patch versions are not recoverable from the Android native metadata or encrypted iOS samples currently available.
- Initial sampling validation passed on 2026-05-26: Android/iOS CSV and JSON reports parse, Android reports include RN native-library evidence for versionCode `504412928`, and cross-app reports include platform-labeled Threads rows.
- Disk cleanup was not performed after initial sampling because `apks/threads` and `ipas/threads` each used about 1.2 GiB and the filesystem still had 233 GiB available.

## Next Step

Refine the Android marker-disappearance window if a richer Android source can be accessed, and sample targeted iOS versions only if Android evidence suggests an iOS boundary worth checking.
