#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import posixpath
import re
import shutil
import zipfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from lxml import html

from check_rn_versions import bytes_text_match, infer_react_native


ANDROID_FIELDS = [
    "android_package",
    "version_name",
    "version_code",
    "source",
    "source_publish_date",
    "source_publish_date_raw",
    "download_url",
    "package",
    "package_file_type",
    "package_size",
    "package_sha256",
    "supported_abis",
    "split_metadata",
    "manifest_metadata",
    "apk_entries",
    "js_bundle_paths",
    "hermes_markers",
    "react_native_libraries",
    "native_symbol_markers",
    "react_renderer",
    "hbc_version",
    "rn_guess",
    "confidence",
    "evidence_notes",
]

RN_LIBRARY_PATTERNS = (
    "reactnative",
    "react_native",
    "react-featureflags",
    "react_featureflags",
    "fabric",
    "turbomodule",
    "hermes",
    "jsi",
    "yoga",
)

NATIVE_MARKERS = (
    "ReactNativeVersion",
    "ReactAndroid",
    "TurboModule",
    "Fabric",
    "JSI",
    "Hermes",
    "Bridgeless",
    "reactnativejni",
    "react_featureflagsjni",
)


def sanitize(value: str) -> str:
    value = value.strip() or "unknown"
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value.strip("_") or "unknown"


def fetch_text(url: str, timeout: int = 30) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def download_binary(url: str, out: Path, timeout: int = 120) -> None:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
            )
        },
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    with urlopen(request, timeout=timeout) as response, tmp.open("wb") as f:
        shutil.copyfileobj(response, f)
    tmp.replace(out)


def load_catalog(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text())
    versions = data.get("versions", [])
    if not isinstance(versions, list):
        raise ValueError(f"{path} does not contain a versions list")
    return [row for row in versions if isinstance(row, dict)]


def catalog_sort_key(entry: dict[str, Any]) -> tuple[int, str]:
    version_code = str(entry.get("version_code", ""))
    return (
        int(version_code) if version_code.isdigit() else -1,
        str(entry.get("source_publish_date", "")),
    )


def direct_download_url(entry: dict[str, Any], timeout: int) -> str:
    page_url = str(entry.get("download_url", ""))
    version_code = str(entry.get("version_code", ""))
    if not page_url:
        return ""
    path = urlparse(page_url).path.lower()
    if path.endswith((".apk", ".apks", ".xapk", ".apkm")):
        return page_url
    document = html.fromstring(fetch_text(page_url, timeout=timeout))
    hrefs = [href for href in document.xpath("//a[@href]/@href") if "d.apkpure.net/b/" in href]
    if version_code:
        exact = [href for href in hrefs if f"versionCode={version_code}" in href]
        if exact:
            return exact[0]
    return hrefs[0] if hrefs else ""


def package_extension(entry: dict[str, Any]) -> str:
    package_type = str(entry.get("package_file_type", "")).lower()
    if "xapk" in package_type:
        return ".xapk"
    if "apks" in package_type:
        return ".apks"
    if "apkm" in package_type:
        return ".apkm"
    return ".apk"


def download_package(
    entry: dict[str, Any],
    *,
    app_slug: str,
    download_dir: Path,
    force: bool,
    timeout: int,
) -> Path:
    version_code = str(entry.get("version_code", ""))
    version_name = str(entry.get("version_name", ""))
    out = download_dir / f"{app_slug}_{sanitize(version_code)}_{sanitize(version_name)}{package_extension(entry)}"
    if out.exists() and not force:
        print(f"already exists: {out}")
        return out
    url = direct_download_url(entry, timeout)
    if not url:
        raise RuntimeError(f"no direct download URL found for {version_name} ({version_code})")
    print(f"downloading {version_name} ({version_code}) -> {out}")
    download_binary(url, out, timeout=timeout)
    return out


def is_js_bundle(name: str) -> bool:
    lower = name.lower()
    if lower.endswith((".jsbundle", ".hbc")):
        return True
    basename = posixpath.basename(lower)
    if not lower.startswith("assets/") or "bundle" not in basename:
        return False
    ignored_suffixes = (
        ".json",
        ".bin",
        ".dat",
        ".param",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".timestamp",
        ".filesize",
    )
    return not basename.endswith(ignored_suffixes)


def inspect_bundle(data: bytes) -> dict[str, Any]:
    renderer = bytes_text_match(data, rb"react-native-renderer:?\s*([0-9]+\.[0-9]+\.[0-9]+)")
    hbc_version = ""
    if data[:4] in {b"\xc6\x1f\xbc\x03", b"HBC\x00"}:
        hbc_version = "present"
    has_virtual = b"VirtualViewMode" in data
    has_rnv_export = b"ReactNativeVersion" in data
    has_logbox = b"unstable_enableLogBox" in data
    has_layout_conformance = b"experimental_LayoutConformance" in data
    has_register_callable = b"registerCallableModule" in data
    has_dev_menu = b"DevMenu" in data
    has_set_up_dom = b"setUpDOM" in data
    has_use_animated_value = b"useAnimatedValue" in data
    has_segmented_control_ios = b"SegmentedControlIOS" in data
    has_date_picker_android = b"DatePickerAndroid" in data
    has_picker_ios = b"PickerIOS" in data
    has_status_bar_ios = b"StatusBarIOS" in data
    has_root_tag_context = b"RootTagContext" in data
    has_unstable_root_tag_context = b"unstable_RootTagContext" in data
    has_platform_color = b"PlatformColor" in data
    has_dynamic_color_ios = b"DynamicColorIOS" in data
    has_pressable = b"Pressable" in data
    has_color_android = b"ColorAndroid" in data
    has_check_box = b"CheckBox" in data
    has_tv_event_handler = b"TVEventHandler" in data
    has_use_window_dimensions = b"useWindowDimensions" in data
    has_native_dialog_manager_android = b"NativeDialogManagerAndroid" in data
    has_turbo_module_registry = b"TurboModuleRegistry" in data
    has_virtualized_section_list = b"VirtualizedSectionList" in data
    has_app_registry = b"AppRegistry" in data
    has_batched_bridge = b"BatchedBridge" in data
    has_native_modules = b"NativeModules" in data
    has_style_sheet = b"StyleSheet" in data
    guess, confidence, reason = infer_react_native(
        renderer,
        has_virtual,
        has_rnv_export,
        has_logbox,
        has_layout_conformance,
        has_register_callable,
        has_dev_menu,
        has_set_up_dom,
        has_use_animated_value,
        has_segmented_control_ios,
        has_date_picker_android,
        has_picker_ios,
        has_status_bar_ios,
        has_root_tag_context,
        has_unstable_root_tag_context,
        has_platform_color,
        has_dynamic_color_ios,
        has_pressable,
        has_color_android,
        has_check_box,
        has_tv_event_handler,
        has_use_window_dimensions,
        has_native_dialog_manager_android,
        has_turbo_module_registry,
        has_virtualized_section_list,
        has_app_registry,
        has_batched_bridge,
        has_native_modules,
        has_style_sheet,
    )
    return {
        "renderer": renderer,
        "hbc_version": hbc_version,
        "rn_guess": guess,
        "confidence": confidence,
        "reason": reason,
        "has_rn_marker": any(
            [
                renderer,
                has_virtual,
                has_rnv_export,
                has_logbox,
                has_register_callable,
                has_app_registry,
                has_batched_bridge,
                has_native_modules,
                has_style_sheet,
            ]
        ),
    }


def inspect_apk_bytes(apk_data: bytes, label: str) -> dict[str, Any]:
    with zipfile.ZipFile(io.BytesIO(apk_data)) as zf:
        names = zf.namelist()
        abis = sorted({parts[1] for name in names if (parts := name.split("/")) and len(parts) >= 3 and parts[0] == "lib"})
        library_names = [name for name in names if name.startswith("lib/") and name.endswith(".so")]

        metadata_texts: list[str] = []
        for metadata_name in ("assets/native_deps.txt", "assets/lib/metadata.txt"):
            if metadata_name in names:
                metadata_texts.append(zf.read(metadata_name).decode("utf-8", "replace"))

        metadata_lines = "\n".join(metadata_texts).splitlines()
        metadata_libraries = [
            line.split()[0]
            for line in metadata_lines
            if line.strip() and any(pattern in line.lower() for pattern in RN_LIBRARY_PATTERNS)
        ]
        rn_libraries = sorted(
            {
                Path(name).name
                for name in library_names
                if any(pattern in name.lower() for pattern in RN_LIBRARY_PATTERNS)
            }
            | set(metadata_libraries)
        )

        marker_text = "\n".join(metadata_texts)
        native_markers = sorted({marker for marker in NATIVE_MARKERS if marker.lower() in marker_text.lower()})

        bundle_paths = [name for name in names if is_js_bundle(name)]
        bundle_findings: list[dict[str, Any]] = []
        for bundle_path in bundle_paths[:10]:
            info = zf.getinfo(bundle_path)
            if info.file_size > 50 * 1024 * 1024:
                if Path(bundle_path).name not in {"index.android.bundle", "index.android.bundle.hbc"}:
                    continue
            bundle_findings.append(inspect_bundle(zf.read(bundle_path)))

        return {
            "label": label,
            "abis": abis,
            "apk_entries": [label],
            "js_bundle_paths": bundle_paths,
            "rn_libraries": rn_libraries,
            "native_markers": native_markers,
            "bundle_findings": bundle_findings,
        }


def merge_findings(findings: list[dict[str, Any]]) -> dict[str, Any]:
    abis = sorted({abi for item in findings for abi in item["abis"]})
    apk_entries = [entry for item in findings for entry in item["apk_entries"]]
    bundle_paths = sorted({path for item in findings for path in item["js_bundle_paths"]})
    rn_libraries = sorted({lib for item in findings for lib in item["rn_libraries"]})
    native_markers = sorted({marker for item in findings for marker in item["native_markers"]})
    bundle_findings = [finding for item in findings for finding in item["bundle_findings"]]

    renderer = next((str(item.get("renderer", "")) for item in bundle_findings if item.get("renderer")), "")
    hbc_version = next((str(item.get("hbc_version", "")) for item in bundle_findings if item.get("hbc_version")), "")
    rn_guess = "unknown"
    confidence = "low"
    evidence = []
    if bundle_findings:
        best = next((item for item in bundle_findings if item.get("rn_guess") != "unknown"), bundle_findings[0])
        rn_guess = str(best.get("rn_guess", "unknown"))
        confidence = str(best.get("confidence", "low"))
        evidence.append(str(best.get("reason", "JS bundle markers found.")))
    if rn_libraries:
        evidence.append("Android native/package metadata lists React Native-related libraries: " + ", ".join(rn_libraries[:12]))
    if native_markers:
        evidence.append("Android native/package metadata contains markers: " + ", ".join(native_markers[:12]))
    if not evidence:
        confidence = "unknown"
        evidence.append("No React Native JS bundle or native library markers found.")

    return {
        "supported_abis": ";".join(abis),
        "apk_entries": ";".join(apk_entries),
        "js_bundle_paths": ";".join(bundle_paths),
        "hermes_markers": ";".join(marker for marker in native_markers if marker.lower() == "hermes"),
        "react_native_libraries": ";".join(rn_libraries),
        "native_symbol_markers": ";".join(native_markers),
        "react_renderer": renderer,
        "hbc_version": hbc_version,
        "rn_guess": rn_guess,
        "confidence": confidence,
        "evidence_notes": " ".join(evidence),
    }


def analyze_package(path: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    suffix = path.suffix.lower()
    if suffix == ".apk":
        findings.append(inspect_apk_bytes(path.read_bytes(), path.name))
    else:
        with zipfile.ZipFile(path) as outer:
            if "classes.dex" in outer.namelist() or "AndroidManifest.xml" in outer.namelist():
                findings.append(inspect_apk_bytes(path.read_bytes(), path.name))
                merged = merge_findings(findings)
                merged["manifest_metadata"] = ""
                return merged
            manifest_metadata = ""
            if "manifest.json" in outer.namelist():
                manifest_metadata = outer.read("manifest.json").decode("utf-8", "replace")
            for name in outer.namelist():
                if name.endswith(".apk"):
                    findings.append(inspect_apk_bytes(outer.read(name), name))
        merged = merge_findings(findings)
        merged["manifest_metadata"] = manifest_metadata[:2000]
        return merged
    merged = merge_findings(findings)
    merged["manifest_metadata"] = ""
    return merged


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ANDROID_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download/analyze Android APK/APKS/XAPK packages for RN evidence.")
    parser.add_argument("--app-slug", required=True)
    parser.add_argument("--app-name", default="")
    parser.add_argument("--android-package", required=True)
    parser.add_argument("--version-list-json", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--version-code", action="append", default=[])
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--analyze-only", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    entries = load_catalog(args.version_list_json)
    if args.version_code:
        wanted = set(args.version_code)
        entries = [entry for entry in entries if str(entry.get("version_code", "")) in wanted]
    entries = sorted(entries, key=catalog_sort_key, reverse=True)
    if args.limit:
        entries = entries[: args.limit]

    by_code = {str(entry.get("version_code", "")): entry for entry in entries}
    packages: dict[str, Path] = {}
    if not args.analyze_only:
        args.download_dir.mkdir(parents=True, exist_ok=True)
        for entry in entries:
            path = download_package(
                entry,
                app_slug=args.app_slug,
                download_dir=args.download_dir,
                force=args.force,
                timeout=args.timeout,
            )
            packages[str(entry.get("version_code", ""))] = path

    for path in sorted(args.download_dir.glob(f"{args.app_slug}_*.*")):
        match = re.search(r"_(\d+)_", path.name)
        if match and match.group(1) in by_code:
            packages.setdefault(match.group(1), path)

    rows: list[dict[str, Any]] = []
    for version_code, path in sorted(packages.items(), key=lambda item: catalog_sort_key(by_code[item[0]])):
        entry = by_code[version_code]
        print(f"analyzing {path}")
        analysis = analyze_package(path)
        row = {
            "android_package": args.android_package,
            "version_name": str(entry.get("version_name", "")),
            "version_code": version_code,
            "source": str(entry.get("source", "")),
            "source_publish_date": str(entry.get("source_publish_date", "")),
            "source_publish_date_raw": str(entry.get("source_publish_date_raw", "")),
            "download_url": str(entry.get("download_url", "")),
            "package": str(path),
            "package_file_type": path.suffix.lower().lstrip(".").upper(),
            "package_size": str(path.stat().st_size),
            "package_sha256": file_sha256(path),
            "split_metadata": str(entry.get("split_metadata", "")),
            **analysis,
        }
        rows.append({field: row.get(field, "") for field in ANDROID_FIELDS})

    if not rows:
        raise RuntimeError("no Android packages analyzed")
    write_csv(args.report.with_suffix(".csv"), rows)
    write_json(args.report.with_suffix(".json"), rows)
    for row in rows:
        print(
            f"{row['version_name']} ({row['version_code']}): RN {row['rn_guess']} "
            f"[{row['confidence']}], libs {row['react_native_libraries'] or 'none'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
