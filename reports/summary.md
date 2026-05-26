# Popular React Native Mobile Apps Timeline Summary

## Methodology

Reports keep platform-specific package timelines separate, then merge them here with platform labels. iOS reports use IPA internal zip timestamps from app bundle `Info.plist` members unless an App Store date is independently verified. Android APK/APKS/XAPK/APKM analysis is first-class evidence when packages are available because Android packages are usually not FairPlay-encrypted like App Store IPAs and often expose JS bundles, Hermes bytecode, RN native libraries, symbols, and resources directly. Android ordering is based on manifest versionCode first, with source order or source publish dates as secondary context when manifest versionCode is unavailable. Android reports record package hashes, embedded manifest metadata, and package identity when available; duplicated, installer/wrapper, or catalog-mismatched payloads are treated as source-quality findings rather than exact historical builds. Source-limited Android catalogs can guide ranges but do not make transition boundaries exact merely because adjacent fetched rows have no known row between them. Exact RN patch versions are reported only when strong markers are exposed; encrypted native binaries generally limit results to RN version bands inferred from JS bundle markers.

## App Status

- Analyzed successfully: 6
- Queued: 0
- In progress: 1
- Needs manual review: 14
- No RN detected: 2
- Skipped: 3

## Analyzed Apps

- Discord: 475 iOS external versions; reports in `reports/discord`
- Facebook Messenger: 735 iOS external versions; reports in `reports/facebook-messenger`
- Instagram: 795 iOS external versions; reports in `reports/instagram`
- Pinterest: 645 iOS external versions; reports in `reports/pinterest`
- Artsy: Buy & Sell Fine Art: 292 iOS external versions; reports in `reports/artsy`
- Mattermost: 175 iOS external versions; reports in `reports/mattermost`

## In Progress Apps

- Bluesky Social: status `version_lists_fetched`; last completed `version_list_fetch`; reports in `reports/bluesky`

## Manual Review Apps

- Threads: last completed `source_limited_boundary_refinement`; reports in `reports/threads`
- Meta Horizon: last completed `source_limited_boundary_refinement`; reports in `reports/meta-horizon`
- Shopify: last completed `source_limited_boundary_refinement`; reports in `reports/shopify`
- Shop: last completed `source_limited_boundary_refinement`; reports in `reports/shop`
- Coinbase: last completed `source_limited_android_sampling`; reports in `reports/coinbase`
- Microsoft Outlook: last completed `source_limited_android_sampling`; reports in `reports/microsoft-outlook`
- Microsoft Teams: last completed `source_limited_android_sampling`; reports in `reports/microsoft-teams`
- Skype: last completed `source_limited_android_sampling`; reports in `reports/skype`
- Walmart: Shopping & Savings: last completed `source_limited_android_sampling`; reports in `reports/walmart`
- Tesla: last completed `source_limited_android_sampling`; reports in `reports/tesla`
- Bloomberg: Business News Daily: last completed `source_limited_android_sampling`; reports in `reports/bloomberg`
- Salesforce: last completed `source_limited_android_sampling`; reports in `reports/salesforce`
- Wix - Website Builder: last completed `source_limited_android_sampling`; reports in `reports/wix`
- NerdWallet: Smart Money App: last completed `source_limited_android_sampling`; reports in `reports/nerdwallet`

## No RN Detected Apps

- Uber Eats: Food & Groceries: sampled 12 iOS IPAs; reports in `reports/uber-eats`
- SoundCloud: The Music You Love: sampled 12 iOS IPAs; reports in `reports/soundcloud`

## Skipped Apps

- Facebook: Registered for analysis on 2026-05-25.; RN usage was not verified because ipatool list-versions failed before sampling.; ipatool list-versions failed for both app ID 284882215 and bundle ID com.facebook.Facebook with Apple's generic unknown error.; ipatool purchase also failed with unsupported protocol scheme before a license could be obtained.
- Base: Formerly Coinbase Wallet: Registered for analysis on 2026-05-26.; Current iOS/App Store branding source: Apple iTunes lookup for App Store ID 1278383455 returned app name Base: Built to Trade & Earn, seller Coinbase Wallet, bundle ID org.toshi.distribution, and current listed version 29.96.; ipatool search Coinbase Wallet --format json returned App Store ID 1278383455, bundle ID org.toshi.distribution, and localized app name Base: Formerly Coinbase Wallet.; Android package source: Google Play, AppBrain, and WalletScrutiny identify package org.toshi for Base/formerly Coinbase Wallet.; APKPure history URLs for org.toshi returned HTTP 410 Gone, so no APKPure version catalog is available at registration time.; iOS version list fetch failed on 2026-05-26: ipatool list-versions by app ID and bundle ID requires an App Store license; ipatool purchase failed with unsupported protocol scheme.; Skipped because neither iOS version history nor a usable Android package-history source is available through the current automated tools.
- Kraken: Registered for analysis on 2026-05-26.; iOS identifier source: Apple iTunes lookup for App Store ID 1481947260 returned bundle ID com.kraken.invest.app, app name Kraken: Buy Crypto & Stocks, seller Payward, Inc., and current listed version 3.65.0.; Android package source: Google Play, AppBrain, and AppRecs identify package com.kraken.invest.app.; APKPure history URLs for com.kraken.invest.app returned HTTP 410 Gone, so no APKPure Android version catalog is available at registration time.; ipatool search Kraken did not surface the finance app in the current localized search results; App Store ID was resolved from the public App Store URL and Apple iTunes lookup.; iOS version list fetch failed on 2026-05-26: ipatool list-versions by app ID requires an App Store license; bundle-ID purchase and list attempts for com.kraken.invest.app returned app not found.; Skipped because neither iOS version history nor a usable Android package-history source is available through the current automated tools.

## RN Ranges

| App | Platform | RN guess | Renderer | Confidence | Source quality | Start | End | Builds |
|---|---|---|---:|---|---|---|---|---:|
| Discord | ios | <=0.59.x |  | medium |  | 1.0 (4) | 3.1.10 (18953) | 8 |
| Discord | ios | 0.61.x |  | medium |  | 3.2.0 (19099) | 20.0 (19811) | 8 |
| Discord | ios | 0.62.x |  | medium |  | 21.0 (19965) | 87.0 (27320) | 8 |
| Discord | ios | 0.64.x |  | medium |  | 88.2 (27527) | 106.0 (29538) | 16 |
| Discord | ios | 0.66.x |  | medium |  | 109.0 (29659) | 132.0 (33253) | 4 |
| Discord | ios | 0.67.x-0.68.x |  | medium |  | 133.0 (33358) | 162.0 (39121) | 7 |
| Discord | ios | 0.69.x-0.70.x |  | medium |  | 163.0 (39243) | 190.0 (47418) | 7 |
| Discord | ios | 0.71.x |  | medium |  | 191.0 (47806) | 245.0 (63641) | 9 |
| Discord | ios | 0.74.x-0.76.x |  | medium |  | 246.0 (63933) | 279.0 (77189) | 42 |
| Discord | ios | 0.78.x | 19.0.0 | high |  | 280.0 (77565) | 306.1 (89123) | 31 |
| Discord | ios | 0.81.x | 19.1.0 | high |  | 307.0 (89215) | 329.0 (100971) | 33 |
| Facebook Messenger | ios | unknown |  | low |  |  (1000) | 91.0 (40546824) | 7 |
| Facebook Messenger | ios | <=0.59.x |  | medium |  | 92.0 (41023043) | 147.0 (84235609) | 7 |
| Facebook Messenger | ios | unknown |  | low |  | 148.0 (86952252) | 562.0.0 (975021560) | 12 |
| Instagram | ios | unknown |  | low |  |  (1.8.7) | 9.7.0 (43028597) | 9 |
| Instagram | ios | <=0.59.x |  | medium |  | 10.0.0 (44114773) | 90.0 (150975176) | 6 |
| Instagram | ios | 0.60.x |  | medium |  | 91.0 (151989260) | 105.0 (165586599) | 5 |
| Instagram | ios | 0.61.x |  | medium |  | 106.0 (166752244) | 113.0 (174653610) | 5 |
| Instagram | ios | unknown |  | low |  | 114.0 (176133011) | 430.0.0 (972915403) | 9 |
| Threads | ios | unknown |  | low |  | 289.0 (489338310) | 431.0.0 (979167741) | 12 |
| Threads | android | unknown |  | low |  | 374.0.0.43.110 (504412928) | 382.0.0.51.85 (505205644) | 2 |
| Threads | android | unknown |  | unknown |  | 400.0.0.38.68 (507007017) | 430.0.0.46.79 (510007506) | 10 |
| Meta Horizon | android | 0.78.x | 19.0.0 | high |  | 287.3.0.33.109 (651148422) | 287.3.0.33.109 (651148422) | 1 |
| Meta Horizon | android | 0.60.x |  | medium |  | 341.0.0.17.107 (806319963) | 349.2.0.46.104 (844730700) | 11 |
| Meta Horizon | android | <=0.59.x |  | medium |  | 360.0.0.23.322 (892081967) | 372.0.1.34.252 (975394013) | 18 |
| Shopify | android | 0.79.x | 19.0.0 | medium |  | 10.2543.0 (193814) | 10.2605.0 (220449) | 8 |
| Shopify | android | 0.60.x |  | medium |  | 10.2606.1 (223088) | 10.2620.0 (281050) | 16 |
| Shop | android | 0.79.x | 19.0.0 | medium |  | 2.231.0 (3319531) | 2.239.0 (3372633) | 11 |
| Shop | android | 0.81.x | 19.1.0 | high |  | 2.240.0 (3376891) | 2.253.0 (3451748) | 16 |
| Coinbase | android | 0.82.x or newer |  | low |  | 14.1.27 (140100270) | 14.19.22 (141900220) | 19 |
| Microsoft Outlook | android | unknown |  | low |  | 4.2504.2 (82504829) | 5.2619.0 (72619117) | 10 |
| Microsoft Teams | android | 0.60.x |  | medium |  | 1416/1.0.0.2026015002 (2026015023) | 1416/1.0.0.2026082702 (2026082725) | 10 |
| Skype | android | 0.74.x-0.76.x |  | medium |  | 8.132.0.201 (1250181076) | 8.150.0.125 (1250186747) | 10 |
| Pinterest | ios | unknown |  | low |  |  (1) | 6.36.1 (1) | 10 |
| Pinterest | ios | <=0.59.x |  | medium |  | 6.37 (4) | 8.12.1 (4) | 10 |
| Pinterest | ios | 0.60.x |  | medium |  | 8.13 (4) | 8.17 (3) | 5 |
| Pinterest | ios | 0.61.x |  | medium |  | 8.18 (3) | 8.26 (4) | 5 |
| Pinterest | ios | 0.63.x |  | medium |  | 8.27 (4) | 10.40 (2) | 16 |
| Pinterest | ios | unknown |  | low |  | 10.41 (2) | 14.19 (2) | 4 |
| Pinterest | android | unknown |  | unknown |  | 12.18.0 (12188010) | 14.8.0 (14088010) | 12 |
| Walmart: Shopping & Savings | android | 0.74.x-0.76.x |  | medium |  | 21.5.5 (21055104) | 21.5.5 (21055104) | 1 |
| Walmart: Shopping & Savings | android | unknown |  | unknown |  | 21.22 (21220106) | 26.18.1 (26180118) | 24 |
| Tesla | android | 0.79.x | 19.0.0 | medium |  | 4.54.0-4094 (4094) | 4.54.0-4094 (4094) | 1 |
| Tesla | android | 0.82.x or newer |  | low |  | 4.54.3-4107 (4107) | 4.54.3-4107 (4107) | 1 |
| Tesla | android | 0.79.x | 19.0.0 | medium |  | 4.54.5-4133 (4133) | 4.57.0-4306 (4306) | 8 |
| Uber Eats: Food & Groceries | ios | unknown |  | low |  | 1.9.2 (1.9.2) | 6.323.10001 (6.323.10001) | 12 |
| SoundCloud: The Music You Love | ios | unknown |  | low |  |  (1.0) | 8.62.0 (1259079) | 12 |
| SoundCloud: The Music You Love | android | unknown |  | unknown |  | 2026.03.27-release (348060) | 2026.05.15-release (355060) | 10 |
| Bloomberg: Business News Daily | android | 0.61.x |  | medium |  | 5.58.0.3042781.7b196c06c (3042781) | 5.58.0.3042781.7b196c06c (3042781) | 1 |
| Bloomberg: Business News Daily | android | 0.74.x-0.76.x |  | medium |  | 5.98.0.3930355.fd19b588e (3930355) | 6.19.0.4315110.19bd92161 (4315110) | 4 |
| Salesforce | android | unknown |  | low |  | 250.030.0 (250030032) | 260.050.0 (260050025) | 10 |
| Wix - Website Builder | android | unknown |  | low | duplicate package hashes (1/10) | 2.115937.0 (130467) | 2.122966.0 (137496) | 10 |
| Artsy: Buy & Sell Fine Art | ios | unknown |  | low |  | 1.0 (140) | 7.3.9 (2022.06.03.16) | 12 |
| Artsy: Buy & Sell Fine Art | ios | 0.66.x |  | medium |  | 8.0.0 (2022.06.24.16) | 8.9.0 (2023.03.09.08) | 9 |
| Artsy: Buy & Sell Fine Art | ios | 0.67.x-0.68.x |  | medium |  | 8.10.0 (2023.03.23.14) | 8.12.4 (2023.05.11.19) | 6 |
| Artsy: Buy & Sell Fine Art | ios | 0.69.x-0.70.x |  | medium |  | 8.12.5 (2023.05.17.13) | 8.27.0 (2023.11.30.23) | 7 |
| Artsy: Buy & Sell Fine Art | ios | 0.71.x |  | medium |  | 8.28.0 (2023.12.13.10) | 8.56.0 (2024.11.14.13) | 11 |
| Artsy: Buy & Sell Fine Art | ios | 0.74.x-0.76.x |  | medium |  | 8.57.0 (2024.11.29.16) | 8.79.0 (2025.07.24.14) | 6 |
| Artsy: Buy & Sell Fine Art | ios | 0.77.x |  | medium |  | 8.80.0 (2025.08.07.10) | 8.83.0 (2025.09.17.12) | 4 |
| Artsy: Buy & Sell Fine Art | ios | 0.79.x | 19.0.0 | medium |  | 8.84.0 (2025.09.30.18) | 8.88.0 (2025.11.12.13) | 5 |
| Artsy: Buy & Sell Fine Art | ios | 0.81.x | 19.1.0 | high |  | 8.89.0 (2025.11.26.02) | 9.9.0 (2026.05.20.12.45) | 5 |
| Artsy: Buy & Sell Fine Art | android | 0.82.x or newer | 19.1.0 | low | duplicate package hashes (1/10) | 9.0.1 (2026022618) | 9.9.0 (2026052012) | 10 |
| NerdWallet: Smart Money App | android | unknown |  | low | source-limited Uptodown catalog; source IDs are not manifest versionCodes; source dates are non-monotonic versus manifest versionCode | 11.29.0 (123845) | 12.6.0 (131162) | 4 |
| NerdWallet: Smart Money App | android | 0.77.x |  | medium | source-limited Uptodown catalog; source IDs are not manifest versionCodes; source dates are non-monotonic versus manifest versionCode | 12.10.1 (140458) | 14.3.0 (162034) | 6 |
| Mattermost | ios | <=0.59.x |  | medium |  | 1.0 (39) | 1.25.1 (247) | 4 |
| Mattermost | ios | 0.61.x |  | medium |  | 1.26.0 (253) | 1.31.2 (296) | 12 |
| Mattermost | ios | 0.62.x |  | medium |  | 1.32.0 (302) | 1.34.1 (320) | 7 |
| Mattermost | ios | 0.63.x |  | medium |  | 1.35.0 (325) | 1.41.1 (349) | 10 |
| Mattermost | ios | 0.64.x |  | medium |  | 1.42.0 (353) | 1.46.0 (368) | 8 |
| Mattermost | ios | 0.65.x |  | medium |  | 1.47.0 (374) | 1.47.2 (377) | 3 |
| Mattermost | ios | 0.66.x |  | medium |  | 1.48.0 (380) | 1.48.2 (382) | 3 |
| Mattermost | ios | 0.67.x-0.68.x |  | medium |  | 1.49.0 (385) | 1.55.1 (423) | 12 |
| Mattermost | ios | 0.69.x-0.70.x |  | medium |  | 2.0.0 (452) | 2.0.0 (452) | 1 |
| Mattermost | ios | 0.71.x |  | medium |  | 2.0.1 (455) | 2.18.1 (536) | 12 |
| Mattermost | ios | 0.74.x-0.76.x |  | medium |  | 2.19.0 (544) | 2.36.4 (712) | 19 |
| Mattermost | ios | 0.77.x |  | medium |  | 2.37.0 (717) | 2.40.0 (749) | 9 |
| Mattermost | android | unknown |  | low | duplicate package hashes (1/10) | 2.39.0 (8000743) | 2.39.0 (8000743) | 10 |

## RN Transitions

| App | Platform | From | To | Last old | First new | Known-list gap | Exact? |
|---|---|---|---|---|---|---:|---|
| Discord | ios | <=0.59.x | 0.61.x | 3.1.10 (18953) | 3.2.0 (19099) | 0 | true |
| Discord | ios | 0.61.x | 0.62.x | 20.0 (19811) | 21.0 (19965) | 0 | true |
| Discord | ios | 0.62.x | 0.64.x | 87.0 (27320) | 88.2 (27527) | 2 | false |
| Discord | ios | 0.64.x | 0.66.x | 106.0 (29538) | 109.0 (29659) | 0 | true |
| Discord | ios | 0.66.x | 0.67.x-0.68.x | 132.0 (33253) | 133.0 (33358) | 0 | true |
| Discord | ios | 0.67.x-0.68.x | 0.69.x-0.70.x | 162.0 (39121) | 163.0 (39243) | 0 | true |
| Discord | ios | 0.69.x-0.70.x | 0.71.x | 190.0 (47418) | 191.0 (47806) | 0 | true |
| Discord | ios | 0.71.x | 0.74.x-0.76.x | 245.0 (63641) | 246.0 (63933) | 0 | true |
| Discord | ios | 0.74.x-0.76.x | 0.78.x | 279.0 (77189) | 280.0 (77565) | 0 | true |
| Discord | ios | 0.78.x | 0.81.x | 306.1 (89123) | 307.0 (89215) | 0 | true |
| Facebook Messenger | ios | unknown | <=0.59.x | 91.0 (40546824) | 92.0 (41023043) | 0 | true |
| Facebook Messenger | ios | <=0.59.x | unknown | 147.0 (84235609) | 148.0 (86952252) | 0 | true |
| Instagram | ios | unknown | <=0.59.x | 9.7.0 (43028597) | 10.0.0 (44114773) | 0 | true |
| Instagram | ios | <=0.59.x | 0.60.x | 90.0 (150975176) | 91.0 (151989260) | 0 | true |
| Instagram | ios | 0.60.x | 0.61.x | 105.0 (165586599) | 106.0 (166752244) | 0 | true |
| Instagram | ios | 0.61.x | unknown | 113.0 (174653610) | 114.0 (176133011) | 0 | true |
| Threads | android | unknown | unknown | 382.0.0.51.85 (505205644) | 400.0.0.38.68 (507007017) | 0 | false |
| Meta Horizon | android | 0.78.x | 0.60.x | 287.3.0.33.109 (651148422) | 341.0.0.17.107 (806319963) | 0 | false |
| Meta Horizon | android | 0.60.x | <=0.59.x | 349.2.0.46.104 (844730700) | 360.0.0.23.322 (892081967) | 0 | false |
| Shopify | android | 0.79.x | 0.60.x | 10.2605.0 (220449) | 10.2606.1 (223088) | 0 | false |
| Shop | android | 0.79.x | 0.81.x | 2.239.0 (3372633) | 2.240.0 (3376891) | 0 | false |
| Pinterest | ios | unknown | <=0.59.x | 6.36.1 (1) | 6.37 (4) | 0 | true |
| Pinterest | ios | <=0.59.x | 0.60.x | 8.12.1 (4) | 8.13 (4) | 0 | true |
| Pinterest | ios | 0.60.x | 0.61.x | 8.17 (3) | 8.18 (3) | 0 | true |
| Pinterest | ios | 0.61.x | 0.63.x | 8.26 (4) | 8.27 (4) | 0 | true |
| Pinterest | ios | 0.63.x | unknown | 10.40 (2) | 10.41 (2) | 0 | true |
| Walmart: Shopping & Savings | android | 0.74.x-0.76.x | unknown | 21.5.5 (21055104) | 21.22 (21220106) | 0 | false |
| Tesla | android | 0.79.x | 0.82.x or newer | 4.54.0-4094 (4094) | 4.54.3-4107 (4107) | 0 | false |
| Tesla | android | 0.82.x or newer | 0.79.x | 4.54.3-4107 (4107) | 4.54.5-4133 (4133) | 1 | false |
| Bloomberg: Business News Daily | android | 0.61.x | 0.74.x-0.76.x | 5.58.0.3042781.7b196c06c (3042781) | 5.98.0.3930355.fd19b588e (3930355) | 0 | false |
| Artsy: Buy & Sell Fine Art | ios | unknown | 0.66.x | 7.3.9 (2022.06.03.16) | 8.0.0 (2022.06.24.16) | 0 | true |
| Artsy: Buy & Sell Fine Art | ios | 0.66.x | 0.67.x-0.68.x | 8.9.0 (2023.03.09.08) | 8.10.0 (2023.03.23.14) | 0 | true |
| Artsy: Buy & Sell Fine Art | ios | 0.67.x-0.68.x | 0.69.x-0.70.x | 8.12.4 (2023.05.11.19) | 8.12.5 (2023.05.17.13) | 0 | true |
| Artsy: Buy & Sell Fine Art | ios | 0.69.x-0.70.x | 0.71.x | 8.27.0 (2023.11.30.23) | 8.28.0 (2023.12.13.10) | 0 | true |
| Artsy: Buy & Sell Fine Art | ios | 0.71.x | 0.74.x-0.76.x | 8.56.0 (2024.11.14.13) | 8.57.0 (2024.11.29.16) | 0 | true |
| Artsy: Buy & Sell Fine Art | ios | 0.74.x-0.76.x | 0.77.x | 8.79.0 (2025.07.24.14) | 8.80.0 (2025.08.07.10) | 0 | true |
| Artsy: Buy & Sell Fine Art | ios | 0.77.x | 0.79.x | 8.83.0 (2025.09.17.12) | 8.84.0 (2025.09.30.18) | 0 | true |
| Artsy: Buy & Sell Fine Art | ios | 0.79.x | 0.81.x | 8.88.0 (2025.11.12.13) | 8.89.0 (2025.11.26.02) | 0 | true |
| NerdWallet: Smart Money App | android | unknown | 0.77.x | 12.6.0 (131162) | 12.10.1 (140458) | 1 | false |
| Mattermost | ios | <=0.59.x | 0.61.x | 1.25.1 (247) | 1.26.0 (253) | 0 | true |
| Mattermost | ios | 0.61.x | 0.62.x | 1.31.2 (296) | 1.32.0 (302) | 0 | true |
| Mattermost | ios | 0.62.x | 0.63.x | 1.34.1 (320) | 1.35.0 (325) | 0 | true |
| Mattermost | ios | 0.63.x | 0.64.x | 1.41.1 (349) | 1.42.0 (353) | 0 | true |
| Mattermost | ios | 0.64.x | 0.65.x | 1.46.0 (368) | 1.47.0 (374) | 0 | true |
| Mattermost | ios | 0.65.x | 0.66.x | 1.47.2 (377) | 1.48.0 (380) | 0 | true |
| Mattermost | ios | 0.66.x | 0.67.x-0.68.x | 1.48.2 (382) | 1.49.0 (385) | 0 | true |
| Mattermost | ios | 0.67.x-0.68.x | 0.69.x-0.70.x | 1.55.1 (423) | 2.0.0 (452) | 0 | true |
| Mattermost | ios | 0.69.x-0.70.x | 0.71.x | 2.0.0 (452) | 2.0.1 (455) | 0 | true |
| Mattermost | ios | 0.71.x | 0.74.x-0.76.x | 2.18.1 (536) | 2.19.0 (544) | 0 | true |
| Mattermost | ios | 0.74.x-0.76.x | 0.77.x | 2.36.4 (712) | 2.37.0 (717) | 0 | true |

## Boundary Confidence

- Exact by transition IDs: 39
- Approximate by transition IDs: 11
- Per-app notes may refine duplicate-build boundary cases where multiple external IDs map to the same app build.
