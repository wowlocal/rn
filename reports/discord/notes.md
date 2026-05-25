# Discord iOS React Native Timeline

## App Identity

- App name: Discord
- App Store ID: 985746746
- Bundle ID: com.hammerandchisel.discord
- Source for checking: candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`; RN usage verified by IPA JS bundle markers in `reports/discord/versions.csv`.

## Coverage

- External version IDs available: 475 (`812213284` through `885730983`)
- IPAs analyzed: 198
- Unique app builds analyzed after dedupe: 173
- Oldest analyzed build: `1.0 (4)`, build timestamp `2015-05-13T19:15:24`
- Newest analyzed build: `329.0 (100971)`, build timestamp `2026-05-15T06:40:04`
- Version timestamps are IPA internal zip timestamps from each app bundle `Info.plist` member.

## RN Detection Evidence

The analysis uses JS bundle markers because the native executables are FairPlay encrypted (`cryptid=1`) in the analyzed IPAs. Exact native React Native constants are therefore not inspectable.

Primary markers include `react-native-renderer` versions when present, Hermes bytecode versions, and RN JS API/index export markers such as `unstable_enableLogBox`, `registerCallableModule`, `DevMenu`, `VirtualViewMode`, `useAnimatedValue`, `setUpDOM`, `PlatformColor`, and legacy removed APIs.

## RN Ranges

| RN guess | Renderer | Confidence | Start | End | Builds |
|---|---:|---|---|---|---:|
| <=0.59.x |  | medium | 1.0 (4), `812213284`, `2015-05-13T19:15:24` | 3.1.10 (18953), `834579637`, `2020-02-03T18:56:26` | 8 |
| 0.61.x |  | medium | 3.2.0 (19099), `834665919`, `2020-02-18T17:49:32` | 20.0 (19811), `835787821`, `2020-05-01T17:54:02` | 8 |
| 0.62.x |  | medium | 21.0 (19965), `835876880`, `2020-05-11T15:12:08` | 87.0 (27320), `843583012`, `2021-08-13T00:18:36` | 8 |
| 0.64.x |  | medium | 88.2 (27527), `843764890`, `2021-08-24T07:52:16` | 106.0 (29538), `845885357`, `2021-12-17T15:06:46` | 16 |
| 0.66.x |  | medium | 109.0 (29659), `846473402`, `2022-01-05T18:20:42` | 132.0 (33253), `850254827`, `2022-06-17T14:35:50` | 4 |
| 0.67.x-0.68.x |  | medium | 133.0 (33358), `850422831`, `2022-06-24T16:31:00` | 162.0 (39121), `854555328`, `2023-01-23T12:17:36` | 7 |
| 0.69.x-0.70.x |  | medium | 163.0 (39243), `854627233`, `2023-01-26T23:47:56` | 190.0 (47418), `858815116`, `2023-08-04T14:22:38` | 7 |
| 0.71.x |  | medium | 191.0 (47806), `859116718`, `2023-08-10T23:49:32` | 245.0 (63641), `868632088`, `2024-08-31T00:07:40` | 9 |
| 0.74.x-0.76.x |  | medium | 246.0 (63933), `868825701`, `2024-09-06T22:43:46` | 279.0 (77189), `874658173`, `2025-05-09T06:38:08` | 42 |
| 0.78.x | 19.0.0 | high | 280.0 (77565), `874850406`, `2025-05-16T06:36:48` | 306.1 (89123), `880053648`, `2025-11-24T22:28:44` | 31 |
| 0.81.x | 19.1.0 | high | 307.0 (89215), `880126085`, `2025-11-26T07:48:16` | 329.0 (100971), `885730983`, `2026-05-15T06:40:04` | 33 |

## Transition Audit

All upgrade boundaries in the full analyzed row set are adjacent in `reports/discord/version-list.json`. The preserved legacy transition table deduplicates by build and keeps the highest external version ID for repeated builds; because of that, the 0.62.x -> 0.64.x legacy row shows two intervening external IDs (`843713142`, `843748771`) that are already analyzed copies of the first 0.64.x app build.

| From RN | Last old | To RN | First new | Boundary |
|---|---|---|---|---|
| <=0.59.x | 3.1.10 (18953), `834579637` | 0.61.x | 3.2.0 (19099), `834665919` | exact |
| 0.61.x | 20.0 (19811), `835787821` | 0.62.x | 21.0 (19965), `835876880` | exact |
| 0.62.x | 87.0 (27320), `843583012` | 0.64.x | 88.2 (27527), first analyzed `843713142` | exact; legacy first-new ID is `843764890` |
| 0.64.x | 106.0 (29538), `845885357` | 0.66.x | 109.0 (29659), `846473402` | exact |
| 0.66.x | 132.0 (33253), `850254827` | 0.67.x-0.68.x | 133.0 (33358), `850422831` | exact |
| 0.67.x-0.68.x | 162.0 (39121), `854555328` | 0.69.x-0.70.x | 163.0 (39243), `854627233` | exact |
| 0.69.x-0.70.x | 190.0 (47418), `858815116` | 0.71.x | 191.0 (47806), `859116718` | exact |
| 0.71.x | 245.0 (63641), `868632088` | 0.74.x-0.76.x | 246.0 (63933), `868825701` | exact |
| 0.74.x-0.76.x | 279.0 (77189), `874658173` | 0.78.x | 280.0 (77565), `874850406` | exact |
| 0.78.x | 306.1 (89123), `880053648` | 0.81.x | 307.0 (89215), `880126085` | exact |

## App-Specific Quirks

- Many App Store external version IDs map to repeated app version/build pairs. The timeline summary deduplicates by app build for range tables.
- React renderer markers appear in newer Hermes bundles starting with the detected 0.78.x range. Older ranges rely on RN JS API marker bands and are reported as version bands rather than exact patch versions.
