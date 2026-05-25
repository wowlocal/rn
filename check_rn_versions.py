#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DISCORD_APP_ID = 985746746
DISCORD_BUNDLE_ID = "com.hammerandchisel.discord"


@dataclass(frozen=True)
class VersionEntry:
    external_version_id: str
    version: str = ""
    build: str = ""
    date: str = ""


def run_cmd(
    argv: list[str],
    *,
    retries: int = 0,
    retry_delay: float = 5.0,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    last: subprocess.CompletedProcess[str] | None = None
    for attempt in range(retries + 1):
        last = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if last.returncode == 0:
            return last
        if attempt < retries:
            print(
                f"retrying after failure ({attempt + 1}/{retries}): {' '.join(argv)}",
                file=sys.stderr,
            )
            if last.stderr:
                print(last.stderr.strip(), file=sys.stderr)
            time.sleep(retry_delay)
    assert last is not None
    if check:
        raise RuntimeError(
            f"command failed ({last.returncode}): {' '.join(argv)}\n"
            f"stdout:\n{last.stdout}\n"
            f"stderr:\n{last.stderr}"
        )
    return last


def load_json_text(text: str) -> Any:
    text = text.strip()
    if not text:
        raise ValueError("empty JSON output")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        starts = [i for i in (text.find("{"), text.find("[")) if i >= 0]
        if not starts:
            raise
        return json.loads(text[min(starts) :])


def first_present(data: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = data.get(key)
        if value is not None and str(value):
            return str(value)
    return ""


def find_version_entries(data: Any) -> list[VersionEntry]:
    id_keys = (
        "externalVersionIdentifier",
        "externalVersionId",
        "externalVersionID",
        "external_version_identifier",
        "external_version_id",
        "softwareVersionExternalIdentifier",
    )
    version_keys = (
        "version",
        "bundleShortVersionString",
        "shortVersionString",
        "displayVersion",
        "versionString",
    )
    build_keys = ("build", "bundleVersion", "buildVersion", "versionCode")
    date_keys = ("date", "releaseDate", "created", "timestamp")
    list_keys = (
        "softwareVersionExternalIdentifiers",
        "externalVersionIdentifiers",
        "external_version_identifiers",
    )

    entries: list[VersionEntry] = []
    seen: set[str] = set()

    def add(entry: VersionEntry) -> None:
        if entry.external_version_id and entry.external_version_id not in seen:
            seen.add(entry.external_version_id)
            entries.append(entry)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key in list_keys:
                identifiers = value.get(key)
                if isinstance(identifiers, list):
                    for identifier in identifiers:
                        if isinstance(identifier, (int, str)) and str(identifier).isdigit():
                            add(VersionEntry(external_version_id=str(identifier)))
            external_id = first_present(value, id_keys)
            if external_id:
                add(
                    VersionEntry(
                        external_version_id=external_id,
                        version=first_present(value, version_keys),
                        build=first_present(value, build_keys),
                        date=first_present(value, date_keys),
                    )
                )
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                if isinstance(child, (int, str)) and str(child).isdigit():
                    add(VersionEntry(external_version_id=str(child)))
                else:
                    walk(child)

    walk(data)
    return entries


def list_versions(args: argparse.Namespace) -> list[VersionEntry]:
    if args.versions_json:
        data = load_json_text(Path(args.versions_json).read_text())
    else:
        target_args = ipatool_target_args(args, "list-versions")
        argv = [
            args.ipatool,
            "list-versions",
            *target_args,
            "--format",
            "json",
        ]
        result = run_cmd(argv, retries=args.retries, retry_delay=args.retry_delay)
        data = load_json_text(result.stdout)
        args.version_list_out.parent.mkdir(parents=True, exist_ok=True)
        args.version_list_out.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n"
        )

    entries = find_version_entries(data)
    if not entries:
        raise RuntimeError("could not find external version identifiers in ipatool output")
    return entries


def version_entries_from_ipa_metadata(paths: list[Path]) -> list[VersionEntry]:
    entries: list[VersionEntry] = []
    seen: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        with zipfile.ZipFile(path) as zf:
            if "iTunesMetadata.plist" not in zf.namelist():
                continue
            data = plistlib.loads(zf.read("iTunesMetadata.plist"))
        for entry in find_version_entries(data):
            if entry.external_version_id not in seen:
                seen.add(entry.external_version_id)
                entries.append(entry)
    return entries


def newest_first(entries: list[VersionEntry]) -> list[VersionEntry]:
    if not entries:
        return []
    if all(entry.external_version_id.isdigit() for entry in entries):
        return sorted(entries, key=lambda entry: int(entry.external_version_id), reverse=True)
    return entries


def sanitize(value: str) -> str:
    value = value.strip() or "unknown"
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value.strip("_") or "unknown"


def ipatool_target_args(args: argparse.Namespace, command: str) -> list[str]:
    if args.use_bundle_identifier:
        if not args.bundle_id:
            raise RuntimeError(f"--bundle-id is required when calling ipatool {command} by bundle identifier")
        return ["--bundle-identifier", args.bundle_id]
    if args.app_id is None:
        raise RuntimeError(f"--app-id is required when calling ipatool {command}")
    return ["--app-id", str(args.app_id)]


def download_ipa(args: argparse.Namespace, entry: VersionEntry, index: int) -> Path:
    label = sanitize(entry.version or entry.build or entry.external_version_id)
    out = args.download_dir / f"{args.app_slug}_{index:03d}_{label}_{entry.external_version_id}.ipa"
    if out.exists() and not args.force:
        print(f"already exists: {out}")
        return out

    target_args = ipatool_target_args(args, "download")
    argv = [
        args.ipatool,
        "download",
        *target_args,
        "--external-version-id",
        entry.external_version_id,
        "--output",
        str(out),
        "--format",
        "json",
    ]
    if args.purchase:
        argv.insert(-2, "--purchase")
    print(f"downloading {entry.external_version_id} -> {out}")
    run_cmd(argv, retries=args.retries, retry_delay=args.retry_delay)
    return out


def zip_member_for_app(zf: zipfile.ZipFile, suffix: str) -> str:
    candidates = [
        name
        for name in zf.namelist()
        if name.startswith("Payload/") and name.endswith(suffix) and ".app/" in name
    ]
    if not candidates:
        return ""
    return sorted(candidates, key=lambda item: (len(item), item))[0]


def extract_info_plist(zf: zipfile.ZipFile) -> dict[str, Any]:
    member = zip_member_for_app(zf, "/Info.plist")
    if not member:
        return {}
    return plistlib.loads(zf.read(member))


def zip_timestamp(zf: zipfile.ZipFile, member: str) -> str:
    if not member:
        return ""
    try:
        date_time = zf.getinfo(member).date_time
    except KeyError:
        return ""
    return (
        f"{date_time[0]:04d}-{date_time[1]:02d}-{date_time[2]:02d}"
        f"T{date_time[3]:02d}:{date_time[4]:02d}:{date_time[5]:02d}"
    )


def external_version_id(path: Path, zf: zipfile.ZipFile) -> str:
    if "iTunesMetadata.plist" in zf.namelist():
        data = plistlib.loads(zf.read("iTunesMetadata.plist"))
        value = data.get("softwareVersionExternalIdentifier")
        if value is not None and str(value).isdigit():
            return str(value)
    match = re.search(r"_([0-9]+)\.ipa$", path.name)
    return match.group(1) if match else ""


def main_bundle_member(zf: zipfile.ZipFile) -> str:
    names = zf.namelist()
    preferred = [
        name
        for name in names
        if name.startswith("Payload/")
        and ".app/" in name
        and name.endswith("/main.jsbundle")
    ]
    if preferred:
        return sorted(preferred, key=lambda item: (len(item), item))[0]
    candidates = [
        name
        for name in names
        if name.startswith("Payload/")
        and ".app/" in name
        and (name.endswith(".jsbundle") or name.endswith(".hbc") or name.endswith(".bundle"))
    ]
    return sorted(candidates, key=lambda item: (len(item), item))[0] if candidates else ""


def executable_member(zf: zipfile.ZipFile, info: dict[str, Any]) -> str:
    executable = info.get("CFBundleExecutable")
    if not executable:
        return ""
    suffix = f".app/{executable}"
    candidates = [
        name for name in zf.namelist() if name.startswith("Payload/") and name.endswith(suffix)
    ]
    return sorted(candidates, key=lambda item: (len(item), item))[0] if candidates else ""


def file_description(path: Path) -> str:
    if not shutil.which("file"):
        return ""
    result = run_cmd(["file", str(path)], check=False)
    return result.stdout.strip()


def executable_cryptid(path: Path) -> str:
    if not shutil.which("otool"):
        return ""
    result = run_cmd(["otool", "-l", str(path)], check=False)
    if result.returncode != 0:
        return ""
    match = re.search(r"LC_ENCRYPTION_INFO_64.*?cryptid\s+(\d+)", result.stdout, re.S)
    if not match:
        match = re.search(r"LC_ENCRYPTION_INFO.*?cryptid\s+(\d+)", result.stdout, re.S)
    return match.group(1) if match else ""


def bytes_text_match(data: bytes, pattern: bytes) -> str:
    match = re.search(pattern, data)
    if not match:
        return ""
    return match.group(1).decode("ascii", errors="replace")


def infer_react_native(
    renderer: str,
    has_virtual_view_mode_export: bool,
    has_react_native_version_export: bool,
    has_unstable_enable_logbox_export: bool,
    has_experimental_layout_conformance_export: bool,
    has_register_callable_module_export: bool,
    has_dev_menu_export: bool,
    has_set_up_dom: bool,
    has_use_animated_value_export: bool,
    has_segmented_control_ios_export: bool,
    has_date_picker_android_export: bool,
    has_picker_ios_export: bool,
    has_status_bar_ios_export: bool,
    has_root_tag_context_export: bool,
    has_unstable_root_tag_context_export: bool,
    has_platform_color_export: bool,
    has_dynamic_color_ios_export: bool,
    has_pressable_export: bool,
    has_color_android_export: bool,
    has_check_box_export: bool,
    has_tv_event_handler_export: bool,
    has_use_window_dimensions_export: bool,
    has_native_dialog_manager_android_export: bool,
    has_turbo_module_registry_export: bool,
    has_virtualized_section_list_export: bool,
    has_app_registry_marker: bool,
    has_batched_bridge_marker: bool,
    has_native_modules_marker: bool,
    has_style_sheet_marker: bool,
) -> tuple[str, str, str]:
    if renderer == "19.2.0":
        return "0.83.x", "medium", "React renderer 19.2.0 is used by the RN 0.83 line."
    if renderer == "19.1.1":
        return "0.82.x", "medium", "React renderer 19.1.1 is used by the RN 0.82 line."
    if renderer == "19.1.0":
        if has_virtual_view_mode_export and not has_react_native_version_export:
            return (
                "0.81.x",
                "high",
                "RN index marker has VirtualViewMode, but not the ReactNativeVersion export added in 0.82.",
            )
        if has_react_native_version_export:
            return "0.82.x or newer", "low", "ReactNativeVersion export is present, but renderer is 19.1.0."
        return "0.80.x or 0.81.x", "low", "Renderer is 19.1.0, but 0.81 index marker was not found."
    if renderer == "19.0.0":
        if has_unstable_enable_logbox_export:
            return (
                "0.78.x",
                "high",
                "Renderer is 19.0.0 and RN index marker unstable_enableLogBox is present; RN 0.79 removes it.",
            )
        return (
            "0.79.x",
            "medium",
            "Renderer is 19.0.0 and RN index marker unstable_enableLogBox is absent.",
        )
    if not renderer and has_unstable_enable_logbox_export:
        if not has_experimental_layout_conformance_export:
            if has_dev_menu_export:
                return (
                    "0.77.x",
                    "medium",
                    "RN index marker unstable_enableLogBox is present, DevMenu export is present, and 0.78's experimental_LayoutConformance marker is absent.",
                )
            if has_register_callable_module_export:
                return (
                    "0.74.x-0.76.x",
                    "medium",
                    "RN index marker registerCallableModule is present, but the 0.77 DevMenu and 0.78 experimental_LayoutConformance markers are absent.",
                )
            if has_set_up_dom:
                return (
                    "0.72.x-0.73.x",
                    "medium",
                    "RN setup marker setUpDOM is present, but the 0.74 registerCallableModule marker is absent.",
                )
            if has_use_animated_value_export:
                return (
                    "0.71.x",
                    "medium",
                    "RN index marker useAnimatedValue is present; setUpDOM from 0.72 is absent.",
                )
            if not has_segmented_control_ios_export:
                return (
                    "0.69.x-0.70.x",
                    "medium",
                    "RN index marker SegmentedControlIOS, removed in 0.69, is absent; useAnimatedValue from 0.71 is absent.",
                )
            if not has_date_picker_android_export:
                return (
                    "0.67.x-0.68.x",
                    "medium",
                    "RN index marker DatePickerAndroid, removed in 0.67, is absent; SegmentedControlIOS is still present.",
                )
            if not has_picker_ios_export and not has_status_bar_ios_export:
                return (
                    "0.66.x",
                    "medium",
                    "RN index markers PickerIOS and StatusBarIOS, removed in 0.66, are absent; DatePickerAndroid is still present.",
                )
            if has_root_tag_context_export and not has_unstable_root_tag_context_export:
                return (
                    "0.65.x",
                    "medium",
                    "RN index marker RootTagContext is present and the older unstable_RootTagContext name is absent.",
                )
            if has_platform_color_export or has_dynamic_color_ios_export or has_pressable_export:
                if has_color_android_export or has_check_box_export or has_tv_event_handler_export:
                    return (
                        "0.63.x",
                        "medium",
                        "RN 0.63 color/Pressable markers are present and legacy CheckBox/TVEventHandler markers are still present.",
                    )
                return (
                    "0.64.x",
                    "medium",
                    "RN 0.63 color/Pressable markers are present and legacy CheckBox/TVEventHandler markers removed in 0.64 are absent.",
                )
            if has_unstable_root_tag_context_export and has_use_window_dimensions_export:
                return (
                    "0.62.x",
                    "medium",
                    "RN LogBox marker is present, but PlatformColor/Pressable from 0.63 are absent.",
                )
            if has_unstable_root_tag_context_export:
                return (
                    "<=0.64.x",
                    "medium",
                    "RN index marker unstable_RootTagContext is present.",
                )
            return (
                "<=0.71.x",
                "medium",
                "RN index marker unstable_enableLogBox is present, but newer JS-side markers from RN 0.72+ are absent.",
            )
    if not renderer:
        if has_unstable_root_tag_context_export and has_use_window_dimensions_export:
            return (
                "0.61.x",
                "medium",
                "RN 0.61 markers unstable_RootTagContext/useWindowDimensions are present and LogBox from 0.62 is absent.",
            )
        if has_turbo_module_registry_export or has_virtualized_section_list_export:
            return (
                "0.60.x",
                "medium",
                "RN 0.60 markers TurboModuleRegistry/VirtualizedSectionList are present and 0.61 markers are absent.",
            )
        if has_app_registry_marker and has_batched_bridge_marker and (has_native_modules_marker or has_style_sheet_marker):
            return (
                "<=0.59.x",
                "medium",
                "Core React Native bundle markers are present, but RN 0.60+ index markers are absent.",
            )
    if renderer:
        return (
            f"unknown (react-native-renderer {renderer})",
            "low",
            "No local signature rule matched this renderer version.",
        )
    return "unknown", "low", "No react-native-renderer marker was found."


def analyze_ipa(path: Path) -> dict[str, str]:
    row: dict[str, str] = {
        "ipa": str(path),
        "external_version_id": "",
        "bundle_id": "",
        "app_version": "",
        "app_build": "",
        "build_timestamp": "",
        "release_channel": "",
        "sentry_release": "",
        "bundle_member": "",
        "hbc_version": "",
        "react_renderer": "",
        "rn_guess": "unknown",
        "confidence": "low",
        "has_virtual_view_mode_export": "false",
        "has_react_native_version_export": "false",
        "has_unstable_enable_logbox_export": "false",
        "has_experimental_layout_conformance_export": "false",
        "has_register_callable_module_export": "false",
        "has_dev_menu_export": "false",
        "has_set_up_dom": "false",
        "has_use_animated_value_export": "false",
        "has_segmented_control_ios_export": "false",
        "has_date_picker_android_export": "false",
        "has_picker_ios_export": "false",
        "has_status_bar_ios_export": "false",
        "has_root_tag_context_export": "false",
        "has_unstable_root_tag_context_export": "false",
        "has_platform_color_export": "false",
        "has_dynamic_color_ios_export": "false",
        "has_pressable_export": "false",
        "has_color_android_export": "false",
        "has_check_box_export": "false",
        "has_tv_event_handler_export": "false",
        "has_use_window_dimensions_export": "false",
        "has_native_dialog_manager_android_export": "false",
        "has_turbo_module_registry_export": "false",
        "has_virtualized_section_list_export": "false",
        "has_app_registry_marker": "false",
        "has_batched_bridge_marker": "false",
        "has_native_modules_marker": "false",
        "has_style_sheet_marker": "false",
        "cryptid": "",
        "notes": "",
    }

    notes: list[str] = []
    with tempfile.TemporaryDirectory(prefix="rn-ipa-") as tmp_name:
        tmp = Path(tmp_name)
        with zipfile.ZipFile(path) as zf:
            row["external_version_id"] = external_version_id(path, zf)
            info_member = zip_member_for_app(zf, "/Info.plist")
            row["build_timestamp"] = zip_timestamp(zf, info_member)
            info = extract_info_plist(zf)
            row["bundle_id"] = str(info.get("CFBundleIdentifier", ""))
            row["app_version"] = str(info.get("CFBundleShortVersionString", ""))
            row["app_build"] = str(info.get("CFBundleVersion", ""))
            row["release_channel"] = str(info.get("RELEASE_CHANNEL", ""))
            row["sentry_release"] = str(info.get("SENTRY_RELEASE", ""))

            bundle_member = main_bundle_member(zf)
            row["bundle_member"] = bundle_member
            if bundle_member:
                bundle_data = zf.read(bundle_member)
                bundle_path = tmp / "main.jsbundle"
                bundle_path.write_bytes(bundle_data)
                desc = file_description(bundle_path)
                hbc_match = re.search(r"Hermes JavaScript bytecode, version (\d+)", desc)
                if hbc_match:
                    row["hbc_version"] = hbc_match.group(1)

                row["react_renderer"] = bytes_text_match(
                    bundle_data,
                    rb"react-native-renderer:?\s*([0-9]+\.[0-9]+\.[0-9]+)",
                )
                has_virtual = b"get VirtualViewMode" in bundle_data
                has_rnv_export = b"get ReactNativeVersion" in bundle_data
                has_logbox = b"unstable_enableLogBox" in bundle_data
                has_layout_conformance = b"experimental_LayoutConformance" in bundle_data
                has_register_callable = b"get registerCallableModule" in bundle_data
                has_dev_menu = b"get DevMenu" in bundle_data
                has_set_up_dom = b"setUpDOM" in bundle_data
                has_use_animated_value = b"get useAnimatedValue" in bundle_data
                has_segmented_control_ios = b"get SegmentedControlIOS" in bundle_data
                has_date_picker_android = b"get DatePickerAndroid" in bundle_data
                has_picker_ios = b"get PickerIOS" in bundle_data
                has_status_bar_ios = b"get StatusBarIOS" in bundle_data
                has_root_tag_context = b"get RootTagContext" in bundle_data
                has_unstable_root_tag_context = b"get unstable_RootTagContext" in bundle_data
                has_platform_color = b"get PlatformColor" in bundle_data
                has_dynamic_color_ios = b"get DynamicColorIOS" in bundle_data
                has_pressable = b"get Pressable" in bundle_data
                has_color_android = b"get ColorAndroid" in bundle_data
                has_check_box = b"get CheckBox" in bundle_data
                has_tv_event_handler = b"get TVEventHandler" in bundle_data
                has_use_window_dimensions = b"get useWindowDimensions" in bundle_data
                has_native_dialog_manager_android = b"get NativeDialogManagerAndroid" in bundle_data
                has_turbo_module_registry = b"get TurboModuleRegistry" in bundle_data
                has_virtualized_section_list = b"get VirtualizedSectionList" in bundle_data
                has_app_registry = b"AppRegistry" in bundle_data
                has_batched_bridge = b"BatchedBridge" in bundle_data
                has_native_modules = b"NativeModules" in bundle_data
                has_style_sheet = b"StyleSheet" in bundle_data
                row["has_virtual_view_mode_export"] = str(has_virtual).lower()
                row["has_react_native_version_export"] = str(has_rnv_export).lower()
                row["has_unstable_enable_logbox_export"] = str(has_logbox).lower()
                row["has_experimental_layout_conformance_export"] = str(has_layout_conformance).lower()
                row["has_register_callable_module_export"] = str(has_register_callable).lower()
                row["has_dev_menu_export"] = str(has_dev_menu).lower()
                row["has_set_up_dom"] = str(has_set_up_dom).lower()
                row["has_use_animated_value_export"] = str(has_use_animated_value).lower()
                row["has_segmented_control_ios_export"] = str(has_segmented_control_ios).lower()
                row["has_date_picker_android_export"] = str(has_date_picker_android).lower()
                row["has_picker_ios_export"] = str(has_picker_ios).lower()
                row["has_status_bar_ios_export"] = str(has_status_bar_ios).lower()
                row["has_root_tag_context_export"] = str(has_root_tag_context).lower()
                row["has_unstable_root_tag_context_export"] = str(has_unstable_root_tag_context).lower()
                row["has_platform_color_export"] = str(has_platform_color).lower()
                row["has_dynamic_color_ios_export"] = str(has_dynamic_color_ios).lower()
                row["has_pressable_export"] = str(has_pressable).lower()
                row["has_color_android_export"] = str(has_color_android).lower()
                row["has_check_box_export"] = str(has_check_box).lower()
                row["has_tv_event_handler_export"] = str(has_tv_event_handler).lower()
                row["has_use_window_dimensions_export"] = str(has_use_window_dimensions).lower()
                row["has_native_dialog_manager_android_export"] = str(has_native_dialog_manager_android).lower()
                row["has_turbo_module_registry_export"] = str(has_turbo_module_registry).lower()
                row["has_virtualized_section_list_export"] = str(has_virtualized_section_list).lower()
                row["has_app_registry_marker"] = str(has_app_registry).lower()
                row["has_batched_bridge_marker"] = str(has_batched_bridge).lower()
                row["has_native_modules_marker"] = str(has_native_modules).lower()
                row["has_style_sheet_marker"] = str(has_style_sheet).lower()
                guess, confidence, reason = infer_react_native(
                    row["react_renderer"],
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
                row["rn_guess"] = guess
                row["confidence"] = confidence
                notes.append(reason)
            else:
                notes.append("No JS bundle was found in the app bundle.")

            exe_member = executable_member(zf, info)
            if exe_member:
                exe_path = tmp / "app_executable"
                exe_path.write_bytes(zf.read(exe_member))
                row["cryptid"] = executable_cryptid(exe_path)
                if row["cryptid"] == "1":
                    notes.append("Native executable is FairPlay encrypted; exact native RN constants are not inspectable.")
                elif row["cryptid"] == "0":
                    notes.append("Native executable is not encrypted; native constant scanning may be possible.")
            else:
                notes.append("No app executable was found in the IPA.")

    row["notes"] = " ".join(note for note in notes if note)
    return row


def write_reports(rows: list[dict[str, str]], report_base: Path) -> None:
    if not rows:
        return
    report_base.parent.mkdir(parents=True, exist_ok=True)
    json_path = report_base.with_suffix(".json")
    csv_path = report_base.with_suffix(".csv")
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {csv_path}")
    print(f"wrote {json_path}")


def collect_ipas(args: argparse.Namespace, downloaded: list[Path]) -> list[Path]:
    paths: list[Path] = []
    paths.extend(downloaded)
    paths.extend(args.ipa)
    if args.analyze_existing:
        paths.extend(sorted(args.download_dir.glob("*.ipa")))
        for fallback in args.fallback_ipa:
            if fallback.exists():
                paths.append(fallback)

    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen and path.exists():
            seen.add(resolved)
            unique.append(path)
    return unique


def parse_args(
    argv: list[str] | None = None,
    *,
    default_app_id: int | None = None,
    default_bundle_id: str = "",
    default_app_slug: str = "app",
    default_app_name: str = "",
    default_download_dir: Path | None = None,
    default_report: Path | None = None,
    default_version_list_out: Path | None = None,
    default_fallback_ipas: list[Path] | None = None,
    description: str | None = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=description
        or "Download iOS app versions with ipatool and infer React Native versions from the IPAs."
    )
    parser.add_argument("--app-slug", default=default_app_slug)
    parser.add_argument("--app-name", default=default_app_name)
    parser.add_argument("--app-id", type=int, default=default_app_id)
    parser.add_argument("--bundle-id", default=default_bundle_id)
    parser.add_argument(
        "--use-bundle-identifier",
        action="store_true",
        help="Use --bundle-identifier instead of --app-id for ipatool list/download.",
    )
    parser.add_argument("--ipatool", default=shutil.which("ipatool") or "ipatool")
    parser.add_argument("--download-dir", type=Path, default=default_download_dir)
    parser.add_argument("--report", type=Path, default=default_report)
    parser.add_argument("--version-list-out", type=Path, default=default_version_list_out)
    parser.add_argument("--versions-json", type=Path, help="Use saved ipatool list-versions JSON instead of calling ipatool.")
    parser.add_argument(
        "--seed-ipa",
        type=Path,
        action="append",
        default=[],
        help="IPA whose iTunesMetadata.plist contains softwareVersionExternalIdentifiers. Can be repeated.",
    )
    parser.add_argument(
        "--skip-list-versions",
        action="store_true",
        help="Do not call ipatool list-versions; read external IDs from --seed-ipa or fallback IPA paths.",
    )
    parser.add_argument("--version-id", action="append", default=[], help="External version ID to download. Can be repeated.")
    parser.add_argument("--limit", type=int, default=5, help="How many historical versions to download when listing versions.")
    parser.add_argument("--offset", type=int, default=0, help="Skip this many older versions after the latest version is skipped.")
    parser.add_argument("--include-latest", action="store_true", help="Do not skip the first version returned by ipatool.")
    parser.add_argument("--print-version-ids", action="store_true", help="Print external version IDs from --versions-json, --seed-ipa, or fallback IPA paths and exit.")
    parser.add_argument("--list-versions-only", action="store_true", help="Save ipatool list-versions output and exit without downloading.")
    parser.add_argument("--purchase", action="store_true", help="Pass --purchase to ipatool download.")
    parser.add_argument("--force", action="store_true", help="Redownload IPAs that already exist.")
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-delay", type=float, default=5.0)
    parser.add_argument("--download-only", action="store_true")
    parser.add_argument("--analyze-only", action="store_true", help="Do not call ipatool; only analyze provided/existing IPAs.")
    parser.add_argument("--analyze-existing", action="store_true", default=True, help="Analyze IPAs in the download dir and fallback IPA paths.")
    parser.add_argument("--no-analyze-existing", dest="analyze_existing", action="store_false")
    parser.add_argument("--ipa", type=Path, action="append", default=[], help="Extra IPA to analyze. Can be repeated.")
    parser.add_argument(
        "--fallback-ipa",
        type=Path,
        action="append",
        default=list(default_fallback_ipas or []),
        help="Extra local IPA included by --analyze-existing and seed metadata fallback. Can be repeated.",
    )
    args = parser.parse_args(argv)
    if args.download_dir is None:
        args.download_dir = Path("ipas") / args.app_slug
    if args.report is None:
        args.report = Path("reports") / args.app_slug / "versions"
    if args.version_list_out is None:
        args.version_list_out = Path("reports") / args.app_slug / "version-list.json"
    return args


def main(
    argv: list[str] | None = None,
    *,
    default_app_id: int | None = None,
    default_bundle_id: str = "",
    default_app_slug: str = "app",
    default_app_name: str = "",
    default_download_dir: Path | None = None,
    default_report: Path | None = None,
    default_version_list_out: Path | None = None,
    default_fallback_ipas: list[Path] | None = None,
    description: str | None = None,
) -> int:
    args = parse_args(
        argv,
        default_app_id=default_app_id,
        default_bundle_id=default_bundle_id,
        default_app_slug=default_app_slug,
        default_app_name=default_app_name,
        default_download_dir=default_download_dir,
        default_report=default_report,
        default_version_list_out=default_version_list_out,
        default_fallback_ipas=default_fallback_ipas,
        description=description,
    )
    args.download_dir.mkdir(parents=True, exist_ok=True)

    entries: list[VersionEntry] = []
    downloaded: list[Path] = []
    attempted_downloads = 0
    failed_downloads = 0
    if args.list_versions_only:
        entries = list_versions(args)
        print(f"saved {len(entries)} external version IDs to {args.version_list_out}")
        return 0

    if args.print_version_ids:
        if args.version_id:
            entries = [VersionEntry(external_version_id=value) for value in args.version_id]
        elif args.versions_json:
            entries = list_versions(args)
        else:
            seed_ipas = args.seed_ipa or args.fallback_ipa
            entries = version_entries_from_ipa_metadata(seed_ipas)
        entries = newest_first(entries)
        if not args.include_latest:
            entries = entries[1:]
        if args.offset:
            entries = entries[args.offset :]
        if args.limit:
            entries = entries[: args.limit]
        for index, entry in enumerate(entries, start=1):
            details = [entry.external_version_id]
            if entry.version:
                details.append(entry.version)
            if entry.build:
                details.append(entry.build)
            if entry.date:
                details.append(entry.date)
            print("\t".join(details))
        return 0

    if not args.analyze_only:
        if args.version_id:
            entries = [VersionEntry(external_version_id=value) for value in args.version_id]
        else:
            if not args.skip_list_versions:
                try:
                    entries = list_versions(args)
                except Exception as exc:
                    print(f"could not list historical versions with ipatool: {exc}", file=sys.stderr)
            if not entries:
                seed_ipas = args.seed_ipa or args.fallback_ipa
                entries = version_entries_from_ipa_metadata(seed_ipas)
                if entries:
                    print(
                        f"using {len(entries)} external version IDs from iTunesMetadata.plist",
                        file=sys.stderr,
                    )
                else:
                    print(
                        "Pass one or more known external version IDs with --version-id, "
                        "or pass saved list-versions JSON with --versions-json.",
                        file=sys.stderr,
                    )
            entries = newest_first(entries)
            if not args.include_latest:
                entries = entries[1:]
            if args.offset:
                entries = entries[args.offset :]
            entries = entries[: args.limit]
        for index, entry in enumerate(entries, start=1):
            attempted_downloads += 1
            try:
                downloaded.append(download_ipa(args, entry, index))
            except Exception as exc:
                failed_downloads += 1
                print(f"download failed for {entry.external_version_id}: {exc}", file=sys.stderr)

    if args.download_only:
        if attempted_downloads and not downloaded:
            return 1
        return 0

    ipas = collect_ipas(args, downloaded)
    if not ipas:
        print("no IPA files to analyze", file=sys.stderr)
        return 1

    rows: list[dict[str, str]] = []
    for ipa in ipas:
        print(f"analyzing {ipa}")
        try:
            rows.append(analyze_ipa(ipa))
        except Exception as exc:
            rows.append(
                {
                    "ipa": str(ipa),
                    "external_version_id": "",
                    "bundle_id": "",
                    "app_version": "",
                    "app_build": "",
                    "build_timestamp": "",
                    "release_channel": "",
                    "sentry_release": "",
                    "bundle_member": "",
                    "hbc_version": "",
                    "react_renderer": "",
                    "rn_guess": "error",
                    "confidence": "low",
                    "has_virtual_view_mode_export": "false",
                    "has_react_native_version_export": "false",
                    "has_unstable_enable_logbox_export": "false",
                    "has_experimental_layout_conformance_export": "false",
                    "has_register_callable_module_export": "false",
                    "has_dev_menu_export": "false",
                    "has_set_up_dom": "false",
                    "has_use_animated_value_export": "false",
                    "has_segmented_control_ios_export": "false",
                    "has_date_picker_android_export": "false",
                    "has_picker_ios_export": "false",
                    "has_status_bar_ios_export": "false",
                    "has_root_tag_context_export": "false",
                    "has_unstable_root_tag_context_export": "false",
                    "has_platform_color_export": "false",
                    "has_dynamic_color_ios_export": "false",
                    "has_pressable_export": "false",
                    "has_color_android_export": "false",
                    "has_check_box_export": "false",
                    "has_tv_event_handler_export": "false",
                    "has_use_window_dimensions_export": "false",
                    "has_native_dialog_manager_android_export": "false",
                    "has_turbo_module_registry_export": "false",
                    "has_virtualized_section_list_export": "false",
                    "has_app_registry_marker": "false",
                    "has_batched_bridge_marker": "false",
                    "has_native_modules_marker": "false",
                    "has_style_sheet_marker": "false",
                    "cryptid": "",
                    "notes": str(exc),
                }
            )

    write_reports(rows, args.report)
    for row in rows:
        print(
            f"{row['ipa']}: app {row['app_version']} ({row['app_build']}), "
            f"RN {row['rn_guess']} [{row['confidence']}], renderer {row['react_renderer'] or 'unknown'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
