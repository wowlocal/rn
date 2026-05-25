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

- IPAs downloaded: 12
- Unique builds analyzed: 12
- Oldest analyzed build: app version blank, build `1000`, external ID `4003333`, build timestamp `2011-08-02T21:45:38`
- Newest analyzed build: `562.0.0 (975021560)`, external ID `885556428`, build timestamp `2026-05-19T17:01:04`
- RN markers detected: yes, in `131.0 (68165081)`, external ID `823243677`

| External ID | App version | Build | Build timestamp | JS bundle | RN guess | Confidence |
|---|---|---:|---|---|---|---|
| `4003333` |  | 1000 | 2011-08-02T21:45:38 | no | unknown | low |
| `812231857` | 26.0 | 9347487 | 2014-07-28T20:42:06 | no | unknown | low |
| `816903024` | 65.0 | 27013135 | 2016-04-04T17:23:02 | no | unknown | low |
| `823243677` | 131.0 | 68165081 | 2017-08-14T08:58:26 | `Payload/Messenger.app/main.jsbundle` | <=0.59.x | medium |
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
| unknown |  | low | build 1000, `4003333`, `2011-08-02T21:45:38` | 65.0 (27013135), `816903024`, `2016-04-04T17:23:02` | 3 |
| <=0.59.x |  | medium | 131.0 (68165081), `823243677`, `2017-08-14T08:58:26` | 131.0 (68165081), `823243677`, `2017-08-14T08:58:26` | 1 |
| unknown |  | low | 183.0 (123940704), `828538485`, `2018-09-11T23:41:04` | 562.0.0 (975021560), `885556428`, `2026-05-19T17:01:04` | 8 |

## Unresolved Gaps

- The RN-introduction window is between sampled external IDs `816903024` and `823243677`.
- The RN-removal or marker-disappearance window is between sampled external IDs `823243677` and `828538485`.
- Exact RN patch versions are not recoverable from encrypted native binaries; the detected build is a JS-marker band estimate.

## Next Step

Refine the two Messenger boundary windows by downloading midpoint or adjacent versions between `816903024` -> `823243677` and `823243677` -> `828538485`.
