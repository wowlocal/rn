# Walmart React Native Timeline

## Registration

- App name: Walmart: Shopping & Savings
- App Store ID: 338137227
- iOS bundle ID: com.walmart.electronics
- Android package: com.walmart.android
- Status: queued
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Walmart --format json` did not return the consumer Walmart shopping app in the current localized results.
- Public App Store URL and Apple iTunes lookup for App Store ID `338137227` returned app name `Walmart: Shopping & Savings`, seller `Walmart`, bundle ID `com.walmart.electronics`, and current US listed version `26.19.2`.
- App Store URL: `https://apps.apple.com/us/app/walmart-shopping-savings/id338137227`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.walmart.android`.
- Android package sources identify package `com.walmart.android`.
- APKPure history page identified: `https://apkpure.net/walmart-shopping-savings/com.walmart.android/versions`.
- AndroidAPKsFree old versions page identified: `https://androidapks.com/walmart/com-walmart-android/old/`.

## Next Step

Fetch iOS and Android version catalogs, preferring APKPure for the first Android sampling pass if it exposes direct version rows.
