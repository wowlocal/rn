# Bluesky React Native Timeline

## Registration

- App name: Bluesky Social
- App Store ID: 6444370199
- iOS bundle ID: xyz.blueskyweb.app
- Android package: xyz.blueskyweb.app
- Status: version_lists_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Bluesky --format json` returned App Store ID `6444370199`, bundle ID `xyz.blueskyweb.app`, app name `Bluesky Social`, and current listed version `1.121.0`.
- Apple iTunes lookup for App Store ID `6444370199` returned app name `Bluesky Social`, seller `Bluesky PBLLC`, bundle ID `xyz.blueskyweb.app`, current US listed version `1.121.0`, and release date `2026-04-22T22:32:35Z`.
- App Store URL: `https://apps.apple.com/us/app/bluesky-social/id6444370199`.
- Google Play identifies Android package `xyz.blueskyweb.app` and returned HTTP `200`.
- APKPure Android history URL identified: `https://apkpure.net/bluesky/xyz.blueskyweb.app/versions` returned HTTP `200`.

## Next Step

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions --app-id 6444370199 --format json`.
- iOS app-ID version list result: failed because App Store license is required.
- Bundle-ID iOS version list fetch for `xyz.blueskyweb.app` also failed because App Store license is required.
- `ipatool purchase --bundle-identifier xyz.blueskyweb.app --format json` failed with `unsupported protocol scheme`.
- Raw iOS version-list errors: `reports/bluesky/version-list-error.json`, `reports/bluesky/version-list-bundle-error.json`, and `reports/bluesky/purchase-error.json`.
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the catalog: `795` (`1.114.0`)
- Newest Android versionCode in the catalog: `980` (`1.121.0`)
- Raw Android version catalog: `reports/bluesky/android-version-list.json`
- Source-specific APKPure catalog: `reports/bluesky/android-version-list-apkpure.json`
- APKPure exposes a source-limited visible version catalog; missing Android versions should be treated as source limitations, not absence of releases.

## Next Step

Sample Android packages first because iOS version history is license-blocked.
