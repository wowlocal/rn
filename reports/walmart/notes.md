# Walmart React Native Timeline

## Registration

- App name: Walmart: Shopping & Savings
- App Store ID: 338137227
- iOS bundle ID: com.walmart.electronics
- Android package: com.walmart.android
- Status: version_list_fetched
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

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 338137227`.
- iOS version list result: failed because App Store license is required.
- iOS bundle-ID retry and license attempt for `com.walmart.electronics` returned app not found.
- Raw iOS version-list error: `reports/walmart/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `26120216` (`26.12.2`)
- Newest Android versionCode in the APKPure catalog: `26180118` (`26.18.1`)
- Raw Android version catalog: `reports/walmart/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Next Step

Sample the visible Android APKPure catalog first because iOS version-list access is blocked.
