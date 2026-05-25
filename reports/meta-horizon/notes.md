# Meta Horizon React Native Timeline

## Registration

- App name: Meta Horizon
- App Store ID: 1366478176
- iOS bundle ID: com.oculus.twilight
- Android package: com.oculus.twilight
- Status: version_lists_fetched
- Registration date: 2026-05-26

## Evidence

- Candidate listed in `POPULAR_RN_APPS_ANALYSIS_PLAN.md` as Meta Quest / Oculus / Horizon-related app.
- `ipatool search "Meta Horizon" --format json` resolved App Store ID `1366478176`, bundle ID `com.oculus.twilight`, and current listed iOS version `372.1`.
- App Store URL: `https://apps.apple.com/us/app/meta-horizon/id1366478176`.
- Google Play package URL: `https://play.google.com/store/apps/details?id=com.oculus.twilight`.
- Android package history sources identified: APKMirror and APKPure pages for package `com.oculus.twilight`.

## Version Lists

- iOS version list fetch attempted on 2026-05-26 with `ipatool list-versions` by app ID `1366478176` and bundle ID `com.oculus.twilight`.
- iOS version list result: failed because `ipatool` reports `license is required`.
- iOS license attempt: `ipatool purchase --bundle-identifier com.oculus.twilight --format json` failed with `unsupported protocol scheme ""`.
- Raw iOS version-list error: `reports/meta-horizon/version-list-error.json`
- Android APKPure catalog fetched on 2026-05-26 with `fetch_apkpure_versions.py`.
- Android entries available from APKPure sources: 10
- Oldest Android versionCode in the APKPure catalog: `930594021` (`366.0.0.24.290`)
- Newest Android versionCode in the APKPure catalog: `975394013` (`372.0.1.34.252`)
- Raw Android version catalog: `reports/meta-horizon/android-version-list.json`
- APKMirror was identified as a potentially richer Android history source, but automated fetches returned a Cloudflare challenge. APKPure is usable but currently exposes a limited visible history on the fetched page.

## Next Step

Run initial Android sampling against the APKPure catalog before deciding whether this source is sufficient or the app needs manual review for older APKMirror packages.
