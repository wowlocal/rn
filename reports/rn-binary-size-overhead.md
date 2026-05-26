# React Native Binary Size Overhead From Decrypted iOS Dumps

## Scope

- Accepted decrypted dump rows analyzed: 29
- Apps represented: 11
- Dump IPAs are local evidence under `tmp/ios-dumps`; they are not committed.
- `direct_rn_payload_bytes` is an RN-associated packaging floor: JS/Hermes bundle files plus separately named React Native/Hermes/JSI/Yoga native artifacts in the primary app bundle.
- JS/Hermes bundle bytes include app/product JavaScript as well as framework/runtime glue, so they are not pure React Native framework overhead.
- `rn_named_native_bytes` is the closer framework/runtime signal when RN/Hermes/JSI/Yoga ship as separately named binaries.
- Many iOS apps statically link React Native into the main executable. For those, exact RN-only native bytes cannot be separated from app code without link maps or symbol-level attribution, so `rn_carrier_macho_bytes` reports the containing Mach-O size as context, not as direct overhead.
- Rows with no current RN evidence are retained as controls and should not be interpreted as RN overhead.

## Observations

- RN-positive rows: 22; static-linked rows with no separable RN artifacts: 9; negative/control rows: 7.
- Largest RN-associated packaging floors:
  - Coinbase `14.19.22 (14190022)`: 104.7 MiB (41.25% of primary app uncompressed bytes; 100.1 MiB JS / 4.5 MiB native).
  - Coinbase `13.45.27 (13450027)`: 93.7 MiB (35.76% of primary app uncompressed bytes; 89.2 MiB JS / 4.5 MiB native).
  - Coinbase `13.44.24 (13440024)`: 93.0 MiB (35.63% of primary app uncompressed bytes; 88.5 MiB JS / 4.5 MiB native).
  - Shopify `10.2621.0 (282789)`: 47.8 MiB (26.74% of primary app uncompressed bytes; 42.0 MiB JS / 5.8 MiB native).
  - Shopify `10.2606.0 (222553)`: 42.7 MiB (25.58% of primary app uncompressed bytes; 36.9 MiB JS / 5.8 MiB native).
- Static-linked RN rows can have a zero direct-artifact floor; the largest carrier context is 123.3 MiB in Threads `431.0.0 (979167741)`.
- Largest separately named native RN/Hermes/JSI/Yoga runtime payloads:
  - Shopify `10.2606.0 (222553)`: 5.8 MiB native runtime bytes across 1 file(s).
  - Shopify `10.2621.0 (282789)`: 5.8 MiB native runtime bytes across 1 file(s).
  - Artsy: Buy & Sell Fine Art `9.9.0 (2026.05.20.12.45)`: 4.6 MiB native runtime bytes across 1 file(s).
  - Coinbase `13.44.24 (13440024)`: 4.5 MiB native runtime bytes across 1 file(s).
  - Coinbase `13.45.27 (13450027)`: 4.5 MiB native runtime bytes across 1 file(s).
- Largest JS/Hermes bundle payloads:
  - Coinbase `14.19.22 (14190022)`: 100.1 MiB uncompressed (35.9 MiB compressed).
  - Coinbase `13.45.27 (13450027)`: 89.2 MiB uncompressed (31.2 MiB compressed).
  - Coinbase `13.44.24 (13440024)`: 88.5 MiB uncompressed (31.0 MiB compressed).
  - Shopify `10.2621.0 (282789)`: 42.0 MiB uncompressed (15.3 MiB compressed).
  - Shopify `10.2606.0 (222553)`: 36.9 MiB uncompressed (14.3 MiB compressed).
- No RN overhead is attributed to current negative/control rows: Agoda: Cheap Flights & Hotels, SoundCloud: The Music You Love, Uber Eats: Food & Groceries.

## Per-Dump Results

| App | Version | RN evidence | RN-associated payload | Split | Direct % of app | RN carrier Mach-O | Coverage | Notes |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- |
| Agoda: Cheap Flights & Hotels | `13.40.0 (310516.2)` | no_rn_detected | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 0.0 MiB | loaded_app_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers |
| Threads | `373.0.0 (711845629)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 61.0 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Threads | `387.0.0 (755202338)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 74.7 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Threads | `400.0.0 (797742903)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 83.5 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Threads | `431.0.0 (979167741)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 123.3 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Instagram | `114.0 (176133011)` | 0.61.x | 0.9 MiB | 0.9 MiB JS / 0.0 MiB native | 0.86% | 19.1 MiB | main_only_decrypted | remaining encrypted non-extension Mach-O may hide additional bytes |
| Instagram | `430.0.0 (972915403)` | native_rn_marker_without_version | 2.2 MiB | 2.2 MiB JS / 0.0 MiB native | 0.52% | 329.8 MiB | loaded_app_decrypted | native_rn_marker_without_version |
| Facebook Messenger | `562.0.0 (975021560)` | native_rn_marker_without_version | 1.6 MiB | 1.6 MiB JS / 0.0 MiB native | 0.88% | 96.6 MiB | main_only_decrypted | native_rn_marker_without_version remaining encrypted non-extension Mach-O may hide additional bytes |
| Shopify | `10.2606.0 (222553)` | 0.82.x or newer | 42.7 MiB | 36.9 MiB JS / 5.8 MiB native | 25.58% | 36.7 MiB | main_only_decrypted | remaining encrypted non-extension Mach-O may hide additional bytes |
| Shopify | `10.2621.0 (282789)` | 0.82.x or newer | 47.8 MiB | 42.0 MiB JS / 5.8 MiB native | 26.74% | 39.0 MiB | main_only_decrypted | remaining encrypted non-extension Mach-O may hide additional bytes |
| Mattermost | `2.40.0 (749)` | 0.77.x | 32.9 MiB | 28.4 MiB JS / 4.5 MiB native | 42.71% | 4.5 MiB |  | accepted dump predates decrypted coverage classification |
| Skype | `8.150.3125 (8.150.0.125)` | 0.71.x | 34.5 MiB | 30.1 MiB JS / 4.3 MiB native | 20.61% | 64.9 MiB | loaded_app_decrypted |  |
| Skype | `8.79.92 (8.79.0.92)` | 0.63.x | 18.2 MiB | 18.2 MiB JS / 0.0 MiB native | 15.01% | 66.1 MiB | loaded_app_decrypted |  |
| Skype | `8.97.3203 (8.97.0.203)` | 0.71.x | 20.5 MiB | 20.5 MiB JS / 0.0 MiB native | 21.32% | 45.5 MiB | loaded_app_decrypted |  |
| SoundCloud: The Music You Love | `7.16.0 (1243764)` | no_rn_detected | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 0.0 MiB | loaded_app_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers |
| SoundCloud: The Music You Love | `7.44.0 (1248257)` | no_rn_detected | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| SoundCloud: The Music You Love | `8.32.0 (1254310)` | no_rn_detected | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| SoundCloud: The Music You Love | `8.5.0 (1251600)` | no_rn_detected | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| SoundCloud: The Music You Love | `8.62.0 (1259079)` | no_rn_detected | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| Uber Eats: Food & Groceries | `6.281.10000 (6.281.10000)` | no_rn_detected | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| Coinbase | `13.44.24 (13440024)` | 0.79.x | 93.0 MiB | 88.5 MiB JS / 4.5 MiB native | 35.63% | 75.1 MiB | loaded_app_decrypted |  |
| Coinbase | `13.45.27 (13450027)` | 0.60.x | 93.7 MiB | 89.2 MiB JS / 4.5 MiB native | 35.76% | 75.1 MiB | loaded_app_decrypted |  |
| Coinbase | `14.19.22 (14190022)` | 0.60.x | 104.7 MiB | 100.1 MiB JS / 4.5 MiB native | 41.25% | 56.4 MiB | loaded_app_decrypted |  |
| Artsy: Buy & Sell Fine Art | `7.3.5 (2022.04.22.16)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 12.7 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.6 (2022.05.11.16)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 12.8 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.7 (2022.05.25.17)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 12.8 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.8 (2022.05.29.23)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 12.8 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.9 (2022.06.03.16)` | native_rn_marker_without_version | 0.0 MiB | 0.0 MiB JS / 0.0 MiB native | 0.00% | 12.6 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `9.9.0 (2026.05.20.12.45)` | 0.81.x | 16.5 MiB | 11.9 MiB JS / 4.6 MiB native | 16.47% | 44.1 MiB | loaded_app_decrypted |  |

## Component Breakdown

| App | Version | Source IPA | Primary App Uncompressed | Main Executable | JS/Hermes Bundle | Named Native Runtime | Direct Compressed | Files |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Agoda: Cheap Flights & Hotels | `13.40.0 (310516.2)` | 310.6 MiB | 407.6 MiB | 198.8 MiB (48.79%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 0 carrier |
| Threads | `373.0.0 (711845629)` | 62.5 MiB | 78.9 MiB | 61.0 MiB (77.34%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Threads | `387.0.0 (755202338)` | 74.6 MiB | 93.5 MiB | 74.7 MiB (79.82%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Threads | `400.0.0 (797742903)` | 104.5 MiB | 105.6 MiB | 83.5 MiB (79.09%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Threads | `431.0.0 (979167741)` | 154.1 MiB | 146.7 MiB | 123.3 MiB (84.08%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Instagram | `114.0 (176133011)` | 76.6 MiB | 100.5 MiB | 0.2 MiB (0.16%) | 0.9 MiB | 0.0 MiB | 0.9 MiB (1.24% of dump IPA) | 1 JS, 0 native, 2 carrier |
| Instagram | `430.0.0 (972915403)` | 440.2 MiB | 423.3 MiB | 279.4 MiB (66.00%) | 2.2 MiB | 0.0 MiB | 1.1 MiB (0.34% of dump IPA) | 1 JS, 0 native, 2 carrier |
| Facebook Messenger | `562.0.0 (975021560)` | 168.9 MiB | 183.9 MiB | 0.4 MiB (0.21%) | 1.6 MiB | 0.0 MiB | 0.9 MiB (0.70% of dump IPA) | 1 JS, 0 native, 2 carrier |
| Shopify | `10.2606.0 (222553)` | 124.6 MiB | 167.1 MiB | 30.9 MiB (18.50%) | 36.9 MiB | 5.8 MiB | 15.9 MiB (18.23% of dump IPA) | 1 JS, 1 native, 2 carrier |
| Shopify | `10.2621.0 (282789)` | 131.7 MiB | 178.9 MiB | 33.2 MiB (18.53%) | 42.0 MiB | 5.8 MiB | 16.9 MiB (18.18% of dump IPA) | 1 JS, 1 native, 2 carrier |
| Mattermost | `2.40.0 (749)` | 59.0 MiB | 77.1 MiB | 16.5 MiB (21.42%) | 28.4 MiB | 4.5 MiB | 13.2 MiB (26.15% of dump IPA) | 1 JS, 1 native, 0 carrier |
| Skype | `8.150.3125 (8.150.0.125)` | 122.3 MiB | 167.2 MiB | 60.6 MiB (36.21%) | 30.1 MiB | 4.3 MiB | 12.6 MiB (16.38% of dump IPA) | 1 JS, 1 native, 2 carrier |
| Skype | `8.79.92 (8.79.0.92)` | 67.0 MiB | 121.5 MiB | 66.1 MiB (54.37%) | 18.2 MiB | 0.0 MiB | 3.7 MiB (8.45% of dump IPA) | 1 JS, 0 native, 1 carrier |
| Skype | `8.97.3203 (8.97.0.203)` | 64.6 MiB | 96.0 MiB | 45.5 MiB (47.39%) | 20.5 MiB | 0.0 MiB | 4.2 MiB (10.30% of dump IPA) | 1 JS, 0 native, 1 carrier |
| SoundCloud: The Music You Love | `7.16.0 (1243764)` | 117.6 MiB | 199.9 MiB | 15.4 MiB (7.71%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 0 carrier |
| SoundCloud: The Music You Love | `7.44.0 (1248257)` | 210.9 MiB | 268.1 MiB | 20.9 MiB (7.80%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 0 carrier |
| SoundCloud: The Music You Love | `8.32.0 (1254310)` | 197.1 MiB | 192.9 MiB | 25.3 MiB (13.12%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 0 carrier |
| SoundCloud: The Music You Love | `8.5.0 (1251600)` | 189.9 MiB | 183.2 MiB | 22.2 MiB (12.13%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 0 carrier |
| SoundCloud: The Music You Love | `8.62.0 (1259079)` | 202.9 MiB | 219.9 MiB | 19.4 MiB (8.81%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 0 carrier |
| Uber Eats: Food & Groceries | `6.281.10000 (6.281.10000)` | 266.6 MiB | 311.7 MiB | 210.5 MiB (67.53%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 0 carrier |
| Coinbase | `13.44.24 (13440024)` | 143.4 MiB | 261.1 MiB | 66.8 MiB (25.57%) | 88.5 MiB | 4.5 MiB | 32.2 MiB (32.49% of dump IPA) | 1 JS, 1 native, 3 carrier |
| Coinbase | `13.45.27 (13450027)` | 143.7 MiB | 262.0 MiB | 66.8 MiB (25.48%) | 89.2 MiB | 4.5 MiB | 32.5 MiB (32.64% of dump IPA) | 1 JS, 1 native, 3 carrier |
| Coinbase | `14.19.22 (14190022)` | 137.8 MiB | 253.8 MiB | 48.1 MiB (18.97%) | 100.1 MiB | 4.5 MiB | 37.2 MiB (36.95% of dump IPA) | 1 JS, 1 native, 3 carrier |
| Artsy: Buy & Sell Fine Art | `7.3.5 (2022.04.22.16)` | 37.6 MiB | 51.0 MiB | 12.7 MiB (24.96%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Artsy: Buy & Sell Fine Art | `7.3.6 (2022.05.11.16)` | 37.7 MiB | 51.2 MiB | 12.8 MiB (25.03%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Artsy: Buy & Sell Fine Art | `7.3.7 (2022.05.25.17)` | 38.0 MiB | 51.6 MiB | 12.8 MiB (24.87%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Artsy: Buy & Sell Fine Art | `7.3.8 (2022.05.29.23)` | 38.0 MiB | 51.6 MiB | 12.8 MiB (24.84%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Artsy: Buy & Sell Fine Art | `7.3.9 (2022.06.03.16)` | 36.0 MiB | 49.2 MiB | 12.6 MiB (25.71%) | 0.0 MiB | 0.0 MiB | 0.0 MiB (0.00% of dump IPA) | 0 JS, 0 native, 1 carrier |
| Artsy: Buy & Sell Fine Art | `9.9.0 (2026.05.20.12.45)` | 75.0 MiB | 100.3 MiB | 35.7 MiB (35.63%) | 11.9 MiB | 4.6 MiB | 6.4 MiB (13.65% of dump IPA) | 1 JS, 1 native, 3 carrier |

## App-Level Takeaways

- Artsy: Buy & Sell Fine Art: RN-associated payload up to 16.5 MiB (JS/Hermes up to 11.9 MiB, named native runtime up to 4.6 MiB); largest RN carrier Mach-O context 44.1 MiB; latest analyzed row `9.9.0 (2026.05.20.12.45)`; sampled direct delta 16.5 MiB.
- Coinbase: RN-associated payload up to 104.7 MiB (JS/Hermes up to 100.1 MiB, named native runtime up to 4.5 MiB); largest RN carrier Mach-O context 75.1 MiB; latest analyzed row `14.19.22 (14190022)`; sampled direct delta 11.7 MiB.
- Facebook Messenger: RN-associated payload up to 1.6 MiB (JS/Hermes up to 1.6 MiB, named native runtime up to 0.0 MiB); largest RN carrier Mach-O context 96.6 MiB; latest analyzed row `562.0.0 (975021560)`.
- Instagram: RN-associated payload up to 2.2 MiB (JS/Hermes up to 2.2 MiB, named native runtime up to 0.0 MiB); largest RN carrier Mach-O context 329.8 MiB; latest analyzed row `430.0.0 (972915403)`; sampled direct delta 1.3 MiB.
- Mattermost: RN-associated payload up to 32.9 MiB (JS/Hermes up to 28.4 MiB, named native runtime up to 4.5 MiB); largest RN carrier Mach-O context 4.5 MiB; latest analyzed row `2.40.0 (749)`.
- Shopify: RN-associated payload up to 47.8 MiB (JS/Hermes up to 42.0 MiB, named native runtime up to 5.8 MiB); largest RN carrier Mach-O context 39.0 MiB; latest analyzed row `10.2621.0 (282789)`; sampled direct delta 5.1 MiB.
- Skype: RN-associated payload up to 34.5 MiB (JS/Hermes up to 30.1 MiB, named native runtime up to 4.3 MiB); largest RN carrier Mach-O context 66.1 MiB; latest analyzed row `8.150.3125 (8.150.0.125)`; sampled direct delta 16.2 MiB.
- Threads: RN-associated payload up to 0.0 MiB (JS/Hermes up to 0.0 MiB, named native runtime up to 0.0 MiB); largest RN carrier Mach-O context 123.3 MiB; latest analyzed row `431.0.0 (979167741)`; sampled direct delta 0.0 MiB.

## Interpretation Limits

- Treat `direct_rn_payload_bytes` as an RN-associated packaging floor, not a pure framework tax. It includes the app's JavaScript bundle because that bundle is required by the RN architecture, but app logic would exist in some form in a native implementation too.
- Treat `rn_carrier_macho_bytes` as context. When RN is statically linked into a large main executable, this field can be much larger than the actual RN symbols inside it.
- Rows with `remaining_encrypted_non_extension_count > 0` may hide additional native bytes outside the main app process that the current dump did not decrypt.
- Negative/control rows are important: they keep native or web-hybrid apps from being charged RN overhead just because generic React, JSI, or Yoga-like strings appear elsewhere.
