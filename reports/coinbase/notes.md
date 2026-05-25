# Coinbase React Native Timeline

## Registration

- App name: Coinbase
- App Store ID: 886427730
- iOS bundle ID: com.vilcsak.bitcoin2
- Android package: com.coinbase.android
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Coinbase --format json` returned App Store ID `886427730`, bundle ID `com.vilcsak.bitcoin2`, and current listed version `14.19.22`.
- Apple iTunes lookup for App Store ID `886427730` returned app name `Coinbase: Buy Crypto & Stocks`, seller `Coinbase, Inc.`, bundle ID `com.vilcsak.bitcoin2`, and current listed version `14.19.22`.
- App Store URL: `https://apps.apple.com/us/app/coinbase-buy-crypto-stocks/id886427730`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.coinbase.android`.
- Android package history source identified: APKPure page for package `com.coinbase.android`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 886427730 --format json`.
- iOS external version IDs available: 555
- Oldest iOS external version ID: `596373720`
- Newest iOS external version ID: `885921388`
- Raw iOS version catalog: `reports/coinbase/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `141000440` (`14.10.44`)
- Newest Android versionCode in the APKPure catalog: `141900220` (`14.19.22`)
- Raw Android version catalog: `reports/coinbase/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Next Step

Download and analyze the visible Android XAPKs first; use iOS IPAs only if Android does not expose usable RN markers or if platform comparison is needed.
