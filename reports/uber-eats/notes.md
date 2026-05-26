# Uber Eats React Native Timeline

## Registration

- App name: Uber Eats: Food & Groceries
- App Store ID: 1058959277
- iOS bundle ID: com.ubercab.UberEats
- Android package: com.ubercab.eats
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search "Uber Eats" --format json` returned App Store ID `1058959277`, bundle ID `com.ubercab.UberEats`, localized app name `Uber Eats: Доставка еды`, and current listed version `6.323.10001`.
- Apple iTunes lookup for App Store ID `1058959277` returned app name `Uber Eats: Food & Groceries`, seller `Uber Technologies, Inc.`, bundle ID `com.ubercab.UberEats`, current US listed version `6.323.10001`, and release date `2026-05-18T15:48:53Z`.
- App Store URL: `https://apps.apple.com/us/app/uber-eats-food-groceries/id1058959277`.
- Android package sources identify package `com.ubercab.eats`.
- APKPure current page: `https://apkpure.net/uber-eats-food-and-grocery/com.ubercab.eats`.
- APKPure versions URL `https://apkpure.net/uber-eats-food-and-grocery/com.ubercab.eats/versions` returned HTTP `410 Gone`.
- AndroidAPKsFree guessed old versions URL for package `com.ubercab.eats` returned HTTP `404`.
- APKMirror history URL `https://www.apkmirror.com/apk/uber-technologies-inc/uber-eats-food-delivery/` returned HTTP `403` for automated fetches.

## Next Step

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 1058959277`.
- iOS external version IDs available: 624
- Oldest iOS external version ID: `814482031`
- Newest iOS external version ID: `885646390`
- Raw iOS version list: `reports/uber-eats/version-list.json`
- Android APKPure version-list fetch attempted on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android APKPure version-list result: failed with HTTP `410 Gone`, matching the registration-time URL check.
- Raw Android version-list error: `reports/uber-eats/android-version-list-error.json`

## Next Step

Sample the iOS App Store version list first. Revisit Android sources only if iOS sampling is blocked or fails to expose useful RN markers.
