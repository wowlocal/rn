# Agoda React Native Timeline

## Registration

- App name: Agoda: Cheap Flights & Hotels
- App Store ID: 440676901
- iOS bundle ID: com.agoda.consumer
- Android package: com.agoda.mobile.consumer
- Status: needs_manual_review
- Registration date: 2026-05-26

## Evidence

- User-provided App Store URL: `https://apps.apple.com/ru/app/agoda-%D0%BE%D1%82%D0%B5%D0%BB%D0%B8-%D0%B8-%D0%B0%D0%B2%D0%B8%D0%B0%D0%B1%D0%B8%D0%BB%D0%B5%D1%82%D1%8B/id440676901`.
- Apple iTunes lookup for App Store ID `440676901` returned seller `Agoda Company Pte. Ltd.`, bundle ID `com.agoda.consumer`, and current listed version `14.19.0`.
- Google Play identifies Android package `com.agoda.mobile.consumer`.
- APKPure and AndroidAPKsFree also identify Android package `com.agoda.mobile.consumer`.
- APKPure history URL identified: `https://apkpure.net/agoda-cheap-flights-hotels/com.agoda.mobile.consumer/versions`.
- AndroidAPKsFree old versions URL identified: `https://androidapks.com/agoda/com-agoda-mobile-consumer/old/`.

## Version Lists

- iOS version list initially failed on 2026-05-26 before the App Store license was available.
- After the App Store license was purchased, iOS version list fetch succeeded with `download_agoda_ios_versions.sh`.
- iOS external version IDs available: 537.
- Oldest iOS external version ID: `42072638`.
- Newest iOS external version ID: `886000512`.
- Raw iOS version list: `reports/agoda/version-list.json`.
- Earlier raw iOS version-list error: `reports/agoda/version-list-error.json`.
- APKPure catalog fetch returned a bot-cookie challenge for simple automated fetches; APKCombo returned HTTP `403`.
- AndroidAPKsFree catalog fetched on 2026-05-26 with `fetch_androidapksfree_versions.py`.
- Android entries available from AndroidAPKsFree sources: 35.
- Oldest AndroidAPKsFree versionCode: `82521` (`9.27.0`).
- Newest AndroidAPKsFree versionCode: `288069` (`12.18.0`).
- Raw Android version catalog: `reports/agoda/android-version-list.json`.
- Source-specific AndroidAPKsFree catalog: `reports/agoda/androidapksfree-version-list.json`.

## Android Sampling

- Android sampling date: 2026-05-26.
- Android packages downloaded and analyzed: 12.
- Android package source: AndroidAPKsFree visible old-version catalog.
- Sampled range: `9.27.0` (`82521`) through `12.18.0` (`288069`).
- Android RN markers detected: no.
- No sampled APK exposed React Native JS bundle paths, Hermes bytecode, React Native native libraries, or RN native metadata markers.
- Android reports: `reports/agoda/android-versions.csv`, `reports/agoda/android-ranges.csv`, `reports/agoda/android-transitions.json`, and source-specific `reports/agoda/androidapksfree-versions.csv`.

## iOS Sampling

- iOS download date: 2026-05-26.
- iOS IPAs downloaded: 12.
- iOS source-analysis rows retained: 3.
- Download command: `./download_agoda_ios_versions.sh`.
- Download directory: `ipas/agoda`.
- Downloaded external version IDs: `886000512`, `885709219`, `885427672`, `885268309`, `884884458`, `884712153`, `884375151`, `884096070`, `883837393`, `883577562`, `883339261`, `883091610`.
- Source-analyzed `14.19.0` build `383953.2`, external ID `886000512`: bundle ID `com.agoda.consumer`, minimum iOS `17.0`, source IPA SHA-256 `faeeeb44dfd29a380d3942bf354e92d9422ff6160d1087eb5819fdeb85bef71b`, size `349688413`; install failed on the iOS `16.7.7` device with `DeviceOSVersionTooLow`.
- Source-analyzed `14.12.0` build `366004.2`, external ID `884096070`: bundle ID `com.agoda.consumer`, minimum iOS `17.0`, source IPA SHA-256 `ba0a3b297dda54d0c0f8483cab4b10d83b11ee85d582768a84be862a8f5c43e0`, size `346676437`; not dumped because it also requires iOS `17.0`.
- Source-analyzed `13.40.0` build `310516.2`, external ID `879020412`: bundle ID `com.agoda.consumer`, minimum iOS `16.0`, source IPA SHA-256 `f5593f5d8d86149600fa4fc30470bb5695d0ae71bf18b148c5de165753f20c53`, size `325667569`; this was the newest sampled build installable on the iOS `16.7.7` device.
- All three source-analysis rows have no RN JS bundle and remain RN `unknown`; the two iOS `17.0` rows are `encrypted_native_only`.
- Source IPAs for `14.12.0` and `14.19.0` expose the same `CXPRoomGrid`/Capacitor/Cordova web bundle pattern as the decrypted `13.40.0` app, including React/React DOM `18.3.1` assets, but their native executables remain encrypted.
- iOS reports: `reports/agoda/versions.csv`, `reports/agoda/ranges.csv`, `reports/agoda/transitions.json`, and `reports/agoda/timeline.json`.

## Decrypted iOS Evidence

- Accepted decrypted dump for `13.40.0` build `310516.2`, external ID `879020412`: dumped IPA SHA-256 `18a1fcb71453017c66a5ae1a7b40f35e8875212050bd735e7e58577b1fbbba6a`, dumped size `205265996`, metadata matched source bundle/version/build, main executable `cryptid 0`, coverage `loaded_app_decrypted`.
- Dump context: `frida-ipa-extract --all-binaries` on device `Meoi`, hardware model `D201AP`, iOS `16.7.7` build `20H330`; full command and compact cryptid inventory are recorded in `reports/agoda/versions.csv`.
- Per-Mach-O inventory for `13.40.0`: 27 Mach-Os total; main executable and 24 bundled framework/dylib binaries decrypted; 2 app-extension executables remain encrypted; no non-extension Mach-Os remain encrypted.
- Remaining encrypted app extensions: `Agoda_Consumer_PushExtension.appex` and `Agoda_Consumer_WidgetExtension.appex`. Extension triggering was not pursued because no app-extension file or current source-row evidence points to React Native.
- Follow-up audit found the earlier native React Native/Hermes/JSI/Yoga result was a false positive from broad substring matching. Weak strings include `ios_react_native`/`ios_reactnative`, isolated `RCTView`, PayPal `hermes` paths, Google OMID `GADOMIDJSInvoker`/`jsInvoker`, and yoga amenity/icon labels.
- Strong native marker audit found no `RCTBridge`, `RCTRootView`, `RCTCxxBridge`, `facebook::react`, `ReactCommon`, `React-Core`, React Native framework link, Hermes executor/runtime marker, JSI runtime marker, or Yoga `YGNode`/`YGConfig` marker. The only relevant dynamic links are `CXPRoomGrid`, `ReactiveObjC`, `Capacitor`, and `Cordova`.
- Decrypted analysis for `13.40.0` finds no RN JS bundle, Hermes bytecode version, `react-native-renderer`, version-specific RN marker, strong native RN symbol, or linked RN/Hermes/Yoga framework. The row remains RN `unknown` with reason `no_js_or_native_rn_markers`.

## Web React / Capacitor Evidence

- `CXPRoomGrid.framework` contains `com.agoda.cxp.room-grid.bundle.bundle`, `public/index.html` titled `Capybara Room Grid`, and `capacitor.config.json` with app ID `com.agoda.mobile.capybara`.
- The embedded `CXPRoomGrid` web assets contain React/React DOM `18.3.1`, Ionic/Capacitor routing, and `createRoot` usage. This is web React inside a Capacitor/Cordova wrapper, not React Native.
- The latest source IPAs `14.12.0` and `14.19.0` expose `Capacitor.framework`, `Cordova.framework`, `CXPRoomGrid.framework`, `public/index.html`, and large `public/assets/app-*.js` web bundles; no RN bundle filenames, Hermes bytecode files, or RN framework filenames were visible in the source archives.

## Provisional Ranges

| Platform | RN guess | Confidence | Start | End | Builds |
|---|---|---|---|---|---:|
| iOS | unknown | low | 13.40.0 (`879020412`) | 14.19.0 (`886000512`) | 3 |
| Android | unknown | unknown | 9.27.0 (`82521`) | 12.18.0 (`288069`) | 12 |

## Open Gaps

- AndroidAPKsFree is source-limited and stale for this app; it stops at May 2024, while Google Play/App Store show newer 2026 releases.
- APKPure web metadata exposes newer packages, but direct automated package downloads were blocked by Cloudflare during this run.
- Current App Store IPAs `14.12.0` and `14.19.0` require iOS `17.0`, so they could not be decrypted on the available iOS `16.7.7` jailbroken device.
- The newest installable decrypted iOS build does not provide reliable React Native evidence after the false-positive audit. Current iOS `17.0` native executables remain encrypted, so the latest native-only path cannot be fully ruled out on this device.

## Next Step

Do not count Agoda as React Native evidence from the current dataset. Revisit with an iOS `17.x` jailbroken device for current Agoda IPAs, or inspect a downloadable current Android source, only if encrypted current-native evidence becomes boundary-priority.
