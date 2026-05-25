# Shopify React Native Timeline

## Registration

- App name: Shopify
- App Store ID: 371294472
- iOS bundle ID: com.jadedpixel.shopify
- Android package: com.shopify.mobile
- Status: version_lists_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search "Shopify" --format json` resolved App Store ID `371294472`, bundle ID `com.jadedpixel.shopify`, and current listed iOS version `10.2621.0`.
- App Store URL: `https://apps.apple.com/us/app/shopify-your-ecommerce-store/id371294472`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.shopify.mobile`.
- Android package history source identified: APKPure page for package `com.shopify.mobile`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions` through `check_rn_versions.py --list-versions-only`.
- iOS external version IDs available: 508
- Oldest iOS external version ID: `821337490`
- Newest iOS external version ID: `886020173`
- Raw iOS version list: `reports/shopify/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `237419` (`10.2611.0`)
- Newest Android versionCode in the APKPure catalog: `281050` (`10.2620.0`)
- Raw Android version catalog: `reports/shopify/android-version-list.json`
- APKPure currently exposes a limited visible history on the fetched page.

## Next Step

Run initial sampling, starting with Android packages because APKs may expose clearer React Native evidence than encrypted iOS binaries.
