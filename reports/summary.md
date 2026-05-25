# Popular React Native Mobile Apps Timeline Summary

## Methodology

Reports keep platform-specific package timelines separate, then merge them here with platform labels. iOS reports use IPA internal zip timestamps from app bundle `Info.plist` members unless an App Store date is independently verified. Android APK/APKS/XAPK/APKM analysis is first-class evidence when packages are available, with Android ordering based on versionCode and source publish dates when available. Exact RN patch versions are reported only when strong markers are exposed; encrypted native binaries generally limit results to RN version bands inferred from JS bundle markers.

## App Status

- Analyzed successfully: 3
- Queued: 0
- In progress: 0
- Needs manual review: 1
- Skipped: 1

## Analyzed Apps

- Discord: 475 iOS external versions; reports in `reports/discord`
- Facebook Messenger: 735 iOS external versions; reports in `reports/facebook-messenger`
- Instagram: 795 iOS external versions; reports in `reports/instagram`

## Skipped Apps

- Facebook: Registered for analysis on 2026-05-25.; RN usage was not verified because ipatool list-versions failed before sampling.; ipatool list-versions failed for both app ID 284882215 and bundle ID com.facebook.Facebook with Apple's generic unknown error.; ipatool purchase also failed with unsupported protocol scheme before a license could be obtained.

## RN Ranges

| App | Platform | RN guess | Renderer | Confidence | Start | End | Builds |
|---|---|---|---:|---|---|---|---:|
| Discord | ios | <=0.59.x |  | medium | 1.0 (4) | 3.1.10 (18953) | 8 |
| Discord | ios | 0.61.x |  | medium | 3.2.0 (19099) | 20.0 (19811) | 8 |
| Discord | ios | 0.62.x |  | medium | 21.0 (19965) | 87.0 (27320) | 8 |
| Discord | ios | 0.64.x |  | medium | 88.2 (27527) | 106.0 (29538) | 16 |
| Discord | ios | 0.66.x |  | medium | 109.0 (29659) | 132.0 (33253) | 4 |
| Discord | ios | 0.67.x-0.68.x |  | medium | 133.0 (33358) | 162.0 (39121) | 7 |
| Discord | ios | 0.69.x-0.70.x |  | medium | 163.0 (39243) | 190.0 (47418) | 7 |
| Discord | ios | 0.71.x |  | medium | 191.0 (47806) | 245.0 (63641) | 9 |
| Discord | ios | 0.74.x-0.76.x |  | medium | 246.0 (63933) | 279.0 (77189) | 42 |
| Discord | ios | 0.78.x | 19.0.0 | high | 280.0 (77565) | 306.1 (89123) | 31 |
| Discord | ios | 0.81.x | 19.1.0 | high | 307.0 (89215) | 329.0 (100971) | 33 |
| Facebook Messenger | ios | unknown |  | low |  (1000) | 91.0 (40546824) | 7 |
| Facebook Messenger | ios | <=0.59.x |  | medium | 92.0 (41023043) | 147.0 (84235609) | 7 |
| Facebook Messenger | ios | unknown |  | low | 148.0 (86952252) | 562.0.0 (975021560) | 12 |
| Instagram | ios | unknown |  | low |  (1.8.7) | 9.7.0 (43028597) | 9 |
| Instagram | ios | <=0.59.x |  | medium | 10.0.0 (44114773) | 90.0 (150975176) | 6 |
| Instagram | ios | 0.60.x |  | medium | 91.0 (151989260) | 105.0 (165586599) | 5 |
| Instagram | ios | 0.61.x |  | medium | 106.0 (166752244) | 113.0 (174653610) | 5 |
| Instagram | ios | unknown |  | low | 114.0 (176133011) | 430.0.0 (972915403) | 9 |
| Threads | ios | unknown |  | low | 289.0 (489338310) | 431.0.0 (979167741) | 12 |
| Threads | android | unknown |  | low | 374.0.0.43.110 (504412928) | 382.0.0.51.85 (505205644) | 2 |
| Threads | android | unknown |  | unknown | 400.0.0.38.68 (507007017) | 430.0.0.46.79 (510007506) | 10 |

## RN Transitions

| App | Platform | From | To | Last old | First new | Version-list gap |
|---|---|---|---|---|---|---:|
| Discord | ios | <=0.59.x | 0.61.x | 3.1.10 (18953) | 3.2.0 (19099) | 0 |
| Discord | ios | 0.61.x | 0.62.x | 20.0 (19811) | 21.0 (19965) | 0 |
| Discord | ios | 0.62.x | 0.64.x | 87.0 (27320) | 88.2 (27527) | 2 |
| Discord | ios | 0.64.x | 0.66.x | 106.0 (29538) | 109.0 (29659) | 0 |
| Discord | ios | 0.66.x | 0.67.x-0.68.x | 132.0 (33253) | 133.0 (33358) | 0 |
| Discord | ios | 0.67.x-0.68.x | 0.69.x-0.70.x | 162.0 (39121) | 163.0 (39243) | 0 |
| Discord | ios | 0.69.x-0.70.x | 0.71.x | 190.0 (47418) | 191.0 (47806) | 0 |
| Discord | ios | 0.71.x | 0.74.x-0.76.x | 245.0 (63641) | 246.0 (63933) | 0 |
| Discord | ios | 0.74.x-0.76.x | 0.78.x | 279.0 (77189) | 280.0 (77565) | 0 |
| Discord | ios | 0.78.x | 0.81.x | 306.1 (89123) | 307.0 (89215) | 0 |
| Facebook Messenger | ios | unknown | <=0.59.x | 91.0 (40546824) | 92.0 (41023043) | 0 |
| Facebook Messenger | ios | <=0.59.x | unknown | 147.0 (84235609) | 148.0 (86952252) | 0 |
| Instagram | ios | unknown | <=0.59.x | 9.7.0 (43028597) | 10.0.0 (44114773) | 0 |
| Instagram | ios | <=0.59.x | 0.60.x | 90.0 (150975176) | 91.0 (151989260) | 0 |
| Instagram | ios | 0.60.x | 0.61.x | 105.0 (165586599) | 106.0 (166752244) | 0 |
| Instagram | ios | 0.61.x | unknown | 113.0 (174653610) | 114.0 (176133011) | 0 |
| Threads | android | unknown | unknown | 382.0.0.51.85 (505205644) | 400.0.0.38.68 (507007017) | 0 |

## Boundary Confidence

- Exact by transition IDs: 16
- Approximate by transition IDs: 1
- Per-app notes may refine duplicate-build boundary cases where multiple external IDs map to the same app build.
