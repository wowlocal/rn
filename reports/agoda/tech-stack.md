# Agoda iOS Tech Stack Notes

Analysis target: decrypted iOS `13.40.0` build `310516.2`, external version ID `879020412`.

Artifact: `tmp/agoda-1340-decrypted/Payload/Agoda_Consumer.app`.

## Executive Summary

Agoda is primarily a native iOS app, written in Swift and Objective-C, with a large modular native codebase and resource-bundle layout. The decrypted build embeds a substantial web React room-grid module inside `CXPRoomGrid.framework`, packaged with Capacitor/Cordova and Ionic. This is web React running in a WebKit/Capacitor context, not React Native.

No reliable React Native runtime evidence was found in the decrypted native app. `RCTRootView`/`RCTView` strings exist inside Facebook SDK codeless-event matching code, and other weak strings come from unrelated SDKs or business labels; they are not evidence that Agoda links or runs React Native.

## Native Host

- Bundle ID: `com.agoda.consumer`
- App version/build: `13.40.0` / `310516.2`
- Main executable: Mach-O arm64, decrypted (`cryptid 0`)
- Build metadata: Xcode `16.1`, SDK `iphoneos18.1`, minimum iOS `16.0`
- App size: `416M`; main executable: `199M`; embedded frameworks: `63M`
- Native UI evidence: `280` NIB files, `108` storyboard entries, two Core Data model directories
- Main Apple frameworks linked: UIKit, SwiftUI, Combine, WebKit, JavaScriptCore, CoreData, CoreLocation, CoreMotion, ActivityKit, AppIntents, AppTrackingTransparency, AuthenticationServices, StoreKit, SafariServices, PDFKit, MetricKit, UserNotifications, MapKit, Metal
- Swift evidence: extensive Swift runtime linkage plus Swift symbols such as `Agoda_Consumer`, `LegacyCore`, `LegacyContract`, `NetworkStack`, `GraphQLEntity`, `UIComponents`, `SearchFunnel`
- Architecture naming in symbols strongly suggests VIPER/Clean-style modules: `ModuleBuilder`, `Interactor`, `Presenter`, `Router`, `Assembly`, `Repository`, `ViewController`

## Embedded Web React Module

The strongest non-native UI stack is `Frameworks/CXPRoomGrid.framework/com.agoda.cxp.room-grid.bundle.bundle`.

- Native wrapper: `CXPRoomGrid.framework`
- Web wrapper/runtime: `Capacitor.framework` and `Cordova.framework`
- Capacitor app ID/name: `com.agoda.mobile.capybara` / `capybara`
- Capacitor server host: `capybara.agoda.com`
- Web app title: `Capybara Room Grid`
- Entry point: `public/index.html` with root node `<div id="root"></div>`
- Bundler/tooling evidence: Vite module/legacy script layout and pnpm paths in `roomgrid.json` / `build/stats.html`
- Main decrypted web assets:
  - `assets/app-BFPshl6V.js`: `9.1M`
  - `assets/app-legacy-4LZG-ttd.js`: `11.8M`
  - `assets/app-CkGi66qI.css`: `2.9M`
- Web app stack evidence:
  - React `18.3.1`
  - React DOM `18.3.1`
  - Ionic Core `7.4.1`
  - Capacitor packages including `@agoda/capacitor.core@5.5.10`, `@capacitor/share@5.0.6`, `@capacitor/clipboard@5.0.6`
  - TanStack Query `5.51.21`
  - Zustand `4.5.0`
  - Immer `10.0.3`
  - Zod `4.1.7`
  - React Aria packages
  - Agoda packages including `@agoda/capylink`, `@agoda/statesync`, `@agoda/messaging-client`, `@agoda/performance-client`, analytics packages, and CMS client
  - Agoda design systems including `@drone-js/*` and `@kite-js/*`
- Business-domain strings in the web bundle point to room grid, property, cart, packages, pricing, chatbot/Aide, analytics, and webview state-sync flows.

The newer source-only iOS builds `14.12.0` and `14.19.0` still expose the same `CXPRoomGrid`/Capacitor/Cordova web asset pattern, but their native executables require iOS `17.0` and were not decrypted on the available iOS `16.7.7` device.

## Native Third-Party SDKs

Embedded dynamic frameworks:

- Appboy/Braze: `Appboy_iOS_SDK.framework` `4.5.0`
- Capacitor/Cordova: `Capacitor.framework`, `Cordova.framework`
- Payments/risk: `CardinalMobile.framework` `2.2.3`, `PPRiskMagnes.framework`, `RiskifiedBeacon.framework`, `ForterSDK.framework` `2.3.4`, `FingerprintPro.framework` `2.0.1`
- Social/auth: Facebook SDK frameworks `13.0.0`, `LineSDK.framework` `5.11.2`
- Maps: `NMapsMap.framework` `3.18.1`, `NMapsGeometry.framework` `1.0.2`, plus Google Maps and Baidu map resource bundles
- UI/media: `Lottie.framework` `4.5.0`, `SDWebImage.framework` `5.21.0`
- Utility/reactive: `ReactiveObjC.framework` `2.1.2`, `Mantle.framework` `1.5.8`
- Privacy/consent: `OTPublishersHeadlessSDK.framework` `202410.1.0`
- Agoda/proprietary: `CXPRoomGrid.framework`, `NavigatorUI.framework`, `PerformanceSuite.framework`

Pods/settings metadata also lists AFNetworking, Alamofire, AppsFlyer, Braintree, Firebase Analytics/Crashlytics/Performance/Remote Config/Sessions/Installations, GCDWebServer, Google Mobile Ads, Google Analytics/AppMeasurement, Google User Messaging Platform, GT3Captcha, IGListKit, JLRoutes, Kakao SDKs, ReSwift, WechatOpenSDK, Yams, lottie-ios, and nanopb.

## Data, Network, And Services

- Native networking evidence: Alamofire, AFNetworking, URLSession, GraphQL modules, protobuf/nanopb, Braintree GraphQL, GCDWebServer
- Persistence evidence: CoreData, SQLite, `ChatStorageDataModel.momd`, Google Maps cache model
- Firebase config:
  - Project: `agoda-dd55`
  - Google app ID: `1:552028937321:ios:baad1459baeecc19`
  - GCM and Sign-In enabled; Analytics disabled in `GoogleService-Info.plist`
- Shipped Agoda endpoints include production and non-production hosts such as `accountapi.agoda.com`, `bookapi.agoda.com`, `searchapi.agoda.com`, `gw.agoda.com`, `www.agoda.com`, `qa*`, `pre-*`, `mock-gw.agodadev.io`, and `localhost:8080`.

## App Extensions

Two extension executables remained encrypted in the dump, but their metadata and load commands are visible:

- `com.agoda.consumer.pushnotificationservice`: iOS notification service extension, links Foundation/UserNotifications and Swift runtime.
- `com.agoda.consumer.widgetservice`: WidgetKit extension, links WidgetKit, SwiftUI, ActivityKit, Foundation, and Swift runtime.

No extension metadata or load-command evidence points to React Native.

## Not React Native

Negative RN checks on the decrypted app:

- No `main.jsbundle`, `.hbc`, Hermes bytecode, or React Native bundle filename in the app bundle.
- No React Native, Hermes, Yoga, or React-Core framework in linked dynamic libraries.
- No non-Facebook strong runtime markers such as `RCTBridge`, `RCTCxxBridge`, `ReactNativeVersion`, `react-native-renderer`, `facebook::react`, `ReactCommon`, `HermesExecutor`, `HermesRuntime`, `JSCRuntime`, `YGNode`, or `YGConfig`.
- `RCTRootView`/`RCTView` strings are present in `FBSDKCoreKit.framework` as part of Facebook codeless event matching for RN apps, so they are third-party detection strings.
- Weak strings such as `hermes`, `jsInvoker`, and `yoga` map to unrelated SDK paths, Google OMID JS invocation, or ordinary travel/amenity labels.

Conclusion: classify this decrypted iOS build as native Swift/Obj-C plus Capacitor/Ionic/web React, not React Native.

