# Popular React Native iOS Apps Timeline Plan

Purpose: guide a long-running agent through collecting React Native upgrade timelines for popular iOS apps one app at a time. Treat this as a live checklist: update statuses as each app moves through discovery, sampling, boundary refinement, reporting, and cleanup.

## Ground Rules

- Work from `/Users/mike/src/tries/2026-05-25-rn`.
- Reuse and generalize the existing Discord scripts instead of starting from scratch.
- Process one app at a time unless a step is pure local reporting.
- Do not run concurrent `ipatool` commands; the cookie lock can collide.
- Keep all durable outputs before deleting any IPA.
- Delete only generated IPA/cache files inside this project when disk pressure requires it.
- Never delete scripts, manifests, reports, CSV/JSON outputs, or notes.
- Use IPA internal zip timestamps for build timestamps unless App Store metadata is independently verified.
- Report exact RN versions only when the IPA exposes strong markers. Otherwise report RN bands with confidence and evidence.
- Android APKs may be used as supplementary evidence for React Native detection and RN version inference when iOS binaries are encrypted or iOS JS markers are too sparse. Keep iOS timelines anchored to iOS App Store external version IDs and IPA internal zip timestamps.
- Do not expose account credentials in logs or reports.
- Commit after every completed checklist step so the task is resumable and each app's progress has a clear checkpoint.

## Git Checkpoints

- Commit after creating or updating task infrastructure, such as scripts, manifests, ignore rules, and report generators.
- Commit after each per-app checklist section is completed:
  - app registration
  - version list fetch
  - initial sampling
  - boundary refinement
  - disk cleanup
  - per-app notes
  - final per-app status update
- Commit after cross-app reports are regenerated.
- Keep commits small and descriptive, for example `Add Discord version list`, `Analyze Discord initial RN samples`, or `Refine Discord RN transition boundaries`.
- Do not commit downloaded IPAs, APKs, temporary app package files, Python bytecode, cache directories, or credentials.
- Before each commit, run `git status --short` and verify only intended files are staged.
- If a step produces a large generated report, commit the compact CSV/JSON/Markdown outputs, not the raw IPA.

## Output Layout

Create or maintain this structure:

```text
apps.json
reports/
  summary.md
  all-apps-rn-timeline.csv
  all-apps-rn-timeline.json
  all-apps-rn-transitions.csv
  all-apps-rn-transitions.json
  <app-slug>/
    version-list.json
    versions.csv
    versions.json
    ranges.csv
    ranges.json
    transitions.csv
    transitions.json
    notes.md
ipas/
  <app-slug>/
    retained-boundary-ipas...
apks/
  <app-slug>/
    retained-android-evidence-apks...
logs/
  run.log
  deleted-ipas.log
```

## Candidate App Queue

Start with these candidates. Verify RN usage from each IPA; do not assume.

- [ ] Discord
- [ ] Facebook
- [ ] Facebook Messenger
- [ ] Instagram
- [ ] Threads
- [ ] Meta Quest / Oculus / Horizon-related app
- [ ] Shopify
- [ ] Shop
- [ ] Coinbase
- [ ] Coinbase Wallet
- [ ] Kraken
- [ ] Microsoft Outlook
- [ ] Microsoft Teams
- [ ] Skype
- [ ] Pinterest
- [ ] Walmart
- [ ] Tesla
- [ ] Uber Eats
- [ ] SoundCloud
- [ ] Bloomberg
- [ ] Salesforce
- [ ] Wix
- [ ] Artsy
- [ ] NerdWallet
- [ ] Mattermost
- [ ] Bluesky

Add more candidates to `apps.json` as evidence appears.

## Per-App Checklist

Repeat this checklist for each app before moving to the next.

### 1. Register App

- [ ] Pick the next candidate from the queue.
- [ ] Resolve App Store app ID and bundle ID if possible.
- [ ] Add or update the app in `apps.json`.
- [ ] Set status to `queued`.
- [ ] Record source/evidence for why the app is being checked.
- [ ] Create `reports/<app-slug>/`.
- [ ] Create `ipas/<app-slug>/` only when downloads are needed.

Required `apps.json` fields:

```json
{
  "app_slug": "discord",
  "app_name": "Discord",
  "app_id": "985746746",
  "bundle_id": "com.hammerandchisel.discord",
  "status": "queued",
  "evidence": "Known public RN usage; verified by IPA markers",
  "last_completed_step": null,
  "notes": []
}
```

### 2. Fetch Version List

- [ ] Run `ipatool list-versions --app-id <app_id> --format json`.
- [ ] Save raw output to `reports/<app-slug>/version-list.json`.
- [ ] Count available external version IDs.
- [ ] Record newest and oldest external version IDs in `apps.json`.
- [ ] Mark app status as `version_list_fetched`.
- [ ] If `ipatool` cannot list versions, mark status `skipped` and document the error.

### 3. Initial Sampling

Do not download all versions first. Sample enough to determine whether the app actually exposes RN markers.

- [ ] Download latest available version.
- [ ] Download oldest available version.
- [ ] Download 6 to 12 evenly spaced historical versions.
- [ ] Analyze each downloaded IPA.
- [ ] Write provisional `versions.csv` and `versions.json`.
- [ ] Decide whether RN is detected.
- [ ] If no RN markers are detected in any sample, mark `not_react_native_detected` unless the app deserves deeper sampling.
- [ ] If RN markers are detected, continue to timeline refinement.

### 4. Per-IPA Analysis

For every IPA, capture at least:

- [ ] External version ID.
- [ ] App version.
- [ ] App build.
- [ ] Bundle ID.
- [ ] IPA internal build timestamp.
- [ ] IPA path.
- [ ] IPA size.
- [ ] Main executable path.
- [ ] Encryption status when visible.
- [ ] Hermes markers.
- [ ] JS bundle paths.
- [ ] React Native framework or library names.
- [ ] `react-native-renderer` marker, if present.
- [ ] React version marker, if present.
- [ ] RN JS API markers used for inference.
- [ ] RN guess or band.
- [ ] Confidence: `high`, `medium`, `low`, or `unknown`.
- [ ] Evidence notes explaining the inference.
- [ ] Android APK evidence used for RN inference, if any, clearly labeled as supplementary and not as an iOS timeline timestamp source.

### 5. Build Initial Ranges

- [ ] Sort analyzed rows by App Store external version order.
- [ ] Deduplicate repeated app version/build rows where needed.
- [ ] Group contiguous rows by RN guess and renderer version.
- [ ] Write provisional `ranges.csv` and `ranges.json`.
- [ ] Write provisional `transitions.csv` and `transitions.json`.
- [ ] Mark status `sampled`.

### 6. Refine Upgrade Boundaries

For each detected RN transition:

- [ ] Identify the last known old RN row.
- [ ] Identify the first known new RN row.
- [ ] Use the external version list to find all IDs between them.
- [ ] Download the midpoint or adjacent missing versions.
- [ ] Analyze new downloads.
- [ ] Regenerate `versions`, `ranges`, and `transitions`.
- [ ] Repeat until the old and new rows are adjacent in the external version list.
- [ ] If a version cannot be fetched, record the missing ID and reason.
- [ ] If exact adjacency cannot be reached, report the smallest remaining window.

Boundary output must include:

- [ ] Last old app version/build.
- [ ] Last old build timestamp.
- [ ] Last old external version ID.
- [ ] First new app version/build.
- [ ] First new build timestamp.
- [ ] First new external version ID.
- [ ] RN old guess.
- [ ] RN new guess.
- [ ] Confidence.
- [ ] Whether boundary is exact.
- [ ] Gap size in external version IDs.

### 7. Disk Cleanup Per App

After durable CSV/JSON files are written:

- [ ] Check free space with `df -h .`.
- [ ] Keep latest IPA if useful.
- [ ] Keep first and last IPA for each detected RN range if space allows.
- [ ] Keep both sides of exact or approximate upgrade boundaries if space allows.
- [ ] Delete intermediate sampled IPAs only when they are no longer needed.
- [ ] Log every deletion in `logs/deleted-ipas.log`.
- [ ] Confirm per-app reports can be regenerated from saved CSV/JSON without IPAs.

Deletion log format:

```text
timestamp=<iso8601> app=<slug> external_version_id=<id> app_version=<version> app_build=<build> path=<path> reason=<reason>
```

### 8. Per-App Notes

Write `reports/<app-slug>/notes.md` with:

- [ ] App identity and App Store ID.
- [ ] Coverage: oldest and newest analyzed builds.
- [ ] Number of external versions available.
- [ ] Number of IPAs downloaded.
- [ ] Number of unique builds analyzed.
- [ ] RN detection evidence.
- [ ] RN range table.
- [ ] RN transition table.
- [ ] Unresolved gaps or missing versions.
- [ ] Encryption limitations.
- [ ] Any app-specific marker quirks.
- [ ] Android APK corroboration, if used, including package version/build, APK source, extracted RN markers, and how it affects confidence.

### 9. Mark App Done

- [ ] Verify scripts compile.
- [ ] Verify per-app CSV/JSON is valid.
- [ ] Verify transitions are backed by rows in `versions.csv`.
- [ ] Verify exact boundaries are adjacent in `version-list.json`.
- [ ] Update `apps.json` status to `done`, `skipped`, or `needs_manual_review`.
- [ ] Append key findings to `reports/summary.md`.
- [ ] Move to the next app.

## Cross-App Reporting Checklist

Run this after every few apps and at the end.

- [ ] Rebuild `reports/all-apps-rn-timeline.csv`.
- [ ] Rebuild `reports/all-apps-rn-timeline.json`.
- [ ] Rebuild `reports/all-apps-rn-transitions.csv`.
- [ ] Rebuild `reports/all-apps-rn-transitions.json`.
- [ ] Update `reports/summary.md`.
- [ ] List apps analyzed successfully.
- [ ] List apps skipped and reasons.
- [ ] List exact upgrade boundaries by app.
- [ ] List approximate upgrade windows by app.
- [ ] Compare upgrade timing across apps.
- [ ] Highlight high-confidence transitions separately from marker-band estimates.

## Completion Criteria

The full run is complete when:

- [ ] Every queued candidate has status `done`, `skipped`, or `needs_manual_review`.
- [ ] Every app with RN markers has per-app versions, ranges, transitions, and notes files.
- [ ] Cross-app timeline and transition reports exist.
- [ ] Exact boundaries have adjacency checks recorded.
- [ ] Approximate boundaries clearly state gap size and missing IDs.
- [ ] Disk cleanup is logged.
- [ ] `reports/summary.md` explains confidence limits and methodology.

## Existing Discord Baseline

Use Discord as the reference implementation and sanity check:

- Existing analyzed app: Discord iOS.
- Current coverage: app `1.0 (4)` through `329.0 (100971)`.
- Existing outputs:
  - `discord-rn-versions.csv`
  - `discord-rn-versions.json`
  - `discord-rn-timeline-ranges.csv`
  - `discord-rn-timeline-transitions.csv`
  - `discord-rn-timeline.json`
- Existing scripts:
  - `check_discord_rn_versions.py`
  - `summarize_discord_rn_timeline.py`

First engineering task for the long-running agent: generalize these scripts into app-agnostic tools while preserving the Discord output as a regression check.
