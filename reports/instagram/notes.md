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
- RN markers detected: yes, from `10.0.0 (44114773)` through `113.0 (174653610)`, with observed marker-band changes from `<=0.59.x` to `0.60.x` to `0.61.x`
- Full row-level evidence is in `reports/instagram/versions.csv` and `reports/instagram/versions.json`.
- Duplicate external IDs `831095391` and `831129706` both map to `91.0 (151989260)`; duplicate external IDs `832266212` and `832333184` both map to `106.0 (166752244)`. Range starts use the earliest duplicate external ID so transition gaps match App Store ordering.

## Exact RN Transitions

| From | To | Version-list gap |
|---|---|---:|
| unknown at `9.7.0 (43028597)`, external ID `819447240` | `<=0.59.x` at `10.0.0 (44114773)`, external ID `819646349` | 0 |
| `<=0.59.x` at `90.0 (150975176)`, external ID `830989899` | `0.60.x` at `91.0 (151989260)`, external ID `831095391` | 0 |
| `0.60.x` at `105.0 (165586599)`, external ID `832184604` | `0.61.x` at `106.0 (166752244)`, external ID `832266212` | 0 |
| `0.61.x` at `113.0 (174653610)`, external ID `832888376` | unknown at `114.0 (176133011)`, external ID `832986604` | 0 |

## RN Ranges

| RN guess | Renderer | Confidence | Start | End | Builds |
|---|---:|---|---|---|---:|
| unknown |  | low | build 1.8.7, `2948163`, `2010-09-27T16:39:00` | 9.7.0 (43028597), `819447240`, `2016-11-03T10:43:20` | 9 |
| <=0.59.x |  | medium | 10.0.0 (44114773), `819646349`, `2016-11-17T12:37:44` | 90.0 (150975176), `830989899`, `2019-04-19T17:03:30` | 6 |
| 0.60.x |  | medium | 91.0 (151989260), `831095391`, `2019-04-27T03:34:08` | 105.0 (165586599), `832184604`, `2019-08-01T19:22:40` | 5 |
| 0.61.x |  | medium | 106.0 (166752244), `832266212`, `2019-08-09T18:53:36` | 113.0 (174653610), `832888376`, `2019-09-26T18:11:26` | 5 |
| unknown |  | low | 114.0 (176133011), `832986604`, `2019-10-04T17:27:40` | 430.0.0 (972915403), `885526725`, `2026-05-16T18:55:26` | 9 |

## Cleanup and Validation

- Disk cleanup reviewed on 2026-05-26; no Instagram IPAs were deleted because `ipas/instagram` used 3.7 GiB and the filesystem still had 236 GiB available.
- Validation passed on 2026-05-26: scripts compile, Instagram CSV/JSON reports parse, and all four transition rows are adjacent in `version-list.json`.
- Exact RN patch versions are not recoverable from encrypted native binaries; the detected builds are JS-marker band estimates.
