# Shop React Native Timeline

## Registration

- App name: Shop
- App Store ID: 1223471316
- iOS bundle ID: com.jadedlabs.arrive
- Android package: com.shopify.arrive
- Status: version_lists_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- Apple iTunes lookup for App Store ID `1223471316` resolved bundle ID `com.jadedlabs.arrive`, app name `Shop: All your favorite brands`, and current listed iOS version `2.253.0`.
- App Store URL: `https://apps.apple.com/us/app/shop-all-your-favorite-brands/id1223471316`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.shopify.arrive`.
- Android package history source identified: APKPure page for package `com.shopify.arrive`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `1223471316` and bundle ID `com.jadedlabs.arrive`.
- iOS version list result: failed because app ID lookup reports `license is required`, while bundle-ID lookup reports `app not found`.
- iOS license attempt: `ipatool purchase --bundle-identifier com.jadedlabs.arrive --format json` failed with `app not found`.
- Raw iOS version-list error: `reports/shop/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `3409799` (`2.246.0`)
- Newest Android versionCode in the APKPure catalog: `3451748` (`2.253.0`)
- Raw Android version catalog: `reports/shop/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Next Step

Run initial Android sampling because APKs may expose clearer React Native evidence and iOS version-list access is currently blocked.
