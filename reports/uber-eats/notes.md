# Uber Eats React Native Timeline

## Registration

- App name: Uber Eats: Food & Groceries
- App Store ID: 1058959277
- iOS bundle ID: com.ubercab.UberEats
- Android package: com.ubercab.eats
- Status: not_react_native_detected
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

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 1058959277`.
- iOS external version IDs available: 624
- Oldest iOS external version ID: `814482031`
- Newest iOS external version ID: `885646390`
- Raw iOS version list: `reports/uber-eats/version-list.json`
- Android APKPure version-list fetch attempted on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android APKPure version-list result: failed with HTTP `410 Gone`, matching the registration-time URL check.
- Raw Android version-list error: `reports/uber-eats/android-version-list-error.json`

## Initial iOS Sampling

- iOS sampling date: 2026-05-26
- iOS IPAs downloaded and analyzed: 12
- Unique app builds analyzed: 12
- Sample strategy: 12 evenly spaced external version IDs from the 624-entry App Store version list, including oldest and newest available IDs.
- Sampled external version IDs: `814482031`, `819763331`, `825734304`, `830475334`, `834678875`, `839453042`, `844340326`, `851791131`, `859897772`, `869096326`, `876620596`, `885646390`.
- Sampled app versions: `1.9.2`, `1.61.1`, `1.121.10002`, `1.178.10002`, `1.228.10001`, `1.270.10007`, `6.79.10004`, `6.127.10003`, `6.182.10003`, `6.235.10002`, `6.281.10000`, `6.323.10001`.
- No sampled IPA contained a JS bundle, Hermes bytecode, or React Native-related filenames such as `ReactNative`, `react-native`, `Hermes`, `JSI`, `Yoga`, `.jsbundle`, or `.hbc`.
- All sampled IPA main executables are FairPlay encrypted, so native constants are not inspectable.
- iOS reports: `reports/uber-eats/versions.csv`, `reports/uber-eats/versions.json`, `reports/uber-eats/ranges.csv`, and `reports/uber-eats/timeline.json`.

## Result

Marked `not_react_native_detected` because no React Native markers were found in the 12-point iOS sample and no automated Android package history is available.
