# Threads React Native Timeline

## Registration

- App name: Threads
- App Store ID: 6446901002
- iOS bundle ID: com.burbn.barcelona
- Android package: com.instagram.barcelona
- Status: needs_manual_review
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
- Android entries available from APKPure sources: 12
- Oldest Android versionCode in the APKPure catalog: `504412928`
- Newest Android versionCode in the APKPure catalog: `510007506`
- Raw Android version catalog: `reports/threads/android-version-list.json`
- APKMirror was identified as a potentially richer Android history source, but automated fetches returned a Cloudflare challenge. APKPure is usable but currently exposes a limited visible history on the fetched page.

## Initial Sampling

- Android sampling date: 2026-05-26
- Android packages downloaded and analyzed: 12
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

## Decrypted iOS Evidence

- Decrypted iOS dump date: 2026-05-26.
- Dump tooling: `./dump_ios_ipa.py <ipa> --method frida-ipa-extract --all-binaries`; the wrapper installed through `ideviceinstaller` when SSH password auth was unavailable and recorded device context from `ideviceinfo`.
- Device context for accepted dumps: iOS `16.7.7` (`20H330`), hardware model `D201AP`.
- `400.0.0` build `797742903`, external ID `878332041`: source IPA SHA-256 `e0738704798ec7c37f261f543065cd0503241b0689b0d55c6646079548396b41`, dumped IPA SHA-256 `2495a9c1b324d349165653d7a39839b241fd2badc344a941031fb888e8a00681`, dumped size `76109478`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `431.0.0` build `979167741`, external ID `885819877`: source IPA SHA-256 `6985cd26785bf11563f89a81fcf81546c18da78272e984f4294e8ab8f284af0b`, dumped IPA SHA-256 `0469b0c5224b17f3e760ba78b5ff23a7df207a715e10cba43b22eaef84239b72`, dumped size `111514854`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `400.0.0` initially failed while spawned under `frida-ipa-extract` with `frida.InvalidOperationError: script has been destroyed`; after verifying the installed build with `ideviceinstaller`, a lightweight Frida launch plus wrapper `--skip-install --no-kill-before-dump --attach-running` produced the accepted dump.
- Per-Mach-O inventory for `400.0.0`: 5 Mach-Os total; main executable decrypted; 4 app-extension executables remain encrypted.
- Per-Mach-O inventory for `431.0.0`: 7 Mach-Os total; main executable and 2 bundled framework/dylib Mach-Os decrypted; 4 app-extension executables remain encrypted.
- Remaining encrypted executables are `BarcelonaNotificationExtension`, `BarcelonaShareExtension`, `BarcelonaWidgetExtension`, and `BarcelonaWidgetExtensionLiveActivities`. Extension attach was not pursued because the main executable already contains the RN-related native evidence and no current evidence suggests the RN version marker only lives in extensions.
- Decrypted analyzer result for both accepted rows: no JS bundle, Hermes bytecode, `react-native-renderer`, `BatchedBridge`, or `AppRegistry` marker was found; the decrypted main executable does contain native `ReactNative` / `react_native` plus JSI/Yoga references. RN presence is therefore stronger for these two iOS rows, but exact RN version remains `unknown` with reason `native_rn_marker_without_version`.
- The 10 other sampled iOS rows remain unresolved with reason `encrypted_native_only`; each row now carries a next action to dump with `frida-ipa-extract --all-binaries` only if it becomes boundary-priority evidence.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| Android | unknown, RN native metadata present | low | 374.0.0.43.110 (`504412928`), APKPure date `2025-04-01` | 382.0.0.51.85 (`505205644`), APKPure date `2025-05-28` | 2 |
| Android | unknown, no RN markers exposed | unknown | 400.0.0.38.68 (`507007017`), APKPure date `2025-09-28` | 430.0.0.46.79 (`510007506`), APKPure date `2026-05-19` | 10 |
| iOS | unknown | low | 289.0 (489338310), external ID `855897532`, IPA timestamp `2023-06-27T23:32:54` | 431.0.0 (979167741), external ID `885819877`, IPA timestamp `2026-05-25T02:25:36` | 12 |

## Open Gaps

- Android boundary refinement added APKPure page versions `382.0.0.51.85 (505205644)` and `400.0.0.38.68 (507007017)`.
- `382.0.0.51.85 (505205644)` still exposes RN native metadata; `400.0.0.38.68 (507007017)` does not expose RN markers.
- Android has a source-limited marker-disappearance window between `382.0.0.51.85 (505205644)` and `400.0.0.38.68 (507007017)`.
- iOS decrypted evidence for app `400.0.0` still contains native RN references, so the Android marker disappearance should be treated as analyzer/source-limited rather than proof that Threads removed RN by that release train.
- APKMirror may have more historical Android packages, but automated fetches returned a Cloudflare challenge.
- Other mirrors surfaced possible intermediate builds, but their exposed signature metadata did not match the APKPure/Instagram signature, so they were not used as evidence.
- Exact RN patch versions are not recoverable from the Android native metadata, encrypted iOS samples, or the two accepted decrypted iOS dumps currently available.
- Initial sampling validation passed on 2026-05-26: Android/iOS CSV and JSON reports parse, Android reports include RN native-library evidence for versionCode `504412928`, and cross-app reports include platform-labeled Threads rows.
- Disk cleanup was not performed after initial sampling because `apks/threads` and `ipas/threads` each used about 1.2 GiB and the filesystem still had 233 GiB available.

## Next Step

Manual review is still needed to access trusted APKMirror or another signature-verified source for Android builds between `382.0.0.51.85` and `400.0.0.38.68`. If more iOS work is needed, decrypt `373.0.0` and `387.0.0` before dumping broad history; otherwise look for stronger native RN version constants or a triggerable RN surface that loads version-specific code.
