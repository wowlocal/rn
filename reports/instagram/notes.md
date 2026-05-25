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
- IPAs downloaded: 16
- Unique builds analyzed: 16
- Oldest analyzed build: app version blank, build `1.8.7`, external ID `2948163`, build timestamp `2010-09-27T16:39:00`
- Newest analyzed build: `430.0.0 (972915403)`, external ID `885526725`, build timestamp `2026-05-16T18:55:26`
- RN markers detected: yes, from sampled `10.10.0 (50667367)` through `104.0 (164599121)`, with an observed marker-band change from `<=0.59.x` to `0.60.x`

| External ID | App version | Build | Build timestamp | JS bundle | RN guess | Confidence |
|---|---|---:|---|---|---|---|
| `2948163` |  | 1.8.7 | 2010-09-27T16:39:00 | no | unknown | low |
| `584942731` | 5.0.11 | 2447659 | 2013-10-04T02:08:30 | no | unknown | low |
| `813610568` | 7.7.2 | 15484445 | 2015-09-30T21:36:32 | no | unknown | low |
| `816877594` | 7.19.1 | 26398067 | 2016-03-28T12:45:08 | no | unknown | low |
| `818795448` | 9.3.0 | 38579444 | 2016-09-09T08:29:54 | no | unknown | low |
| `821056195` | 10.10.0 | 50667367 | 2017-02-23T14:15:16 | `Payload/Instagram.app/main.jsbundle` | <=0.59.x | medium |
| `828138988` | 58.0 | 120248682 | 2018-08-09T18:31:38 | `Payload/Instagram.app/main.jsbundle` | <=0.59.x | medium |
| `830905744` | 89.0 | 149781277 | 2019-04-11T15:07:06 | `Payload/Instagram.app/main.jsbundle` | <=0.59.x | medium |
| `832101581` | 104.0 | 164599121 | 2019-07-26T13:33:40 | `Payload/Instagram.app/main.jsbundle` | 0.60.x | medium |
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
| <=0.59.x |  | medium | 10.10.0 (50667367), `821056195`, `2017-02-23T14:15:16` | 89.0 (149781277), `830905744`, `2019-04-11T15:07:06` | 3 |
| 0.60.x |  | medium | 104.0 (164599121), `832101581`, `2019-07-26T13:33:40` | 104.0 (164599121), `832101581`, `2019-07-26T13:33:40` | 1 |
| unknown |  | low | 118.0 (180988914), `833368709`, `2019-11-01T17:18:24` | 430.0.0 (972915403), `885526725`, `2026-05-16T18:55:26` | 7 |

## Unresolved Gaps

- The RN-introduction window is between sampled external IDs `818795448` and `821056195`.
- The RN `<=0.59.x` -> `0.60.x` marker-band upgrade window is between sampled external IDs `830905744` and `832101581`.
- The RN-removal or marker-disappearance window is between sampled external IDs `832101581` and `833368709`.
- Exact RN patch versions are not recoverable from encrypted native binaries; the detected builds are JS-marker band estimates.

## Next Step

Refine the three Instagram boundary windows by downloading midpoint or adjacent versions between `818795448` -> `821056195`, `830905744` -> `832101581`, and `832101581` -> `833368709`.
