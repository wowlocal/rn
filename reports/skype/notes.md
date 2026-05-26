# Skype React Native Timeline

## Registration
- App name: Skype
- App Store ID: 304878510
- iOS bundle ID: com.skype.skype
- Android package: com.skype.raider
- Status: queued
- Registration date: 2026-05-26

## Evidence
- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- Skype consumer service and apps are retired as of 2025-05-05.
- Current Apple iTunes lookup for App Store ID 304878510 returns no result.
- Current Google Play URL for package com.skype.raider returns 404.
- Historical iOS identifier sources identify App Store ID 304878510 and bundle ID com.skype.skype for Skype for iPhone.
- APKPure identifies Android package com.skype.raider and exposes package history URL https://apkpure.net/skype/com.skype.raider/versions.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions --app-id 304878510`.
- iOS external version IDs available: 185
- Oldest iOS external version ID: `822306851`
- Newest iOS external version ID: `874426597`
- Raw iOS version list: `reports/skype/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `1250181076` (`8.132.0.201`)
- Newest Android versionCode in the APKPure catalog: `1250186747` (`8.150.0.125`)
- Raw Android version catalog: `reports/skype/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Next Step
Sample the visible Android APKPure catalog first because APKs are directly inspectable and the app is retired from current public store lookups.
