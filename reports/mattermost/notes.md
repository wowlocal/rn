# Mattermost React Native Timeline

## Registration

- App name: Mattermost
- App Store ID: 1257222717
- iOS bundle ID: com.mattermost.rn
- Android package: com.mattermost.rn
- Status: initial_sampling
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

## Initial Sampling

- Android sampling completed on 2026-05-26 from all 10 visible APKPure rows.
- Android result: React Native markers are present through `assets/dist/bundle.js`, `assets/index.android.bundle`, Hermes bytecode, and native libraries including `libreactnative.so`, `libhermes.so`, `libjsi.so`, and `libwatermelondb-jsi.so`.
- Android source-quality finding: every APKPure catalog row resolved to the same embedded manifest versionName `2.39.0`, manifest versionCode `8000743`, and package hash, so the Android catalog is current-payload evidence only.
- iOS sampling completed on 2026-05-26 from 12 evenly spaced IPAs across external version IDs `822837610` through `885697976`.
- Broad iOS sample ranges: `1.0` build `39` through `1.25.1` build `247` as RN `<=0.59.x`; `1.32.2` build `307` as RN `0.62.x`; `1.42.1` build `354` as RN `0.64.x`; `1.50.1` build `388` as RN `0.67.x-0.68.x`; `2.5.1` build `476` through `2.15.0` build `512` as RN `0.71.x`; `2.24.1` build `593` through `2.33.1` build `680` as RN `0.74.x-0.76.x`; `2.40.0` build `749` as RN `0.77.x`.
- Reports: `reports/mattermost/versions.csv`, `reports/mattermost/versions.json`, `reports/mattermost/ranges.csv`, `reports/mattermost/ranges.json`, `reports/mattermost/transitions.csv`, `reports/mattermost/transitions.json`, `reports/mattermost/android-versions.csv`, and `reports/mattermost/android-ranges.json`.

## Next Step

Refine iOS RN transition boundaries using adjacent App Store external version IDs.
