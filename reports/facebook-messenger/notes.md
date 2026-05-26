# Facebook Messenger iOS React Native Timeline

## Registration

- App name: Facebook Messenger
- App Store ID: 454638411
- Bundle ID: com.facebook.Messenger
- Status: done
- Registration date: 2026-05-25

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- App Store URL resolved as `https://apps.apple.com/us/app/messenger/id454638411`.
- `ipatool search facebook --format json` resolved bundle ID `com.facebook.Messenger` and current listed version `562.0.0`.

## Version List

- External version IDs available: 735
- Oldest external version ID: `4003333`
- Newest external version ID: `885556428`
- Raw version list: `reports/facebook-messenger/version-list.json`

## Initial Sampling

- IPAs downloaded: 26
- Unique builds analyzed: 26
- Oldest analyzed build: app version blank, build `1000`, external ID `4003333`, build timestamp `2011-08-02T21:45:38`
- Newest analyzed build: `562.0.0 (975021560)`, external ID `885556428`, build timestamp `2026-05-19T17:01:04`
- RN markers detected: yes. Version-specific JS marker bands identify `92.0 (41023043)` through `147.0 (84235609)` as `<=0.59.x`.
- Analyzer update on 2026-05-26 also detected renderer inspector markers in `146.0`, `147.0`, and `148.0`, plus latest `main.hbcbundle` Hermes bytecode. The latest exact RN version remains unresolved.
- Unknown rows now carry `unknown_reason` plus `next_action` in `reports/facebook-messenger/versions.csv` and `reports/facebook-messenger/versions.json`.

| External ID | App version | Build | Build timestamp | JS bundle | RN guess | Confidence |
|---|---|---:|---|---|---|---|
| `4003333` |  | 1000 | 2011-08-02T21:45:38 | no | unknown | low |
| `812231857` | 26.0 | 9347487 | 2014-07-28T20:42:06 | no | unknown | low |
| `816903024` | 65.0 | 27013135 | 2016-04-04T17:23:02 | no | unknown | low |
| `818196039` | 81.0 | 34694251 | 2016-07-25T14:07:34 | no | unknown | low |
| `818893675` | 89.0 | 39433806 | 2016-09-19T14:44:26 | no | unknown | low |
| `818999426` | 90.0 | 39954546 | 2016-09-26T15:07:46 | no | unknown | low |
| `819099576` | 91.0 | 40546824 | 2016-10-02T15:12:24 | `Payload/Messenger.app/main.jsbundle` | unknown | low |
| `819183439` | 92.0 | 41023043 | 2016-10-08T09:13:24 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `819274182` | 93.0 | 41774394 | 2016-10-17T13:46:22 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `819781397` | 98.0 | 44186053 | 2016-11-18T11:12:28 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `823243677` | 131.0 | 68165081 | 2017-08-14T08:58:26 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `824651339` | 145.0 | 82143310 | 2017-11-28T17:09:26 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `825195544` | 146.0 | 83068889 | 2017-12-04T18:28:34 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `825227473` | 147.0 | 84235609 | 2017-12-12T09:16:54 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `825310109` | 148.0 | 86952252 | 2018-01-08T17:01:12 | `Payload/Messenger.app/main.jsbundle` | unknown (renderer `16.2.0`) | low |
| `825599677` | 149.0 | 87964402 | 2018-01-16T14:39:26 | no | unknown | low |
| `825927199` | 153.0 | 91923955 | 2018-02-12T20:12:40 | no | unknown | low |
| `826787358` | 163.0 | 104735954 | 2018-04-24T07:01:24 | no | unknown | low |
| `828538485` | 183.0 | 123940704 | 2018-09-11T23:41:04 | no | unknown | low |
| `833799330` | 243.1 | 185914695 | 2019-11-27T12:24:04 | no | unknown | low |
| `838965715` | 291.0 | 256509383 | 2020-10-20T14:56:02 | no | unknown | low |
| `845952569` | 342.0 | 338823778 | 2021-12-10T00:40:28 | no | unknown | low |
| `854961972` | 396.1 | 446890740 | 2023-02-16T22:36:16 | no | unknown | low |
| `864747553` | 452.0.0 | 583923274 | 2024-03-28T16:48:02 | no | unknown | low |
| `873336561` | 500.0.0 | 713622393 | 2025-03-14T00:36:32 | no | unknown | low |
| `885556428` | 562.0.0 | 975021560 | 2026-05-19T17:01:04 | `Payload/Messenger.app/main.hbcbundle` | unknown | low |

## Decrypted iOS Evidence

- Decrypted iOS dump date: 2026-05-26.
- Dump tooling: `./dump_ios_ipa.py <ipa> --method frida-ipa-extract --all-binaries`; the wrapper installed through `ideviceinstaller` and recorded device context from `ideviceinfo`.
- Device context for dump attempts: iOS `16.7.7` (`20H330`), hardware model `D201AP`.
- `91.0` build `40546824`, external ID `819099576`: source IPA SHA-256 `fef1553354769962d57250f34098762cba4f13d2e8a02515a48b7bcf0875ad1e`, size `151303500`. Install succeeded and installed metadata matched the target row, but Frida spawn timed out; `uiopen` plus attach-running retry found the app was not running, so no accepted decrypted dump was produced.
- `148.0` build `86952252`, external ID `825310109`: source IPA SHA-256 `5a5d6431148dcee7050c2eb5ef81c6e20b6b26319fba6a71c15f7628ae2ece3e`, size `159102566`. Install succeeded and installed metadata matched the target row, but Frida spawn timed out; `uiopen` plus attach-running retry found the app was not running, so no accepted decrypted dump was produced.
- `149.0` build `87964402`, external ID `825599677`: source IPA SHA-256 `efe293756f42bad1468aea5f46ad3c2aa5da9dc830abd854917f25358ef29099`, size `150953490`. Install succeeded and installed metadata matched the target row, but Frida spawn timed out; skip-install prelaunch plus attach-running retry found the app was not running, so no accepted decrypted dump was produced.
- `562.0.0` build `975021560`, external ID `885556428`: source IPA SHA-256 `33277e64591f60a4a7dff8b9d3d5846e29f5bdd046b471e85a59bf9a52c5c808`, dumped IPA SHA-256 `29b0960be715decd5f828b25e96a9399da14ba31686c5cb0a37228aa0d634338`, dumped size `129675715`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `main_only_decrypted`.
- `562.0.0` decrypted analysis finds `main.hbcbundle` Hermes bytecode version `98`, generic React Native bridge markers, and a native React Native marker in the decrypted main executable, but no version-specific RN marker or renderer marker. The row remains RN `unknown` with reason `native_rn_marker_without_version`.
- Remaining encrypted non-extension code in `562.0.0`: `Payload/Messenger.app/Frameworks/RTCAndSpark.framework/RTCAndSpark`. Seven app extensions also remain encrypted, so exact constants outside the loaded main app and two dumped frameworks are still limited.

## RN Ranges

| RN guess | Renderer | Confidence | Start | End | Builds |
|---|---:|---|---|---|---:|
| unknown |  | low | build 1000, `4003333`, `2011-08-02T21:45:38` | 91.0 (40546824), `819099576`, `2016-10-02T15:12:24` | 7 |
| <=0.59.x |  | medium | 92.0 (41023043), `819183439`, `2016-10-08T09:13:24` | 145.0 (82143310), `824651339`, `2017-11-28T17:09:26` | 5 |
| <=0.59.x | 16.1.1 | medium | 146.0 (83068889), `825195544`, `2017-12-04T15:09:24` | 146.0 (83068889), `825195544`, `2017-12-04T15:09:24` | 1 |
| <=0.59.x | 16.2.0 | medium | 147.0 (84235609), `825227473`, `2017-12-12T09:16:54` | 147.0 (84235609), `825227473`, `2017-12-12T09:16:54` | 1 |
| unknown (react-native-renderer 16.2.0) | 16.2.0 | low | 148.0 (86952252), `825310109`, `2018-01-08T17:01:12` | 148.0 (86952252), `825310109`, `2018-01-08T17:01:12` | 1 |
| unknown |  | low | 149.0 (87964402), `825599677`, `2018-01-16T14:39:26` | 562.0.0 (975021560), `885556428`, `2026-05-19T17:01:04` | 11 |

## Unresolved Gaps

- RN introduction boundary is exact: `91.0 (40546824)`, external ID `819099576`, build timestamp `2016-10-02T15:12:24`, unknown -> `92.0 (41023043)`, external ID `819183439`, build timestamp `2016-10-08T09:13:24`, RN <=0.59.x. Gap size: 0.
- RN disappearance boundary is exact at the version-list level: `147.0 (84235609)`, external ID `825227473`, build timestamp `2017-12-12T09:16:54`, RN `<=0.59.x` -> `148.0 (86952252)`, external ID `825310109`, build timestamp `2018-01-08T17:01:12`, unknown with renderer `16.2.0`. Gap size: 0.
- Exact RN patch versions are not recoverable for every row; the detected early builds are JS-marker band estimates, while latest decrypted evidence confirms RN-like bridge/native markers without a version-specific marker.

## Final Validation

- Scripts compile with `python3 -m py_compile`.
- `versions`, `ranges`, `transitions`, and `timeline` CSV/JSON reports parse successfully.
- Decrypted dump report for `562.0.0` was accepted; dump attempts for `91.0` and `148.0` were rejected because the installed apps did not stay running for attach on iOS 16.7.7.
- All remaining unknown rows carry `unknown_reason` plus `next_action`.
- Transition external IDs are backed by rows in `reports/facebook-messenger/versions.csv`.
- Exact boundaries are adjacent in `reports/facebook-messenger/version-list.json`.
- Final status: done.

## Disk Cleanup

- Checked free space with `df -h .` on 2026-05-25.
- Available space: 240 GiB.
- Deleted IPAs: none.
- Reason: retained sampled and boundary IPAs for reproducibility because disk pressure does not require cleanup.
- Deletion log: `logs/deleted-ipas.log` unchanged for Messenger.
