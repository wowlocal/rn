# Pinterest React Native Timeline

## Registration

- App name: Pinterest
- App Store ID: 429047995
- iOS bundle ID: pinterest
- Android package: com.pinterest
- Status: queued
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

## Next Step

Fetch iOS version IDs and build an Android version catalog from the parseable Android history sources, preferring directly inspectable APKs where available.
