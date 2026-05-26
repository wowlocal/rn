# Pinterest React Native Timeline

## Registration

- App name: Pinterest
- App Store ID: 429047995
- iOS bundle ID: pinterest
- Android package: com.pinterest
- Status: version_list_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Pinterest --format json` returned App Store ID `429047995`, bundle ID `pinterest`, and current listed version `14.19`.
- Apple iTunes lookup for App Store ID `429047995` returned app name `Pinterest`, seller `Pinterest, Inc.`, bundle ID `pinterest`, and current US listed version `14.19`.
- App Store URL: `https://apps.apple.com/us/app/pinterest/id429047995`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.pinterest`.
- Android package sources identify package `com.pinterest`.
- APKPure current app page identified: `https://apkpure.net/pinterest/com.pinterest`; its `/versions` route currently returns HTTP 410.
- APKMirror history page identified: `https://www.apkmirror.com/apk/pinterest/pinterest/`; automated fetches currently return a Cloudflare challenge.
- AndroidAPKsFree old versions page identified: `https://androidapks.com/pinterest/com-pinterest/old/` and exposes direct historical APK download rows.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 429047995`.
- iOS external version IDs available: 645
- Oldest iOS external version ID: `3572654`
- Newest iOS external version ID: `885829462`
- Raw iOS version list: `reports/pinterest/version-list.json`
- Android catalog fetched on 2026-05-26 with `fetch_androidapksfree_versions.py`.
- Android entries available from AndroidAPKsFree sources: 50
- Oldest Android versionCode in the catalog: `12188010` (`12.18.0`)
- Newest Android versionCode in the catalog: `14088010` (`14.8.0`)
- Raw Android version catalog: `reports/pinterest/android-version-list.json`
- AndroidAPKsFree `Updated` dates are preserved as source context but not treated as release dates for ordering.
- APKPure and APKMirror did not provide an automated parseable history at this step.

## Next Step

Sample the Android APK catalog first because packages are directly inspectable and the Android source has a useful mid-2024 through 2026 window.
