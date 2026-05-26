# Instagram iOS React Native Timeline

## Registration

- App name: Instagram
- App Store ID: 389801252
- Bundle ID: com.burbn.instagram
- Status: done
- Registration date: 2026-05-25

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- App Store URL resolved as `https://apps.apple.com/us/app/instagram/id389801252`.
- `ipatool search instagram --format json` resolved bundle ID `com.burbn.instagram` and current listed version `430.0.0`.

## Version List

- External version IDs available: 795
- Oldest external version ID: `2948163`
- Newest external version ID: `885526725`
- Raw version list: `reports/instagram/version-list.json`
- Fetch note: `ipatool list-versions --app-id 389801252 --format json` returned Apple's generic unknown error, but `ipatool list-versions --bundle-identifier com.burbn.instagram --format json` succeeded.

## Sampling and Boundary Refinement

- Sampling date: 2026-05-26
- IPAs downloaded and analyzed: 36
- Unique builds analyzed: 34
- Oldest analyzed build: app version blank, build `1.8.7`, external ID `2948163`, build timestamp `2010-09-27T16:39:00`
- Newest analyzed build: `430.0.0 (972915403)`, external ID `885526725`, build timestamp `2026-05-16T18:55:26`
- RN markers detected: yes, from `10.0.0 (44114773)` through latest sampled build `430.0.0 (972915403)`, although latest exact RN version remains unresolved.
- Analyzer update on 2026-05-26 added support for zstd-compressed `main.jsbundle.zst`, `main.hbcbundle`, and React renderer inspector markers such as `version:"16.8.6",rendererPackageName:"react-native-renderer"`.
- Updated marker bands now include `<=0.59.x`, `0.60.x`, `0.61.x`, `0.64.x`, `0.69.x-0.70.x`, `0.71.x`, `0.78.x`, and `0.83.x`.
- Full row-level evidence is in `reports/instagram/versions.csv` and `reports/instagram/versions.json`.
- Duplicate external IDs `831095391` and `831129706` both map to `91.0 (151989260)`; duplicate external IDs `832266212` and `832333184` both map to `106.0 (166752244)`. Range starts use the earliest duplicate external ID so transition gaps match App Store ordering.

## Decrypted iOS Evidence

- Decrypted iOS dump date: 2026-05-26.
- Dump tooling: `./dump_ios_ipa.py <ipa> --method frida-ipa-extract --all-binaries`; the wrapper installed through `ideviceinstaller` and recorded device context from `ideviceinfo`.
- Device context for accepted dumps: iOS `16.7.7` (`20H330`), hardware model `D201AP`.
- `114.0` build `176133011`, external ID `832986604`: source IPA SHA-256 `b37c6b8190158ef59ade270222a612e539500647c57dce02aa56ca67d7fe7abf`, dumped IPA SHA-256 `9812fbd41b2c3d83c074043e3dcddc10c8df57a0a18fec5c23d6b2978176e1ad`, dumped size `73387774`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `main_only_decrypted`.
- `430.0.0` build `972915403`, external ID `885526725`: source IPA SHA-256 `435da2b593b711211feb099b82ae6909cf23e07ff7c14898c349761a49a1dafe`, dumped IPA SHA-256 `4113218bff9df91cb3de9d0ed4cc64c4d2c07e383f6a4715dcaf730370c08d05`, dumped size `326217004`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- `114.0` decrypted analysis confirms `main.jsbundle.zst` resolves to RN `0.61.x` with React renderer `16.8.6`; one non-extension framework (`InstagramAppCoreImplFramework`) and two app extensions remain encrypted, so exact native constants outside the main executable are still limited.
- `430.0.0` decrypted analysis finds `main.hbcbundle` Hermes bytecode version `98` and native React Native/Hermes/JSI/Yoga markers in the decrypted main executable, but no version-specific RN marker or renderer marker. The row remains RN `unknown` with reason `native_rn_marker_without_version`.
- Remaining encrypted executables in `430.0.0` are app extensions only. Extension attach was not pursued because RN evidence already appears in the main app bundle/main executable and no current evidence suggests the RN version marker only lives in extensions.

## Exact RN Transitions

| From | To | Version-list gap |
|---|---|---:|
| unknown at `9.7.0 (43028597)`, external ID `819447240` | `<=0.59.x` at `10.0.0 (44114773)`, external ID `819646349` | 0 |
| `<=0.59.x` at `90.0 (150975176)`, external ID `830989899` | `0.60.x` at `91.0 (151989260)`, external ID `831095391` | 0 |
| `0.60.x` at `105.0 (165586599)`, external ID `832184604` | `0.61.x` at `106.0 (166752244)`, external ID `832266212` | 0 |
| `0.83.x` at `385.0.0 (748614773)`, external ID `875444719` | unknown at `430.0.0 (972915403)`, external ID `885526725` | 21 |

## RN Ranges

| RN guess | Renderer | Confidence | Start | End | Builds |
|---|---:|---|---|---|---:|
| unknown |  | low | build 1.8.7, `2948163`, `2010-09-27T16:39:00` | 9.7.0 (43028597), `819447240`, `2016-11-03T10:43:20` | 9 |
| <=0.59.x |  | medium | 10.0.0 (44114773), `819646349`, `2016-11-17T12:37:44` | 90.0 (150975176), `830989899`, `2019-04-19T17:03:30` | 6 |
| 0.60.x |  | medium | 91.0 (151989260), `831095391`, `2019-04-27T03:34:08` | 105.0 (165586599), `832184604`, `2019-08-01T19:22:40` | 5 |
| 0.61.x |  | medium | 106.0 (166752244), `832266212`, `2019-08-09T18:53:36` | 118.0 (180988914), `833368709`, `2019-11-01T17:18:24` | 8 |
| 0.64.x |  | medium | 177.0 (275424340), `840589643`, `2021-02-26T15:39:50` | 177.0 (275424340), `840589643`, `2021-02-26T15:39:50` | 1 |
| 0.69.x-0.70.x |  | medium | 236.1 (372089098), `849384047`, `2022-05-24T23:28:50` | 236.1 (372089098), `849384047`, `2022-05-24T23:28:50` | 1 |
| 0.71.x |  | medium | 290.1 (491279855), `858142473`, `2023-07-03T20:59:36` | 290.1 (491279855), `858142473`, `2023-07-03T20:59:36` | 1 |
| 0.78.x | 19.0.0 | high | 340.0.10 (622957927), `867327376`, `2024-07-15T23:38:50` | 340.0.10 (622957927), `867327376`, `2024-07-15T23:38:50` | 1 |
| 0.83.x | 19.2.0 | medium | 385.0.0 (748614773), `875444719`, `2025-06-14T08:13:04` | 385.0.0 (748614773), `875444719`, `2025-06-14T08:13:04` | 1 |
| unknown |  | low | 430.0.0 (972915403), `885526725`, `2026-05-16T18:55:26` | 430.0.0 (972915403), `885526725`, `2026-05-16T18:55:26` | 1 |

## Cleanup and Validation

- Disk cleanup reviewed on 2026-05-26; no Instagram IPAs were deleted because `ipas/instagram` used 3.7 GiB and the filesystem still had 236 GiB available.
- Validation passed on 2026-05-26: scripts compile, Instagram CSV/JSON reports parse, decrypted dump reports for `114.0` and `430.0.0` were accepted, and all remaining unknown rows carry `unknown_reason` plus `next_action`.
- Exact RN patch versions are not recoverable for every row; most detected builds are JS/Hermes marker-band estimates, while `340.0.10` and `385.0.0` use direct renderer markers.
