# Instagram iOS React Native Timeline

## Registration

- App name: Instagram
- App Store ID: 389801252
- Bundle ID: com.burbn.instagram
- Status: sampled
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

## Initial Sampling

- Sampling date: 2026-05-26
- IPAs downloaded: 19
- Unique builds analyzed: 19
- Oldest analyzed build: app version blank, build `1.8.7`, external ID `2948163`, build timestamp `2010-09-27T16:39:00`
- Newest analyzed build: `430.0.0 (972915403)`, external ID `885526725`, build timestamp `2026-05-16T18:55:26`
- RN markers detected: yes, from sampled `10.0.1 (44338396)` through `111.0 (172467877)`, with observed marker-band changes from `<=0.59.x` to `0.60.x` to `0.61.x`

| External ID | App version | Build | Build timestamp | JS bundle | RN guess | Confidence |
|---|---|---:|---|---|---|---|
| `2948163` |  | 1.8.7 | 2010-09-27T16:39:00 | no | unknown | low |
| `584942731` | 5.0.11 | 2447659 | 2013-10-04T02:08:30 | no | unknown | low |
| `813610568` | 7.7.2 | 15484445 | 2015-09-30T21:36:32 | no | unknown | low |
| `816877594` | 7.19.1 | 26398067 | 2016-03-28T12:45:08 | no | unknown | low |
| `818795448` | 9.3.0 | 38579444 | 2016-09-09T08:29:54 | no | unknown | low |
| `819837266` | 10.0.1 | 44338396 | 2016-11-21T09:39:06 | `Payload/Instagram.app/main.jsbundle` | <=0.59.x | medium |
| `821056195` | 10.10.0 | 50667367 | 2017-02-23T14:15:16 | `Payload/Instagram.app/main.jsbundle` | <=0.59.x | medium |
| `828138988` | 58.0 | 120248682 | 2018-08-09T18:31:38 | `Payload/Instagram.app/main.jsbundle` | <=0.59.x | medium |
| `830905744` | 89.0 | 149781277 | 2019-04-11T15:07:06 | `Payload/Instagram.app/main.jsbundle` | <=0.59.x | medium |
| `831543078` | 96.1 | 157574695 | 2019-06-04T22:54:00 | `Payload/Instagram.app/main.jsbundle` | 0.60.x | medium |
| `832101581` | 104.0 | 164599121 | 2019-07-26T13:33:40 | `Payload/Instagram.app/main.jsbundle` | 0.60.x | medium |
| `832777026` | 111.0 | 172467877 | 2019-09-14T05:14:24 | `Payload/Instagram.app/main.jsbundle` | 0.61.x | medium |
| `833368709` | 118.0 | 180988914 | 2019-11-01T17:18:24 | no | unknown | low |
| `840589643` | 177.0 | 275424340 | 2020-12-02T23:43:04 | no | unknown | low |
| `849384047` | 236.1 | 372089098 | 2022-05-12T00:11:44 | no | unknown | low |
| `858142473` | 290.1 | 491279855 | 2023-07-21T02:02:50 | no | unknown | low |
| `867327376` | 340.0.10 | 622957927 | 2024-07-09T00:44:42 | no | unknown | low |
| `875444719` | 385.0.0 | 748614773 | 2025-06-11T02:04:38 | no | unknown | low |
| `885526725` | 430.0.0 | 972915403 | 2026-05-16T18:55:26 | no | unknown | low |

## RN Ranges

| RN guess | Renderer | Confidence | Start | End | Builds |
|---|---:|---|---|---|---:|
| unknown |  | low | build 1.8.7, `2948163`, `2010-09-27T16:39:00` | 9.3.0 (38579444), `818795448`, `2016-09-09T08:29:54` | 5 |
| <=0.59.x |  | medium | 10.0.1 (44338396), `819837266`, `2016-11-21T09:39:06` | 89.0 (149781277), `830905744`, `2019-04-11T15:07:06` | 4 |
| 0.60.x |  | medium | 96.1 (157574695), `831543078`, `2019-06-04T22:54:00` | 104.0 (164599121), `832101581`, `2019-07-26T13:33:40` | 2 |
| 0.61.x |  | medium | 111.0 (172467877), `832777026`, `2019-09-14T05:14:24` | 111.0 (172467877), `832777026`, `2019-09-14T05:14:24` | 1 |
| unknown |  | low | 118.0 (180988914), `833368709`, `2019-11-01T17:18:24` | 430.0.0 (972915403), `885526725`, `2026-05-16T18:55:26` | 7 |

## Unresolved Gaps

- The RN-introduction window is between sampled external IDs `818795448` and `819837266`.
- The RN `<=0.59.x` -> `0.60.x` marker-band upgrade window is between sampled external IDs `830905744` and `831543078`.
- The RN `0.60.x` -> `0.61.x` marker-band upgrade window is between sampled external IDs `832101581` and `832777026`.
- The RN-removal or marker-disappearance window is between sampled external IDs `832777026` and `833368709`.
- Exact RN patch versions are not recoverable from encrypted native binaries; the detected builds are JS-marker band estimates.

## Next Step

Refine the four Instagram boundary windows by downloading midpoint or adjacent versions between `818795448` -> `819837266`, `830905744` -> `831543078`, `832101581` -> `832777026`, and `832777026` -> `833368709`.
