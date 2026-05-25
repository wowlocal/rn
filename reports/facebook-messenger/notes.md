# Facebook Messenger iOS React Native Timeline

## Registration

- App name: Facebook Messenger
- App Store ID: 454638411
- Bundle ID: com.facebook.Messenger
- Status: sampled
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

- IPAs downloaded: 18
- Unique builds analyzed: 18
- Oldest analyzed build: app version blank, build `1000`, external ID `4003333`, build timestamp `2011-08-02T21:45:38`
- Newest analyzed build: `562.0.0 (975021560)`, external ID `885556428`, build timestamp `2026-05-19T17:01:04`
- RN markers detected: yes, from sampled `98.0 (44186053)` through `145.0 (82143310)`

| External ID | App version | Build | Build timestamp | JS bundle | RN guess | Confidence |
|---|---|---:|---|---|---|---|
| `4003333` |  | 1000 | 2011-08-02T21:45:38 | no | unknown | low |
| `812231857` | 26.0 | 9347487 | 2014-07-28T20:42:06 | no | unknown | low |
| `816903024` | 65.0 | 27013135 | 2016-04-04T17:23:02 | no | unknown | low |
| `818196039` | 81.0 | 34694251 | 2016-07-25T14:07:34 | no | unknown | low |
| `818893675` | 89.0 | 39433806 | 2016-09-19T14:44:26 | no | unknown | low |
| `819781397` | 98.0 | 44186053 | 2016-11-18T11:12:28 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `823243677` | 131.0 | 68165081 | 2017-08-14T08:58:26 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `824651339` | 145.0 | 82143310 | 2017-11-28T17:09:26 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
| `825927199` | 153.0 | 91923955 | 2018-02-12T20:12:40 | no | unknown | low |
| `826787358` | 163.0 | 104735954 | 2018-04-24T07:01:24 | no | unknown | low |
| `828538485` | 183.0 | 123940704 | 2018-09-11T23:41:04 | no | unknown | low |
| `833799330` | 243.1 | 185914695 | 2019-11-27T12:24:04 | no | unknown | low |
| `838965715` | 291.0 | 256509383 | 2020-10-20T14:56:02 | no | unknown | low |
| `845952569` | 342.0 | 338823778 | 2021-12-10T00:40:28 | no | unknown | low |
| `854961972` | 396.1 | 446890740 | 2023-02-16T22:36:16 | no | unknown | low |
| `864747553` | 452.0.0 | 583923274 | 2024-03-28T16:48:02 | no | unknown | low |
| `873336561` | 500.0.0 | 713622393 | 2025-03-14T00:36:32 | no | unknown | low |
| `885556428` | 562.0.0 | 975021560 | 2026-05-19T17:01:04 | no | unknown | low |

## RN Ranges

| RN guess | Renderer | Confidence | Start | End | Builds |
|---|---:|---|---|---|---:|
| unknown |  | low | build 1000, `4003333`, `2011-08-02T21:45:38` | 89.0 (39433806), `818893675`, `2016-09-19T14:44:26` | 5 |
| <=0.59.x |  | medium | 98.0 (44186053), `819781397`, `2016-11-18T11:12:28` | 145.0 (82143310), `824651339`, `2017-11-28T17:09:26` | 3 |
| unknown |  | low | 153.0 (91923955), `825927199`, `2018-02-12T20:12:40` | 562.0.0 (975021560), `885556428`, `2026-05-19T17:01:04` | 10 |

## Unresolved Gaps

- The RN-introduction window is between sampled external IDs `818893675` and `819781397`.
- The RN-removal or marker-disappearance window is between sampled external IDs `824651339` and `825927199`.
- Exact RN patch versions are not recoverable from encrypted native binaries; the detected build is a JS-marker band estimate.

## Next Step

Refine the two Messenger boundary windows by downloading midpoint or adjacent versions between `818893675` -> `819781397` and `824651339` -> `825927199`.
