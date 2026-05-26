# Popular React Native Mobile Apps Timeline Plan

Purpose: guide a long-running agent through collecting React Native upgrade timelines for popular mobile apps one app at a time. Prefer the platform that exposes the clearest React Native evidence, then reconcile iOS and Android timelines where both package histories are available. Treat this as a live checklist: update statuses as each app moves through discovery, sampling, boundary refinement, reporting, and cleanup.

## Ground Rules

- Work from `/Users/mike/src/tries/2026-05-25-rn`.
- Reuse and generalize the existing Discord scripts instead of starting from scratch.
- Process one app at a time unless a step is pure local reporting.
- Do not run concurrent `ipatool` commands; the cookie lock can collide.
- APK analysis is first-class. Android packages are usually easier to inspect than App Store IPAs because they are not FairPlay-encrypted; they often expose clearer RN evidence through `assets/index.android.bundle`, Hermes bytecode, `libreactnativejni.so`, `libhermes.so`, SoLoader libraries, native symbols, and package resources.
- Use Android-first sampling when APK/APKS/XAPK/APKM history is easier to obtain or inspect. Use iOS IPAs to validate and anchor iOS-specific timelines when needed.
- Authorized jailbroken or Frida-capable iOS install-and-dump analysis is also first-class evidence when the dumped package is verified against the intended app identity and version. Encrypted App Store IPAs alone remain limited evidence, but an installed-and-dumped decrypted package can expose native RN constants, frameworks, symbols, JS bundles, Hermes bytecode, and resources directly.
- Prefer `dump_ios_ipa.py --method frida-ipa-extract --all-binaries` for iOS dumps when the patched extractor is available. This decrypts the main executable and every loaded encrypted Mach-O under the app bundle. App extensions may still require a separate trigger-and-attach workflow because `.appex` bundles are not normal launchable apps.
- Keep iOS and Android package timelines separate in the raw outputs. Merge them only in cross-app summary files with platform labels.
- Keep all durable outputs before deleting any IPA, APK, APKS, XAPK, APKM, or extracted package directory.
- Delete only generated app package/cache files inside this project when disk pressure requires it.
- Never delete scripts, manifests, reports, CSV/JSON outputs, or notes.
- Use IPA internal zip timestamps for build timestamps unless App Store metadata is independently verified.
- For Android, prefer version ordering by `versionCode`; use APK source publish dates only when the source clearly provides them. ZIP entry timestamps inside APKs can be build artifacts and should be labeled as package timestamps, not store release dates.
- Treat Android source catalogs as source-limited unless the source demonstrably provides a complete history for the package. Adjacent rows in a sparse APKPure/APKMirror-derived catalog are not exact transition boundaries by themselves.
- Record Android package hashes, embedded manifest metadata, and package identity when available. If a source returns duplicated package hashes, installer/wrapper APKs, or embedded version metadata that conflicts with the catalog row, treat the row as a source-quality finding, not an exact historical build.
- For iOS install-and-dump evidence, record the source IPA/external version ID when known, installed bundle ID, `CFBundleShortVersionString`, `CFBundleVersion`, dumped package hash, dump tool/version, device/iOS context, decrypted binary coverage, and visible encryption status such as `cryptid` for every Mach-O where available. If the installed or dumped metadata does not match the intended catalog row, treat the dump as a source-quality finding rather than historical evidence.
- Report exact RN versions only when the IPA exposes strong markers. Otherwise report RN bands with confidence and evidence.
- Android APKs may provide primary evidence for RN version inference. Keep platform-specific timestamps and version identifiers labeled clearly.
- Every `unknown` RN result must have a reason code and next action, such as `encrypted_native_only`, `no_js_bundle`, `ambiguous_marker_band`, `source_catalog_sparse`, `metadata_mismatch`, `extension_not_dumped`, or `tool_failure`.
- Only install, run, dump, or analyze apps and accounts we are authorized to use for this research. Do not expose account credentials, device secrets, or personally identifying device data in logs or reports.
- Commit after every completed checklist step so the task is resumable and each app's progress has a clear checkpoint.

## Git Checkpoints

- Commit after creating or updating task infrastructure, such as scripts, manifests, ignore rules, and report generators.
- Commit after each per-app checklist section is completed:
  - app registration
  - iOS or Android version list fetch
  - initial sampling
  - APK analyzer implementation or refinement
  - boundary refinement
  - disk cleanup
  - per-app notes
  - final per-app status update
- Commit after cross-app reports are regenerated.
- Keep commits small and descriptive, for example `Add Discord version list`, `Analyze Discord initial RN samples`, or `Refine Discord RN transition boundaries`.
- Do not commit downloaded IPAs, decrypted IPA dumps, APKs, temporary app package files, Python bytecode, cache directories, or credentials.
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
    ios-version-list.json
    android-version-list.json
    ios-versions.csv
    ios-versions.json
    android-versions.csv
    android-versions.json
    ios-ranges.csv
    ios-ranges.json
    android-ranges.csv
    android-ranges.json
    ios-transitions.csv
    ios-transitions.json
    android-transitions.csv
    android-transitions.json
    combined-ranges.csv
    combined-transitions.csv
    notes.md
ipas/
  <app-slug>/
    retained-boundary-ipas...
apks/
  <app-slug>/
    retained-android-evidence-apks...
logs/
  run.log
  deleted-packages.log
patches/
  frida-ipa-extract-all-binaries.patch
```

## Candidate App Queue

Start with these candidates. Verify RN usage from each IPA or Android package; do not assume.

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
- [ ] Resolve App Store app ID and iOS bundle ID if possible.
- [ ] Resolve Android package name if possible.
- [ ] Identify Android package history source, if available.
- [ ] Add or update the app in `apps.json`.
- [ ] Set status to `queued`.
- [ ] Record source/evidence for why the app is being checked.
- [ ] Create `reports/<app-slug>/`.
- [ ] Create `ipas/<app-slug>/` or `apks/<app-slug>/` only when downloads are needed.

Required `apps.json` fields:

```json
{
  "app_slug": "discord",
  "app_name": "Discord",
  "ios_app_id": "985746746",
  "ios_bundle_id": "com.hammerandchisel.discord",
  "android_package": "com.discord",
  "android_history_source": null,
  "status": "queued",
  "evidence": "Known public RN usage; verified by IPA markers",
  "last_completed_step": null,
  "notes": []
}
```

### 2. Fetch Version Lists

- [ ] If doing iOS, run `ipatool list-versions --app-id <ios_app_id> --format json`.
- [ ] Save raw iOS output to `reports/<app-slug>/ios-version-list.json`.
- [ ] Count available iOS external version IDs.
- [ ] Record newest and oldest iOS external version IDs in `apps.json`.
- [ ] If doing Android, fetch or build a version catalog from the chosen APK source.
- [ ] Save raw Android version catalog to `reports/<app-slug>/android-version-list.json`.
- [ ] For Android entries, capture package source, version name, version code, architecture/split info, publish date if available, and download URL or stable source identifier.
- [ ] Mark app status as `version_lists_fetched`.
- [ ] If neither iOS nor Android history can be listed, mark status `skipped` and document the error.

### 3. Initial Sampling

Do not download all versions first. Sample enough to determine whether the app actually exposes RN markers. Prefer Android sampling first when Android historical packages are available; it is usually easier to inspect and often exposes richer RN and Hermes evidence than encrypted iOS binaries.

- [ ] Download latest available Android package if available.
- [ ] Download oldest available Android package if available.
- [ ] Download 6 to 12 evenly spaced Android historical versions if available.
- [ ] Analyze each downloaded Android package.
- [ ] If Android confirms RN and yields usable RN version markers, use Android ranges to guide any iOS downloads.
- [ ] Download latest available iOS version if iOS timeline is in scope.
- [ ] Download oldest available iOS version if iOS timeline is in scope.
- [ ] Download 6 to 12 evenly spaced iOS historical versions if iOS timeline is in scope.
- [ ] Analyze each downloaded IPA.
- [ ] For iOS-only or iOS-primary apps, run all-binaries dumps for the newest sample, oldest sample, and any sample whose encrypted static analysis is `unknown` or low confidence.
- [ ] Keep a small queue of "dump next" iOS rows near suspected RN transitions instead of dumping every historical IPA immediately.
- [ ] Write provisional platform-specific `*-versions.csv` and `*-versions.json`.
- [ ] Decide whether RN is detected.
- [ ] If no RN markers are detected in any sample, mark `not_react_native_detected` unless the app deserves deeper sampling.
- [ ] If RN markers are detected, continue to timeline refinement.

### 4. Optional iOS Install-And-Dump Track

Use this track when encrypted iOS IPAs block native inspection and a jailbroken or Frida-capable device is available. Process builds one at a time so each dump can be tied back to a specific catalog row.

- [ ] Verify the target app/build is licensed and authorized for installation and analysis.
- [ ] Install the selected IPA on the device and record the external version ID, app version, build number, and bundle ID expected from the catalog.
- [ ] Launch the app once if the dump tool requires a running process.
- [ ] If using `frida-ipa-extract`, apply `patches/frida-ipa-extract-all-binaries.patch` to the local tool checkout when the checkout does not already support `--all-binaries`.
- [ ] Dump the installed app with `./dump_ios_ipa.py <ipa> --method frida-ipa-extract --all-binaries` when possible. Add `--skip-install --no-kill-before-dump` only when the exact intended build is already installed and metadata can still be matched.
- [ ] If SSH password auth is unavailable but libimobiledevice can see the phone, use the wrapper's `ideviceinstaller` install path and `ideviceinfo` device context rather than moving install verification outside the report.
- [ ] If a build crashes or destroys the Frida script when spawned, verify the exact installed build with `ideviceinstaller list --xml`, launch it once with a lightweight Frida command, then retry with `--skip-install --no-kill-before-dump --attach-running`.
- [ ] Fall back to main-executable-only Frida dumps or iDump only when the all-binaries path fails, and record the failure and fallback reason.
- [ ] Verify the dumped `Info.plist` bundle ID, `CFBundleShortVersionString`, and `CFBundleVersion` match the intended row.
- [ ] Run a Mach-O encryption inventory over the dumped IPA and record `cryptid` for the main executable, loaded frameworks, dylibs, embedded app extensions, and other executable files.
- [ ] Classify decrypted binary coverage:
  - `full_bundle_decrypted`: every bundled Mach-O reports `cryptid 0`.
  - `loaded_app_decrypted`: main executable and loaded app/framework Mach-Os report `cryptid 0`, but non-loaded extensions or helper executables remain encrypted.
  - `main_only_decrypted`: only the main app executable reports `cryptid 0`.
  - `rejected`: metadata mismatch, missing output, or main executable is still encrypted.
- [ ] For encrypted `.appex` executables that matter to the RN question, trigger the extension manually, attach to the extension host/process, and dump that process separately. If the extension cannot be triggered, record `extension_not_dumped` rather than treating the whole app dump as failed.
- [ ] Record dump tool name/version, host timestamp, device model class if useful, iOS version, dumped IPA hash, dump output size, decrypted coverage class, and visible encryption status such as `cryptid` where available.
- [ ] Analyze the decrypted dump for RN markers in native frameworks, main executable strings/symbols, JS bundles, Hermes bytecode, resources, and package metadata.
- [ ] If dump metadata does not match the intended catalog row, reject it as historical evidence and record the mismatch in notes.
- [ ] Delete or retain the dump according to disk policy after compact CSV/JSON evidence is written.

### 5. Per-Package Analysis

For every encrypted/downloaded or decrypted/dumped iOS package, capture at least:

- [ ] External version ID.
- [ ] App version.
- [ ] App build.
- [ ] Bundle ID.
- [ ] IPA internal build timestamp.
- [ ] IPA path.
- [ ] IPA size.
- [ ] Package source: encrypted App Store IPA, decrypted installed dump, simulator/developer build, or other authorized source.
- [ ] Package SHA-256 hash.
- [ ] Dump tool/version and device/iOS context, if dumped from an installed app.
- [ ] Main executable path.
- [ ] Encryption status when visible, including a per-Mach-O `cryptid` inventory for decrypted dumps.
- [ ] Decrypted binary coverage class: `full_bundle_decrypted`, `loaded_app_decrypted`, `main_only_decrypted`, `rejected`, or blank for encrypted source IPAs.
- [ ] Remaining encrypted executable paths, if any.
- [ ] Hermes markers.
- [ ] JS bundle paths.
- [ ] React Native framework or library names.
- [ ] `react-native-renderer` marker, if present.
- [ ] React version marker, if present.
- [ ] RN JS API markers used for inference.
- [ ] Native RN markers from decrypted main/framework binaries, especially when no JS bundle or renderer marker is present.
- [ ] RN guess or band.
- [ ] Confidence: `high`, `medium`, `low`, or `unknown`.
- [ ] Unknown reason code, if confidence is `unknown`.
- [ ] Next action for unknown or low-confidence rows.
- [ ] Evidence notes explaining the inference.

For every Android package, capture at least:

- [ ] Android package name.
- [ ] Version name.
- [ ] Version code.
- [ ] Source and source publish date, if available.
- [ ] Package file path.
- [ ] Package file type: APK, APKS, XAPK, APKM, or extracted split set.
- [ ] Package size.
- [ ] Supported ABIs and split metadata.
- [ ] Manifest app metadata.
- [ ] `assets/index.android.bundle` or other JS bundle paths.
- [ ] Hermes bytecode markers and Hermes version markers, if visible.
- [ ] React Native native libraries such as `libreactnativejni.so`, `libreact_nativemodule_core.so`, `libfabricjni.so`, `libhermes.so`, and SoLoader libraries.
- [ ] Native symbols or strings mentioning `ReactNativeVersion`, `ReactAndroid`, `TurboModule`, `Fabric`, `JSI`, `Hermes`, or `Bridgeless`.
- [ ] `react-native-renderer` marker, if present.
- [ ] React version marker, if present.
- [ ] RN JS API markers used for inference.
- [ ] RN guess or band.
- [ ] Confidence: `high`, `medium`, `low`, or `unknown`.
- [ ] Unknown reason code, if confidence is `unknown`.
- [ ] Next action for unknown or low-confidence rows.
- [ ] Evidence notes explaining the inference.

Android analysis tools may include `unzip`, `aapt`/`aapt2`, `apkanalyzer`, `jadx`, `apktool`, `readelf`, `nm`, `strings`, Hermes bytecode tooling, and structured ZIP/APK parsers. Prefer structured metadata extraction over ad hoc string scraping when available.

### 6. Evidence Ladder And Confidence

Use the strongest available evidence for each package row, and keep weaker evidence as supporting context instead of replacing platform-specific findings.

| Evidence type | Typical confidence impact | Required validation |
| --- | --- | --- |
| Exact RN version string or renderer marker from decrypted native code, JS bundle, Hermes metadata, or Android native libraries | Can support `high` for the row | Package identity matches, marker is directly extracted, and analyzer records the exact file/member |
| Decrypted iOS main executable plus loaded frameworks with compatible JS/Hermes markers | Can support `high` for RN family or `medium` to `high` for exact version depending on marker specificity | Dump metadata matches source IPA, main executable `cryptid 0`, loaded RN/Hermes-related frameworks `cryptid 0` |
| Android APK/APKS with RN native libraries and JS/Hermes markers | Can support `medium` or `high` depending on exact marker availability | Manifest package/version metadata matches catalog, source catalog is not known duplicated/wrapper-only |
| Encrypted IPA with JS bundle markers only | Usually `medium` for version band, rarely exact | IPA metadata matches catalog and markers are unambiguous for the band |
| Generic RN strings only, sparse source catalog, or conflicting platform evidence | `low` or `unknown` | Record reason code and next action |

Confidence rules:

- [ ] Use `high` only when exact RN version or narrow version family is backed by direct package evidence and metadata validation.
- [ ] Use `medium` when markers identify a constrained RN band but exact patch/minor cannot be proven.
- [ ] Use `low` when only generic RN presence or broad-era markers are visible.
- [ ] Use `unknown` when RN cannot be inferred, and always fill `unknown_reason` plus `next_action`.
- [ ] Do not promote confidence only because Android and iOS are near the same calendar date. Cross-platform agreement can strengthen a compatible platform-specific inference, but it is not a substitute for platform evidence.

Unknown triage rules:

- [ ] If native iOS code is encrypted, try the install-and-dump track on the latest row and on rows near suspected transitions.
- [ ] If all loaded app/framework binaries are decrypted but app extensions remain encrypted, continue unless RN evidence is expected to live only in the extension.
- [ ] If Android source catalogs are sparse, mark transition windows as source-limited and prefer iOS external-version adjacency for iOS boundaries.
- [ ] If JS/Hermes markers conflict with native markers, keep the row `needs_manual_review` and preserve both marker sets in notes.

### 7. Build Initial Ranges

- [ ] Sort iOS rows by App Store external version order.
- [ ] Sort Android rows by version code, then source publish date if available.
- [ ] Deduplicate repeated app version/build or versionCode rows where needed.
- [ ] Group contiguous rows by RN guess and renderer version.
- [ ] Write provisional platform-specific `*-ranges.csv` and `*-ranges.json`.
- [ ] Write provisional platform-specific `*-transitions.csv` and `*-transitions.json`.
- [ ] Mark status `sampled`.

### 8. Refine Upgrade Boundaries

For each detected RN transition on each platform:

- [ ] Identify the last known old RN row.
- [ ] Identify the first known new RN row.
- [ ] For iOS, use the external version list to find all IDs between them.
- [ ] For Android, use the versionCode/source catalog to find all versions between them.
- [ ] Download the midpoint or adjacent missing versions.
- [ ] Analyze new downloads.
- [ ] Regenerate `versions`, `ranges`, and `transitions`.
- [ ] Repeat until the old and new rows are adjacent in the platform version catalog.
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
- [ ] Confidence basis: exact marker, decrypted-native marker, Android native marker, JS/Hermes band, cross-platform compatible support, or source-limited estimate.
- [ ] Whether boundary is exact.
- [ ] Gap size in external version IDs.
- [ ] Platform: `ios` or `android`.
- [ ] Android package source and versionCode gap size, when platform is Android.

Cross-platform refinement:

- [ ] Use Android transitions to prioritize iOS sampling near the same calendar window or release train when iOS analysis is expensive.
- [ ] Do not copy an Android RN version onto iOS without evidence. Mark it as Android evidence that increases confidence only when iOS markers are compatible.
- [ ] If Android and iOS upgrade on different app versions or dates, report separate timelines.
- [ ] For each suspected transition, decrypt at least the first row after the boundary and the last row before the boundary when encrypted iOS native evidence is the limiting factor.

### 9. Disk Cleanup Per App

After durable CSV/JSON files are written:

- [ ] Check free space with `df -h .`.
- [ ] Keep latest IPA if useful.
- [ ] Keep latest APK if useful.
- [ ] Keep first and last IPA for each detected RN range if space allows.
- [ ] Keep first and last Android package for each detected RN range if space allows.
- [ ] Keep both sides of exact or approximate upgrade boundaries if space allows.
- [ ] Delete intermediate sampled IPAs/APKs only when they are no longer needed.
- [ ] Log every deletion in `logs/deleted-packages.log`.
- [ ] Confirm per-app reports can be regenerated from saved CSV/JSON without app package files.

Deletion log format:

```text
timestamp=<iso8601> app=<slug> platform=<ios|android> version_id=<id> app_version=<version> app_build_or_version_code=<build_or_code> path=<path> reason=<reason>
```

### 10. Per-App Notes

Write `reports/<app-slug>/notes.md` with:

- [ ] App identity and App Store ID.
- [ ] Android package identity and APK source, if used.
- [ ] Coverage: oldest and newest analyzed builds per platform.
- [ ] Number of external versions available per platform.
- [ ] Number of IPAs downloaded.
- [ ] Number of Android packages downloaded.
- [ ] Number of unique builds analyzed.
- [ ] RN detection evidence.
- [ ] RN range table per platform.
- [ ] RN transition table per platform.
- [ ] Cross-platform comparison table if both platforms were analyzed.
- [ ] Unresolved gaps or missing versions.
- [ ] Encryption limitations.
- [ ] Decrypted binary coverage class for each iOS dump: `full_bundle_decrypted`, `loaded_app_decrypted`, `main_only_decrypted`, or `rejected`.
- [ ] Remaining encrypted bundled executables, especially `.appex` binaries, and whether they affect the RN conclusion.
- [ ] Any app-specific marker quirks.
- [ ] Android APK evidence, if used, including package version/code, APK source, extracted RN markers, and how it affects confidence.
- [ ] iOS dump evidence, if used, including dump tool/version, package hash, installed bundle metadata, decrypted native markers, and how it affects confidence.

### 11. Mark App Done

- [ ] Verify scripts compile.
- [ ] Verify per-app CSV/JSON is valid.
- [ ] Verify transitions are backed by rows in platform-specific `*-versions.csv`.
- [ ] Verify exact iOS boundaries are adjacent in `ios-version-list.json`.
- [ ] Verify exact Android boundaries are adjacent in a complete `android-version-list.json`; if the source catalog is sparse or source-limited, mark the boundary as source-limited even when fetched rows are adjacent.
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
- [ ] List exact upgrade boundaries by app and platform.
- [ ] List approximate upgrade windows by app and platform.
- [ ] Compare upgrade timing across apps.
- [ ] Compare Android and iOS timing within the same app when both are available.
- [ ] Highlight high-confidence transitions separately from marker-band estimates.

Cross-app CSV/JSON rows should include:

- [ ] App slug and app name.
- [ ] Platform.
- [ ] Package identifier: iOS bundle ID or Android package name.
- [ ] Store/source identifier: iOS app ID, iOS external version ID, or Android source/versionCode.
- [ ] App version and build/versionCode.
- [ ] Timestamp type: IPA zip timestamp, Android source publish date, Android package timestamp, or unknown.
- [ ] RN guess or band.
- [ ] Renderer version if known.
- [ ] Confidence.
- [ ] Evidence summary.

## Completion Criteria

The full run is complete when:

- [ ] Every queued candidate has status `done`, `skipped`, or `needs_manual_review`.
- [ ] Every app with RN markers has per-platform versions, ranges, transitions, and notes files for the platforms analyzed.
- [ ] Cross-app timeline and transition reports exist.
- [ ] Exact boundaries have adjacency checks recorded.
- [ ] Approximate boundaries clearly state gap size and missing IDs.
- [ ] Disk cleanup is logged.
- [ ] `reports/summary.md` explains confidence limits and methodology.

## Existing Discord Baseline

Use Discord iOS as the reference implementation and sanity check:

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

First engineering task for the long-running agent: generalize these scripts into app-agnostic, platform-aware tools while preserving the Discord iOS output as a regression check. Then add Android package analysis support and use Discord Android, if fetchable, as the first APK/APKS analyzer validation target.
