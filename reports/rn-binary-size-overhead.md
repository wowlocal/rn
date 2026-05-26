# React Native Binary Size Overhead From Decrypted iOS Dumps

## Scope

- Accepted decrypted dump rows analyzed: 26
- Apps represented: 11
- Dump IPAs are local evidence under `tmp/ios-dumps`; they are not committed.
- `direct_rn_payload_bytes` is a conservative floor: JS/Hermes bundle files plus separately named React Native/Hermes/JSI/Yoga native artifacts in the primary app bundle.
- Many iOS apps statically link React Native into the main executable. For those, exact RN-only native bytes cannot be separated from app code without link maps or symbol-level attribution, so `rn_carrier_macho_bytes` reports the containing Mach-O size as context, not as direct overhead.
- Rows with no current RN evidence are retained as controls and should not be interpreted as RN overhead.

## Observations

- Largest direct RN payload floors:
  - Coinbase `14.19.22 (14190022)`: 104.7 MiB (41.25% of primary app uncompressed bytes).
  - Coinbase `13.45.27 (13450027)`: 93.7 MiB (35.76% of primary app uncompressed bytes).
  - Shopify `10.2621.0 (282789)`: 47.8 MiB (26.74% of primary app uncompressed bytes).
  - Skype `8.150.3125 (8.150.0.125)`: 34.5 MiB (20.61% of primary app uncompressed bytes).
  - Mattermost `2.40.0 (749)`: 32.9 MiB (42.71% of primary app uncompressed bytes).
- Static-linked RN rows can have a zero direct-artifact floor; the largest carrier context is 123.3 MiB in Threads `431.0.0 (979167741)`.
- No RN overhead is attributed to current negative/control rows: Agoda: Cheap Flights & Hotels, SoundCloud: The Music You Love, Uber Eats: Food & Groceries.

## Per-Dump Results

| App | Version | RN evidence | Direct RN payload | Direct % of app | RN carrier Mach-O | Coverage | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| Agoda: Cheap Flights & Hotels | `13.40.0 (310516.2)` | no_rn_detected | 0.0 MiB | 0.00% | 0.0 MiB | loaded_app_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers |
| Threads | `373.0.0 (711845629)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 61.0 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Threads | `387.0.0 (755202338)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 74.7 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Threads | `400.0.0 (797742903)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 83.5 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Threads | `431.0.0 (979167741)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 123.3 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Instagram | `114.0 (176133011)` | 0.61.x | 0.9 MiB | 0.86% | 19.1 MiB | main_only_decrypted | remaining encrypted non-extension Mach-O may hide additional bytes |
| Instagram | `430.0.0 (972915403)` | native_rn_marker_without_version | 2.2 MiB | 0.52% | 329.8 MiB | loaded_app_decrypted | native_rn_marker_without_version |
| Facebook Messenger | `562.0.0 (975021560)` | native_rn_marker_without_version | 1.6 MiB | 0.88% | 96.6 MiB | main_only_decrypted | native_rn_marker_without_version remaining encrypted non-extension Mach-O may hide additional bytes |
| Shopify | `10.2621.0 (282789)` | 0.82.x or newer | 47.8 MiB | 26.74% | 39.0 MiB | main_only_decrypted | remaining encrypted non-extension Mach-O may hide additional bytes |
| Mattermost | `2.40.0 (749)` | 0.77.x | 32.9 MiB | 42.71% | 4.5 MiB |  | accepted dump predates decrypted coverage classification |
| Skype | `8.150.3125 (8.150.0.125)` | 0.71.x | 34.5 MiB | 20.61% | 64.9 MiB | loaded_app_decrypted |  |
| Skype | `8.97.3203 (8.97.0.203)` | 0.71.x | 20.5 MiB | 21.32% | 45.5 MiB | loaded_app_decrypted |  |
| SoundCloud: The Music You Love | `7.16.0 (1243764)` | no_rn_detected | 0.0 MiB | 0.00% | 0.0 MiB | loaded_app_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers |
| SoundCloud: The Music You Love | `7.44.0 (1248257)` | no_rn_detected | 0.0 MiB | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| SoundCloud: The Music You Love | `8.32.0 (1254310)` | no_rn_detected | 0.0 MiB | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| SoundCloud: The Music You Love | `8.5.0 (1251600)` | no_rn_detected | 0.0 MiB | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| SoundCloud: The Music You Love | `8.62.0 (1259079)` | no_rn_detected | 0.0 MiB | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| Uber Eats: Food & Groceries | `6.281.10000 (6.281.10000)` | no_rn_detected | 0.0 MiB | 0.00% | 0.0 MiB | main_only_decrypted | negative/control row: no React Native evidence in current analyzer output no_js_or_native_rn_markers remaining encrypted non-exten |
| Coinbase | `13.45.27 (13450027)` | 0.60.x | 93.7 MiB | 35.76% | 75.1 MiB | loaded_app_decrypted |  |
| Coinbase | `14.19.22 (14190022)` | 0.60.x | 104.7 MiB | 41.25% | 56.4 MiB | loaded_app_decrypted |  |
| Artsy: Buy & Sell Fine Art | `7.3.5 (2022.04.22.16)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 12.7 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.6 (2022.05.11.16)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 12.8 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.7 (2022.05.25.17)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 12.8 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.8 (2022.05.29.23)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 12.8 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `7.3.9 (2022.06.03.16)` | native_rn_marker_without_version | 0.0 MiB | 0.00% | 12.6 MiB | loaded_app_decrypted | direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O native_rn_marker_without_version |
| Artsy: Buy & Sell Fine Art | `9.9.0 (2026.05.20.12.45)` | 0.81.x | 16.5 MiB | 16.47% | 44.1 MiB | loaded_app_decrypted |  |

## App-Level Takeaways

- Artsy: Buy & Sell Fine Art: direct RN payload floor up to 16.5 MiB; largest RN carrier Mach-O context 44.1 MiB; latest analyzed row `9.9.0 (2026.05.20.12.45)`.
- Coinbase: direct RN payload floor up to 104.7 MiB; largest RN carrier Mach-O context 75.1 MiB; latest analyzed row `14.19.22 (14190022)`.
- Facebook Messenger: direct RN payload floor up to 1.6 MiB; largest RN carrier Mach-O context 96.6 MiB; latest analyzed row `562.0.0 (975021560)`.
- Instagram: direct RN payload floor up to 2.2 MiB; largest RN carrier Mach-O context 329.8 MiB; latest analyzed row `430.0.0 (972915403)`.
- Mattermost: direct RN payload floor up to 32.9 MiB; largest RN carrier Mach-O context 4.5 MiB; latest analyzed row `2.40.0 (749)`.
- Shopify: direct RN payload floor up to 47.8 MiB; largest RN carrier Mach-O context 39.0 MiB; latest analyzed row `10.2621.0 (282789)`.
- Skype: direct RN payload floor up to 34.5 MiB; largest RN carrier Mach-O context 64.9 MiB; latest analyzed row `8.150.3125 (8.150.0.125)`.
- Threads: direct RN payload floor up to 0.0 MiB; largest RN carrier Mach-O context 123.3 MiB; latest analyzed row `431.0.0 (979167741)`.
