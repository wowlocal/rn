# Threads React Native Timeline

## Registration

- App name: Threads
- App Store ID: 6446901002
- iOS bundle ID: com.burbn.barcelona
- Android package: com.instagram.barcelona
- Status: version_lists_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- `ipatool search Threads --format json` resolved App Store ID `6446901002`, bundle ID `com.burbn.barcelona`, and current listed iOS version `431.0`.
- App Store URL: `https://apps.apple.com/us/app/threads/id6446901002`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.instagram.barcelona`.
- Android package history sources identified: APKMirror and APKPure pages for package `com.instagram.barcelona`.

## Version Lists

- iOS version list fetched on 2026-05-26 with `ipatool list-versions` through `check_rn_versions.py --list-versions-only`.
- iOS external version IDs available: 182
- Oldest iOS external version ID: `855897532`
- Newest iOS external version ID: `885819877`
- Raw iOS version list: `reports/threads/version-list.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from the visible APKPure source page: 10
- Oldest Android versionCode in the APKPure catalog: `504412928`
- Newest Android versionCode in the APKPure catalog: `510007506`
- Raw Android version catalog: `reports/threads/android-version-list.json`
- APKMirror was identified as a potentially richer Android history source, but automated fetches returned a Cloudflare challenge. APKPure is usable but currently exposes a limited visible history on the fetched page.

## Next Step

Sample Android packages if download links are usable, then sample iOS versions using the 182-entry App Store external version list.
