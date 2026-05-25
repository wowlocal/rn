# Instagram iOS React Native Timeline

## Registration

- App name: Instagram
- App Store ID: 389801252
- Bundle ID: com.burbn.instagram
- Status: version_list_fetched
- Registration date: 2026-05-25

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- App Store URL resolved as `https://apps.apple.com/us/app/instagram/id389801252`.
- `ipatool search instagram --format json` resolved bundle ID `com.burbn.instagram` and current listed version `430.0.0`.

## Next Step

Sample latest, oldest, and evenly spaced historical IPAs from `reports/instagram/version-list.json`.

## Version List

- External version IDs available: 795
- Oldest external version ID: `2948163`
- Newest external version ID: `885526725`
- Raw version list: `reports/instagram/version-list.json`
- Fetch note: `ipatool list-versions --app-id 389801252 --format json` returned Apple's generic unknown error, but `ipatool list-versions --bundle-identifier com.burbn.instagram --format json` succeeded.
