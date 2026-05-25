# Facebook iOS React Native Timeline

## Registration

- App name: Facebook
- App Store ID: 284882215
- Bundle ID: com.facebook.Facebook
- Status: skipped
- Registration date: 2026-05-25

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md`.
- App Store URL resolved as `https://apps.apple.com/us/app/facebook/id284882215`.
- `ipatool search facebook --format json` resolved bundle ID `com.facebook.Facebook` and current listed version `562.0.0`.

## Next Step

No IPA sampling was performed because `ipatool list-versions` failed before any external version IDs were available.

## Blocker

- `ipatool list-versions --app-id 284882215 --format json` failed with `received error: An unknown error has occurred`.
- `ipatool list-versions --bundle-identifier com.facebook.Facebook --format json` failed with the same error.
- `ipatool purchase --bundle-identifier com.facebook.Facebook --format json` failed with `unsupported protocol scheme ""`.
- Latest raw failed list response is preserved at `reports/facebook/version-list-error.json`.
