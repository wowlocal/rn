# Mattermost React Native Timeline

## Registration

- App name: Mattermost
- App Store ID: 1257222717
- iOS bundle ID: com.mattermost.rn
- Android package: com.mattermost.rn
- Status: version_lists_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Mattermost --format json` returned App Store ID `1257222717`, bundle ID `com.mattermost.rn`, app name `Mattermost`, and current listed version `2.40.0`.
- Apple iTunes lookup for App Store ID `1257222717` returned app name `Mattermost`, seller `Mattermost, Inc.`, bundle ID `com.mattermost.rn`, current US listed version `2.40.0`, and release date `2026-05-15T18:24:59Z`.
- App Store URL: `https://apps.apple.com/us/app/mattermost/id1257222717`.
- Google Play identifies Android package `com.mattermost.rn` and returned HTTP `200`.
- APKPure Android history URL identified: `https://apkpure.net/mattermost/com.mattermost.rn/versions` returned HTTP `200`.

## Next Step

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 1257222717 --format json`.
- iOS external version identifiers available: 175
- Oldest iOS external version ID: `822837610`
- Newest iOS external version ID: `885697976`
- Raw iOS version list: `reports/mattermost/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the catalog: `6000627` (`2.27.0`)
- Newest Android versionCode in the catalog: `6000743` (`2.39.0`)
- Raw Android version catalog: `reports/mattermost/android-version-list.json`
- Source-specific APKPure catalog: `reports/mattermost/android-version-list-apkpure.json`
- APKPure exposes a source-limited visible version catalog; missing Android versions should be treated as source limitations, not absence of releases.

## Next Step

Sample Android packages first, then use those markers to guide iOS sampling if needed.
