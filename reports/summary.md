# Popular React Native iOS Apps Timeline Summary

## Methodology

Reports use IPA internal zip timestamps from app bundle `Info.plist` members unless an App Store date is independently verified. Exact RN patch versions are reported only when strong markers are exposed; encrypted native binaries generally limit results to RN version bands inferred from JS bundle markers.

## App Status

- Analyzed successfully: 1
- Needs manual review: 0
- Skipped: 0

## Analyzed Apps

- Discord: 475 external versions; reports in `reports/discord`

## RN Ranges

| App | RN guess | Renderer | Confidence | Start | End | Builds |
|---|---|---:|---|---|---|---:|
| Discord | <=0.59.x |  | medium | 1.0 (4) | 3.1.10 (18953) | 8 |
| Discord | 0.61.x |  | medium | 3.2.0 (19099) | 20.0 (19811) | 8 |
| Discord | 0.62.x |  | medium | 21.0 (19965) | 87.0 (27320) | 8 |
| Discord | 0.64.x |  | medium | 88.2 (27527) | 106.0 (29538) | 16 |
| Discord | 0.66.x |  | medium | 109.0 (29659) | 132.0 (33253) | 4 |
| Discord | 0.67.x-0.68.x |  | medium | 133.0 (33358) | 162.0 (39121) | 7 |
| Discord | 0.69.x-0.70.x |  | medium | 163.0 (39243) | 190.0 (47418) | 7 |
| Discord | 0.71.x |  | medium | 191.0 (47806) | 245.0 (63641) | 9 |
| Discord | 0.74.x-0.76.x |  | medium | 246.0 (63933) | 279.0 (77189) | 42 |
| Discord | 0.78.x | 19.0.0 | high | 280.0 (77565) | 306.1 (89123) | 31 |
| Discord | 0.81.x | 19.1.0 | high | 307.0 (89215) | 329.0 (100971) | 33 |

## RN Transitions

| App | From | To | Last old | First new | Version-list gap |
|---|---|---|---|---|---:|
| Discord | <=0.59.x | 0.61.x | 3.1.10 (18953) | 3.2.0 (19099) | 0 |
| Discord | 0.61.x | 0.62.x | 20.0 (19811) | 21.0 (19965) | 0 |
| Discord | 0.62.x | 0.64.x | 87.0 (27320) | 88.2 (27527) | 2 |
| Discord | 0.64.x | 0.66.x | 106.0 (29538) | 109.0 (29659) | 0 |
| Discord | 0.66.x | 0.67.x-0.68.x | 132.0 (33253) | 133.0 (33358) | 0 |
| Discord | 0.67.x-0.68.x | 0.69.x-0.70.x | 162.0 (39121) | 163.0 (39243) | 0 |
| Discord | 0.69.x-0.70.x | 0.71.x | 190.0 (47418) | 191.0 (47806) | 0 |
| Discord | 0.71.x | 0.74.x-0.76.x | 245.0 (63641) | 246.0 (63933) | 0 |
| Discord | 0.74.x-0.76.x | 0.78.x | 279.0 (77189) | 280.0 (77565) | 0 |
| Discord | 0.78.x | 0.81.x | 306.1 (89123) | 307.0 (89215) | 0 |

## Boundary Confidence

- Exact by transition IDs: 9
- Approximate by transition IDs: 1
- Per-app notes may refine duplicate-build boundary cases where multiple external IDs map to the same app build.
