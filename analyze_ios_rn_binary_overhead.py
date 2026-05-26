#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any


RN_JS_RE = re.compile(r"(^|/)(main|index)\.(jsbundle|jsbundle\.zst|hbcbundle|hbc)$|\.jsbundle(\.zst)?$|\.hbcbundle$|\.hbc$", re.I)
RN_NATIVE_NAME_RE = re.compile(
    r"^(React($|[-A-Z_])|ReactCommon|React-Core|React-RCT|ReactNative|ReactNativeDependencies|"
    r"RCT[A-Z_]|Yoga|yoga|Hermes|hermes|JSI|jsi|"
    r"libreact|libReact|libhermes|libjsi|libyoga)"
)
NATIVE_REACT_MARKERS = (
    b"ReactNativeVersion",
    b"ReactNativeFeatureFlags",
    b"ReactCommon",
    b"React-Core",
    b"React-RCT",
    b"facebook::react",
    b"__fbBatchedBridge",
    b"RCTBridge",
    b"RCTBridgeModule",
    b"RCTJavaScriptContext",
    b"RCTRootView",
    b"RCTRootContentView",
    b"RCTCxxBridge",
    b"RCTEventEmitter",
    b"RCTModuleData",
    b"RCTModalHostView",
    b"RCTModalHostViewController",
    b"RCTAppDelegate",
    b"RCTFabricSurface",
    b"RCTSurfacePresenter",
    b"RCTTurboModule",
    b"RCTViewManager",
    b"RCTUIManager",
)
NATIVE_HERMES_MARKERS = (
    b"HermesExecutor",
    b"HermesRuntime",
    b"facebook::hermes",
    b"hermes::",
    b"libhermes",
    b"makeHermesRuntime",
)
NATIVE_JSI_MARKERS = (
    b"facebook::jsi",
    b"jsi::Runtime",
    b"JSIExecutor",
    b"jsi/jsi.h",
)
NATIVE_YOGA_MARKERS = (
    b"YGNode",
    b"YGConfig",
    b"YGBaselineFunc",
    b"YogaKit",
    b"facebook::yoga",
)
NATIVE_RCT_OBJC_SYMBOL = re.compile(rb"_OBJC_(?:CLASS|METACLASS)_\$_RCT[A-Za-z0-9_]+")
EXTENSION_MARKERS = ("/PlugIns/", "/Extensions/", "/Watch/")

FIELDS = [
    "app_slug",
    "app_name",
    "bundle_id",
    "app_version",
    "app_build",
    "build_timestamp",
    "external_version_id",
    "rn_guess",
    "confidence",
    "decrypted_coverage",
    "dump_sha256",
    "dump_size_bytes",
    "source_ipa_size_bytes",
    "main_app_uncompressed_bytes",
    "main_app_compressed_member_bytes",
    "main_app_compressed_pct_uncompressed",
    "total_uncompressed_bytes",
    "total_compressed_member_bytes",
    "macho_total_bytes",
    "main_executable_bytes",
    "main_executable_compressed_bytes",
    "main_executable_pct_main_app",
    "js_bundle_bytes",
    "js_bundle_compressed_bytes",
    "js_bundle_compressed_pct_uncompressed",
    "rn_js_file_count",
    "rn_named_native_bytes",
    "rn_named_native_compressed_bytes",
    "rn_named_native_compressed_pct_uncompressed",
    "rn_named_native_file_count",
    "direct_rn_payload_bytes",
    "direct_rn_payload_compressed_bytes",
    "direct_rn_payload_compressed_pct_uncompressed",
    "direct_rn_payload_pct_main_app",
    "direct_rn_payload_compressed_pct_main_app_compressed",
    "direct_rn_payload_pct_source_ipa",
    "direct_rn_payload_compressed_pct_source_ipa",
    "direct_rn_payload_compressed_pct_dump_ipa",
    "js_bundle_pct_direct_rn_payload",
    "rn_named_native_pct_direct_rn_payload",
    "rn_carrier_macho_bytes",
    "rn_carrier_macho_compressed_bytes",
    "rn_carrier_macho_compressed_pct_dump_ipa",
    "rn_carrier_macho_pct_macho",
    "rn_carrier_macho_pct_main_app",
    "rn_carrier_macho_count",
    "rn_carrier_macho_members",
    "rn_evidence_class",
    "static_linked_rn_likely",
    "remaining_encrypted_appex_count",
    "remaining_encrypted_non_extension_count",
    "rn_js_members",
    "rn_named_native_members",
    "notes",
    "dump_report",
    "dump_ipa",
]

COMPONENT_FIELDS = [
    "app_slug",
    "app_name",
    "bundle_id",
    "app_version",
    "app_build",
    "external_version_id",
    "rn_guess",
    "rn_evidence_class",
    "component",
    "member",
    "bytes",
    "compressed_bytes",
    "compressed_pct_uncompressed",
    "pct_main_app_uncompressed",
    "pct_main_app_compressed",
    "pct_source_ipa",
    "pct_dump_ipa",
    "context_only",
    "dump_report",
    "dump_ipa",
]

DELTA_FIELDS = [
    "app",
    "from_version",
    "to_version",
    "evidence",
    "source_delta",
    "main_app_delta",
    "direct_delta",
    "direct_compressed_delta",
    "js_delta",
    "native_delta",
    "carrier_delta",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def app_entries(apps_path: Path) -> list[dict[str, Any]]:
    data = load_json(apps_path)
    apps = data.get("apps", []) if isinstance(data, dict) else data
    return [app for app in apps if isinstance(app, dict)]


def report_rows(reports_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(reports_dir.glob("*/versions.csv")):
        slug = path.parent.name
        with path.open(newline="") as f:
            for row in csv.DictReader(f):
                row = dict(row)
                row["_app_slug"] = slug
                rows.append(row)
    return rows


def accepted_dump_reports(dumps_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    reports: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(dumps_dir.glob("*.json")):
        try:
            data = load_json(path)
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        if (data.get("verification") or {}).get("accepted_decrypted_evidence") is True:
            output_path = Path(str((data.get("output") or {}).get("path", "")))
            if output_path.exists():
                reports.append((path, data))
    return reports


def source_key(report: dict[str, Any]) -> tuple[str, str, str]:
    source = report.get("source") or {}
    return (
        str(source.get("bundle_id", "")),
        str(source.get("version", "")),
        str(source.get("build", "")),
    )


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("bundle_id", ""),
        row.get("app_version", ""),
        row.get("app_build", ""),
    )


def is_true(value: Any) -> bool:
    return str(value).lower() == "true"


def classify_rn(row: dict[str, str] | None) -> tuple[str, bool, str]:
    if not row:
        return "unknown_report_gap", False, "No matching versions.csv row was found for this accepted dump."
    rn_guess = row.get("rn_guess", "")
    native = is_true(row.get("has_native_react_native_marker"))
    hermes = is_true(row.get("has_native_hermes_marker"))
    jsi = is_true(row.get("has_native_jsi_marker"))
    yoga = is_true(row.get("has_native_yoga_marker"))
    js_markers = any(
        is_true(row.get(field))
        for field in (
            "has_app_registry_marker",
            "has_batched_bridge_marker",
            "has_native_modules_marker",
            "has_style_sheet_marker",
            "has_react_native_version_export",
        )
    )
    if rn_guess and rn_guess != "unknown":
        return "versioned_rn", native or hermes or jsi or yoga, ""
    if native:
        return "native_rn_marker_without_version", True, row.get("unknown_reason", "")
    if js_markers:
        return "generic_js_rn_markers", False, row.get("unknown_reason", "")
    return "no_rn_detected", False, row.get("unknown_reason", "")


def dump_command_path(row: dict[str, str]) -> str:
    command = row.get("dump_command", "")
    match = re.search(r" -o ([^ ]+\.ipa)", command)
    return match.group(1) if match else ""


def choose_reports(
    dump_reports: list[tuple[Path, dict[str, Any]]],
    rows: list[dict[str, str]],
) -> list[tuple[Path, dict[str, Any], dict[str, str] | None]]:
    rows_by_sha = {row.get("decrypted_dump_sha256", ""): row for row in rows if row.get("decrypted_dump_sha256")}
    rows_by_key: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        rows_by_key[row_key(row)].append(row)

    selected: dict[tuple[str, str, str], tuple[Path, dict[str, Any], dict[str, str] | None]] = {}

    for path, report in dump_reports:
        output = report.get("output") or {}
        sha = str(output.get("sha256", ""))
        if sha in rows_by_sha:
            row = rows_by_sha[sha]
            selected[(sha, "", "")] = (path, report, row)

    covered_source_keys = {source_key(report) for _, report, _ in selected.values()}

    def score(item: tuple[Path, dict[str, Any]]) -> tuple[int, int, int, str]:
        path, report = item
        dumper = report.get("dumper") or {}
        output = report.get("output") or {}
        coverage = (report.get("verification") or {}).get("decrypted_coverage") or {}
        return (
            1 if dumper.get("all_binaries") else 0,
            1 if coverage.get("coverage_class") else 0,
            int(output.get("size") or 0),
            str(path),
        )

    by_source: dict[tuple[str, str, str], list[tuple[Path, dict[str, Any]]]] = defaultdict(list)
    for item in dump_reports:
        by_source[source_key(item[1])].append(item)

    for key, candidates in by_source.items():
        if key in covered_source_keys:
            continue
        path, report = sorted(candidates, key=score, reverse=True)[0]
        rows_for_source = rows_by_key.get(key, [])
        row = rows_for_source[0] if rows_for_source else None
        selected[(str((report.get("output") or {}).get("sha256", "")), key[1], key[2])] = (path, report, row)

    return sorted(
        selected.values(),
        key=lambda item: (
            str(((item[1].get("source") or {}).get("bundle_id", ""))),
            str(((item[1].get("source") or {}).get("version", ""))),
            str(((item[1].get("source") or {}).get("build", ""))),
            str((item[1].get("output") or {}).get("sha256", "")),
        ),
    )


def in_primary_app_scope(member: str) -> bool:
    return not any(marker in member for marker in EXTENSION_MARKERS)


def rn_native_binary_name(member: str) -> str:
    parts = member.split("/")
    basename = parts[-1]
    if basename.endswith(".dylib"):
        stem = basename[:-6]
        return stem if RN_NATIVE_NAME_RE.search(stem) else ""
    for index, part in enumerate(parts):
        if not part.endswith(".framework"):
            continue
        framework_name = part[: -len(".framework")]
        if RN_NATIVE_NAME_RE.search(framework_name):
            if index + 1 < len(parts) and parts[index + 1] == framework_name:
                return framework_name
            return ""
    return ""


def has_rn_carrier_marker(data: bytes, allow_generic_runtime_markers: bool) -> bool:
    if any(marker in data for marker in NATIVE_REACT_MARKERS) or NATIVE_RCT_OBJC_SYMBOL.search(data):
        return True
    if not allow_generic_runtime_markers:
        return False
    runtime_markers = NATIVE_HERMES_MARKERS + NATIVE_JSI_MARKERS + NATIVE_YOGA_MARKERS
    return any(marker in data for marker in runtime_markers)


def member_list(value: list[str]) -> str:
    return ";".join(value[:20])


def inspect_dump(
    report_path: Path,
    report: dict[str, Any],
    row: dict[str, str] | None,
    apps_by_bundle: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source = report.get("source") or {}
    output = report.get("output") or {}
    verification = report.get("verification") or {}
    coverage = verification.get("decrypted_coverage") or {}
    inventory = verification.get("mach_o_cryptid_inventory") or {}
    bundle_id = str(source.get("bundle_id", ""))
    app = apps_by_bundle.get(bundle_id, {})
    dump_ipa = Path(str(output.get("path", "")))

    total_uncompressed = 0
    total_compressed = 0
    main_app_uncompressed = 0
    main_app_compressed = 0
    js_bytes = 0
    js_compressed = 0
    native_bytes = 0
    native_compressed = 0
    main_executable_compressed = 0
    js_members: list[str] = []
    native_members: list[str] = []
    component_members: list[dict[str, Any]] = []

    with zipfile.ZipFile(dump_ipa) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            total_uncompressed += info.file_size
            total_compressed += info.compress_size
            if in_primary_app_scope(info.filename):
                main_app_uncompressed += info.file_size
                main_app_compressed += info.compress_size
            if RN_JS_RE.search(info.filename) and in_primary_app_scope(info.filename):
                js_bytes += info.file_size
                js_compressed += info.compress_size
                js_members.append(info.filename)
                component_members.append(
                    {
                        "component": "js_bundle",
                        "member": info.filename,
                        "bytes": info.file_size,
                        "compressed_bytes": info.compress_size,
                        "context_only": "false",
                    }
                )
            if in_primary_app_scope(info.filename) and rn_native_binary_name(info.filename):
                native_bytes += info.file_size
                native_compressed += info.compress_size
                native_members.append(info.filename)
                component_members.append(
                    {
                        "component": "named_native_runtime",
                        "member": info.filename,
                        "bytes": info.file_size,
                        "compressed_bytes": info.compress_size,
                        "context_only": "false",
                    }
                )

    inventory_entries = inventory.get("entries", []) if isinstance(inventory, dict) else []
    macho_total = sum(int(entry.get("size") or 0) for entry in inventory_entries if isinstance(entry, dict))
    main_executable_bytes = sum(
        int(entry.get("size") or 0)
        for entry in inventory_entries
        if isinstance(entry, dict) and entry.get("category") == "main_executable"
    )
    with zipfile.ZipFile(dump_ipa) as zf:
        for entry in inventory_entries:
            if not isinstance(entry, dict) or entry.get("category") != "main_executable":
                continue
            member = str(entry.get("member", ""))
            if not member:
                continue
            try:
                main_executable_compressed += zf.getinfo(member).compress_size
            except KeyError:
                continue
    if not main_executable_bytes:
        executable = str(source.get("executable", ""))
        payload_app_dir = str(source.get("payload_app_dir", ""))
        main_member = f"{payload_app_dir}/{executable}" if payload_app_dir and executable else ""
        if main_member:
            with zipfile.ZipFile(dump_ipa) as zf:
                try:
                    info = zf.getinfo(main_member)
                    main_executable_bytes = info.file_size
                    main_executable_compressed = info.compress_size
                except KeyError:
                    main_executable_bytes = 0

    rn_evidence_class, static_linked_likely, class_note = classify_rn(row)
    carrier_macho_members: list[str] = []
    carrier_macho_bytes = 0
    carrier_macho_compressed = 0
    if inventory_entries and rn_evidence_class != "no_rn_detected":
        allow_generic_runtime_markers = rn_evidence_class == "versioned_rn"
        with zipfile.ZipFile(dump_ipa) as zf:
            for entry in inventory_entries:
                if not isinstance(entry, dict):
                    continue
                member = str(entry.get("member", ""))
                if not member or not in_primary_app_scope(member):
                    continue
                if entry.get("cryptid") not in (0, "0"):
                    continue
                try:
                    data = zf.read(member)
                    info = zf.getinfo(member)
                except KeyError:
                    continue
                if has_rn_carrier_marker(data, allow_generic_runtime_markers):
                    carrier_macho_members.append(member)
                    size = int(entry.get("size") or len(data))
                    carrier_macho_bytes += size
                    carrier_macho_compressed += info.compress_size
                    component_members.append(
                        {
                            "component": "rn_carrier_macho",
                            "member": member,
                            "bytes": size,
                            "compressed_bytes": info.compress_size,
                            "context_only": "true",
                        }
                    )

    direct_rn_payload = js_bytes + native_bytes
    direct_rn_payload_compressed = js_compressed + native_compressed
    carrier_bytes = carrier_macho_bytes if carrier_macho_bytes else native_bytes
    carrier_compressed = carrier_macho_compressed if carrier_macho_compressed else native_compressed
    source_ipa_size = int(source.get("size") or 0)
    dump_size = int(output.get("size") or 0)
    remaining_appex = coverage.get("remaining_encrypted_appex_members") or []
    remaining_non_extension = coverage.get("remaining_encrypted_non_extension_members") or []

    def pct(numerator: int, denominator: int) -> str:
        if not denominator:
            return ""
        return f"{(numerator / denominator) * 100:.2f}"

    notes: list[str] = []
    if rn_evidence_class == "no_rn_detected":
        notes.append("negative/control row: no React Native evidence in current analyzer output")
    elif not direct_rn_payload and static_linked_likely:
        notes.append("direct RN artifact floor is zero because RN appears statically linked into app-native Mach-O")
    if class_note:
        notes.append(class_note)
    if verification.get("accepted_decrypted_evidence") and not coverage.get("coverage_class"):
        notes.append("accepted dump predates decrypted coverage classification")
    if coverage.get("remaining_encrypted_non_extension_members"):
        notes.append("remaining encrypted non-extension Mach-O may hide additional bytes")

    result = {
        "app_slug": row.get("_app_slug", "") if row else app.get("app_slug", ""),
        "app_name": app.get("app_name", ""),
        "bundle_id": bundle_id,
        "app_version": str(source.get("version", "")),
        "app_build": str(source.get("build", "")),
        "build_timestamp": row.get("build_timestamp", "") if row else "",
        "external_version_id": row.get("external_version_id", "") if row else "",
        "rn_guess": row.get("rn_guess", "") if row else "",
        "confidence": row.get("confidence", "") if row else "",
        "decrypted_coverage": coverage.get("coverage_class", "") or row.get("decrypted_coverage", "") if row else coverage.get("coverage_class", ""),
        "dump_sha256": output.get("sha256", ""),
        "dump_size_bytes": str(output.get("size", "")),
        "source_ipa_size_bytes": str(source.get("size", "")),
        "main_app_uncompressed_bytes": str(main_app_uncompressed),
        "main_app_compressed_member_bytes": str(main_app_compressed),
        "main_app_compressed_pct_uncompressed": pct(main_app_compressed, main_app_uncompressed),
        "total_uncompressed_bytes": str(total_uncompressed),
        "total_compressed_member_bytes": str(total_compressed),
        "macho_total_bytes": str(macho_total) if macho_total else "",
        "main_executable_bytes": str(main_executable_bytes) if main_executable_bytes else "",
        "main_executable_compressed_bytes": str(main_executable_compressed) if main_executable_compressed else "",
        "main_executable_pct_main_app": pct(main_executable_bytes, main_app_uncompressed),
        "js_bundle_bytes": str(js_bytes),
        "js_bundle_compressed_bytes": str(js_compressed),
        "js_bundle_compressed_pct_uncompressed": pct(js_compressed, js_bytes),
        "rn_js_file_count": str(len(js_members)),
        "rn_named_native_bytes": str(native_bytes),
        "rn_named_native_compressed_bytes": str(native_compressed),
        "rn_named_native_compressed_pct_uncompressed": pct(native_compressed, native_bytes),
        "rn_named_native_file_count": str(len(native_members)),
        "direct_rn_payload_bytes": str(direct_rn_payload),
        "direct_rn_payload_compressed_bytes": str(direct_rn_payload_compressed),
        "direct_rn_payload_compressed_pct_uncompressed": pct(direct_rn_payload_compressed, direct_rn_payload),
        "direct_rn_payload_pct_main_app": pct(direct_rn_payload, main_app_uncompressed),
        "direct_rn_payload_compressed_pct_main_app_compressed": pct(direct_rn_payload_compressed, main_app_compressed),
        "direct_rn_payload_pct_source_ipa": pct(direct_rn_payload, source_ipa_size),
        "direct_rn_payload_compressed_pct_source_ipa": pct(direct_rn_payload_compressed, source_ipa_size),
        "direct_rn_payload_compressed_pct_dump_ipa": pct(direct_rn_payload_compressed, dump_size),
        "js_bundle_pct_direct_rn_payload": pct(js_bytes, direct_rn_payload),
        "rn_named_native_pct_direct_rn_payload": pct(native_bytes, direct_rn_payload),
        "rn_carrier_macho_bytes": str(carrier_bytes) if carrier_bytes else "",
        "rn_carrier_macho_compressed_bytes": str(carrier_compressed) if carrier_compressed else "",
        "rn_carrier_macho_compressed_pct_dump_ipa": pct(carrier_compressed, dump_size),
        "rn_carrier_macho_pct_macho": pct(carrier_bytes, macho_total),
        "rn_carrier_macho_pct_main_app": pct(carrier_bytes, main_app_uncompressed),
        "rn_carrier_macho_count": str(len(carrier_macho_members)),
        "rn_carrier_macho_members": member_list(carrier_macho_members),
        "rn_evidence_class": rn_evidence_class,
        "static_linked_rn_likely": str(static_linked_likely).lower(),
        "remaining_encrypted_appex_count": str(len(remaining_appex)),
        "remaining_encrypted_non_extension_count": str(len(remaining_non_extension)),
        "rn_js_members": member_list(js_members),
        "rn_named_native_members": member_list(native_members),
        "notes": " ".join(notes),
        "dump_report": str(report_path),
        "dump_ipa": str(dump_ipa),
    }
    for member in component_members:
        size = int(member.get("bytes") or 0)
        compressed_size = int(member.get("compressed_bytes") or 0)
        member.update(
            {
                "app_slug": result["app_slug"],
                "app_name": result["app_name"],
                "bundle_id": bundle_id,
                "app_version": result["app_version"],
                "app_build": result["app_build"],
                "external_version_id": result["external_version_id"],
                "rn_guess": result["rn_guess"],
                "rn_evidence_class": rn_evidence_class,
                "bytes": str(size),
                "compressed_bytes": str(compressed_size),
                "compressed_pct_uncompressed": pct(compressed_size, size),
                "pct_main_app_uncompressed": pct(size, main_app_uncompressed),
                "pct_main_app_compressed": pct(compressed_size, main_app_compressed),
                "pct_source_ipa": pct(compressed_size, source_ipa_size),
                "pct_dump_ipa": pct(compressed_size, dump_size),
                "dump_report": str(report_path),
                "dump_ipa": str(dump_ipa),
            }
        )
    result["_component_members"] = component_members
    return result


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in FIELDS} for row in rows])


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    filtered = [{field: row.get(field, "") for field in FIELDS} for row in rows]
    path.write_text(json.dumps(filtered, indent=2, sort_keys=True) + "\n")


def component_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    components: list[dict[str, Any]] = []
    for row in rows:
        components.extend(row.get("_component_members") or [])
    return sorted(
        components,
        key=lambda member: (
            str(member.get("bundle_id", "")),
            str(member.get("app_version", "")),
            str(member.get("app_build", "")),
            str(member.get("component", "")),
            str(member.get("member", "")),
        ),
    )


def write_component_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COMPONENT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in COMPONENT_FIELDS} for row in rows])


def write_component_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    filtered = [{field: row.get(field, "") for field in COMPONENT_FIELDS} for row in rows]
    path.write_text(json.dumps(filtered, indent=2, sort_keys=True) + "\n")


def write_delta_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=DELTA_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in DELTA_FIELDS} for row in rows])


def write_delta_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    filtered = [{field: row.get(field, "") for field in DELTA_FIELDS} for row in rows]
    path.write_text(json.dumps(filtered, indent=2, sort_keys=True) + "\n")


def mib(value: Any) -> str:
    try:
        number = int(str(value) or "0")
    except ValueError:
        number = 0
    return f"{number / 1024 / 1024:.1f}"


def int_field(row: dict[str, Any], field: str) -> int:
    try:
        return int(str(row.get(field, "") or "0"))
    except ValueError:
        return 0


def float_field(row: dict[str, Any], field: str) -> float:
    try:
        return float(str(row.get(field, "") or "0"))
    except ValueError:
        return 0.0


def pct_field(row: dict[str, Any], field: str) -> str:
    value = str(row.get(field, ""))
    return value if value else "0.00"


def split_summary(row: dict[str, Any]) -> str:
    return f"{mib(row['js_bundle_bytes'])} MiB JS / {mib(row['rn_named_native_bytes'])} MiB native"


def evidence_label(row: dict[str, Any]) -> str:
    return str(row["rn_guess"]) if row["rn_guess"] and row["rn_guess"] != "unknown" else str(row["rn_evidence_class"])


def signed_mib(value: int) -> str:
    mib_value = value / 1024 / 1024
    if abs(mib_value) < 0.05:
        return "0.0"
    sign = "+" if mib_value > 0 else ""
    return f"{sign}{mib_value:.1f}"


def median_number(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def size_distribution(rows: list[dict[str, Any]], field: str) -> str:
    values = sorted(int_field(row, field) for row in rows if int_field(row, field) > 0)
    if not values:
        return "n/a"
    return f"median {mib(round(median_number([float(value) for value in values])))} MiB; range {mib(values[0])}-{mib(values[-1])} MiB"


def pct_distribution(rows: list[dict[str, Any]], field: str) -> str:
    values = [float_field(row, field) for row in rows if str(row.get(field, ""))]
    if not values:
        return "n/a"
    return f"median {median_number(values):.2f}%; range {min(values):.2f}-{max(values):.2f}%"


def short_member(member: str) -> str:
    if len(member) <= 72:
        return member
    return "..." + member[-69:]


def component_label(component: str) -> str:
    return {
        "js_bundle": "JS/Hermes bundle",
        "named_native_runtime": "Named native runtime",
        "rn_carrier_macho": "RN carrier Mach-O context",
    }.get(component, component)


def same_app_deltas(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_app: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_app[row["app_name"] or row["bundle_id"]].append(row)

    deltas: list[dict[str, Any]] = []
    for app, app_rows in sorted(by_app.items()):
        ordered = sorted(
            app_rows,
            key=lambda row: (row.get("build_timestamp", ""), row.get("external_version_id", ""), row.get("app_version", "")),
        )
        for previous, current in zip(ordered, ordered[1:]):
            deltas.append(
                {
                    "app": app,
                    "from_version": f"{previous['app_version']} ({previous['app_build']})",
                    "to_version": f"{current['app_version']} ({current['app_build']})",
                    "evidence": f"{evidence_label(previous)} -> {evidence_label(current)}",
                    "source_delta": int_field(current, "source_ipa_size_bytes") - int_field(previous, "source_ipa_size_bytes"),
                    "main_app_delta": int_field(current, "main_app_uncompressed_bytes")
                    - int_field(previous, "main_app_uncompressed_bytes"),
                    "direct_delta": int_field(current, "direct_rn_payload_bytes")
                    - int_field(previous, "direct_rn_payload_bytes"),
                    "direct_compressed_delta": int_field(current, "direct_rn_payload_compressed_bytes")
                    - int_field(previous, "direct_rn_payload_compressed_bytes"),
                    "js_delta": int_field(current, "js_bundle_bytes") - int_field(previous, "js_bundle_bytes"),
                    "native_delta": int_field(current, "rn_named_native_bytes")
                    - int_field(previous, "rn_named_native_bytes"),
                    "carrier_delta": int_field(current, "rn_carrier_macho_bytes")
                    - int_field(previous, "rn_carrier_macho_bytes"),
                }
            )
    return deltas


def markdown(rows: list[dict[str, Any]], members: list[dict[str, Any]], delta_rows: list[dict[str, Any]]) -> str:
    app_count = len({row["bundle_id"] for row in rows})
    rn_rows = [row for row in rows if row["rn_evidence_class"] != "no_rn_detected"]
    control_rows = [row for row in rows if row["rn_evidence_class"] == "no_rn_detected"]
    static_rows = [
        row
        for row in rn_rows
        if row["static_linked_rn_likely"] == "true" and int_field(row, "direct_rn_payload_bytes") == 0
    ]
    separable_rows = [row for row in rn_rows if int_field(row, "direct_rn_payload_bytes") > 0]
    js_rows = [row for row in rn_rows if int_field(row, "js_bundle_bytes") > 0]
    named_native_rows = [row for row in rn_rows if int_field(row, "rn_named_native_bytes") > 0]
    lines = [
        "# React Native Binary Size Overhead From Decrypted iOS Dumps",
        "",
        "## Scope",
        "",
        f"- Accepted decrypted dump rows analyzed: {len(rows)}",
        f"- Apps represented: {app_count}",
        "- Dump IPAs are local evidence under `tmp/ios-dumps`; they are not committed.",
        "- The sibling `rn-binary-size-overhead-members` CSV/JSON files list the exact JS bundle, named native runtime, and carrier Mach-O members used by this report; `rn-binary-size-overhead-deltas` records same-app sampled deltas.",
        "- `direct_rn_payload_bytes` is an RN-associated packaging floor: JS/Hermes bundle files plus separately named React Native/Hermes/JSI/Yoga native artifacts in the primary app bundle.",
        "- `direct_rn_payload_compressed_bytes` applies the dump IPA ZIP member compression to the same files. It is useful for relative package impact, but it is not a perfect App Store CDN byte count because decrypted re-zipping changes compression behavior for encrypted Mach-O pages.",
        "- JS/Hermes bundle bytes include app/product JavaScript as well as framework/runtime glue, so they are not pure React Native framework overhead.",
        "- `rn_named_native_bytes` is the closer framework/runtime signal when RN/Hermes/JSI/Yoga ship as separately named binaries.",
        "- Many iOS apps statically link React Native into the main executable. For those, exact RN-only native bytes cannot be separated from app code without link maps or symbol-level attribution, so `rn_carrier_macho_bytes` reports the containing Mach-O size as context, not as direct overhead.",
        "- Rows with no current RN evidence are retained as controls and should not be interpreted as RN overhead.",
        "",
        "## Observations",
        "",
        f"- RN-positive rows: {len(rn_rows)}; static-linked rows with no separable RN artifacts: {len(static_rows)}; negative/control rows: {len(control_rows)}.",
        f"- Separable direct RN-associated payload appears in {len(separable_rows)} RN-positive row(s): {size_distribution(separable_rows, 'direct_rn_payload_bytes')}.",
        f"- Compressed separable payload distribution: {size_distribution(separable_rows, 'direct_rn_payload_compressed_bytes')}; compressed/uncompressed ratio {pct_distribution(separable_rows, 'direct_rn_payload_compressed_pct_uncompressed')}.",
        f"- JS/Hermes bundle distribution where present: {size_distribution(js_rows, 'js_bundle_bytes')}; share of direct payload {pct_distribution(js_rows, 'js_bundle_pct_direct_rn_payload')}.",
        f"- Named native RN/Hermes/JSI/Yoga runtime distribution where present: {size_distribution(named_native_rows, 'rn_named_native_bytes')}; share of direct payload {pct_distribution(named_native_rows, 'rn_named_native_pct_direct_rn_payload')}.",
    ]

    top_direct = sorted(rn_rows, key=lambda row: int_field(row, "direct_rn_payload_bytes"), reverse=True)[:5]
    if top_direct:
        lines.append("- Largest RN-associated packaging floors:")
        for row in top_direct:
            app = row["app_name"] or row["bundle_id"]
            lines.append(
                f"  - {app} `{row['app_version']} ({row['app_build']})`: "
                f"{mib(row['direct_rn_payload_bytes'])} MiB "
                f"({pct_field(row, 'direct_rn_payload_pct_main_app')}% of primary app uncompressed bytes; "
                f"{split_summary(row)})."
            )

    if static_rows:
        max_static = max(static_rows, key=lambda row: int_field(row, "rn_carrier_macho_bytes"))
        lines.append(
            f"- Static-linked RN rows can have a zero direct-artifact floor; the largest carrier context is "
            f"{mib(max_static['rn_carrier_macho_bytes'])} MiB in "
            f"{max_static['app_name'] or max_static['bundle_id']} `{max_static['app_version']} ({max_static['app_build']})`."
        )

    top_native = sorted(rn_rows, key=lambda row: int_field(row, "rn_named_native_bytes"), reverse=True)[:5]
    if top_native:
        lines.append("- Largest separately named native RN/Hermes/JSI/Yoga runtime payloads:")
        for row in top_native:
            app = row["app_name"] or row["bundle_id"]
            lines.append(
                f"  - {app} `{row['app_version']} ({row['app_build']})`: "
                f"{mib(row['rn_named_native_bytes'])} MiB native runtime bytes "
                f"across {row['rn_named_native_file_count']} file(s)."
            )

    top_js = sorted(rn_rows, key=lambda row: int_field(row, "js_bundle_bytes"), reverse=True)[:5]
    if top_js:
        lines.append("- Largest JS/Hermes bundle payloads:")
        for row in top_js:
            app = row["app_name"] or row["bundle_id"]
            lines.append(
                f"  - {app} `{row['app_version']} ({row['app_build']})`: "
                f"{mib(row['js_bundle_bytes'])} MiB uncompressed "
                f"({mib(row['js_bundle_compressed_bytes'])} MiB compressed)."
            )

    control_apps = sorted({row["app_name"] or row["bundle_id"] for row in control_rows})
    if control_apps:
        lines.append("- No RN overhead is attributed to current negative/control rows: " + ", ".join(control_apps) + ".")

    lines.extend(
        [
            "",
            "## Size Lenses",
            "",
            "| Lens | What It Measures | Best Use | Important Limit |",
            "| --- | --- | --- | --- |",
            "| Direct uncompressed floor | JS/Hermes bundles plus separately named RN/Hermes/JSI/Yoga binaries in the primary app bundle | Installed app footprint attributable to RN packaging | Includes app/product JS, not just framework tax |",
            "| Direct compressed floor | ZIP-compressed bytes for the same direct files in the dumped IPA | Relative package/download pressure across sampled rows | Dump compression is not identical to App Store packaging |",
            "| Named native runtime floor | Separately named RN/Hermes/JSI/Yoga Mach-O artifacts only | Closest native runtime/framework payload when separable | Zero when RN is statically linked into app binaries |",
            "| Carrier Mach-O context | Decrypted Mach-O files containing RN markers | Upper context for static-linked RN | Usually much larger than the actual RN symbols |",
            "",
        ]
    )

    lines.extend(
        [
            "",
            "## Per-Dump Results",
            "",
            "| App | Version | RN evidence | RN floor | Compressed floor | Split | Direct % of app | RN carrier Mach-O | Coverage | Notes |",
            "| --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        app = row["app_name"] or row["bundle_id"]
        version = f"{row['app_version']} ({row['app_build']})"
        evidence = evidence_label(row)
        direct = mib(row["direct_rn_payload_bytes"])
        direct_compressed = mib(row["direct_rn_payload_compressed_bytes"])
        carrier = mib(row["rn_carrier_macho_bytes"])
        pct = pct_field(row, "direct_rn_payload_pct_main_app")
        notes = row["notes"].replace("|", "/")[:130]
        lines.append(
            f"| {app} | `{version}` | {evidence} | {direct} MiB | {direct_compressed} MiB | {split_summary(row)} | {pct}% | {carrier} MiB | "
            f"{row['decrypted_coverage']} | {notes} |"
        )

    lines.extend(
        [
            "",
            "## Component Breakdown",
            "",
            "| App | Version | Source IPA | Primary App | Main Executable | JS/Hermes Bundle | Named Native Runtime | Direct Compressed | Files |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        app = row["app_name"] or row["bundle_id"]
        version = f"{row['app_version']} ({row['app_build']})"
        files = f"{row['rn_js_file_count']} JS, {row['rn_named_native_file_count']} native, {row['rn_carrier_macho_count']} carrier"
        lines.append(
            f"| {app} | `{version}` | {mib(row['source_ipa_size_bytes'])} MiB | "
            f"{mib(row['main_app_uncompressed_bytes'])} MiB ({pct_field(row, 'main_app_compressed_pct_uncompressed')}% compressed) | "
            f"{mib(row['main_executable_bytes'])} MiB ({pct_field(row, 'main_executable_pct_main_app')}% of app) | "
            f"{mib(row['js_bundle_bytes'])} MiB ({pct_field(row, 'js_bundle_pct_direct_rn_payload')}% of direct) | "
            f"{mib(row['rn_named_native_bytes'])} MiB ({pct_field(row, 'rn_named_native_pct_direct_rn_payload')}% of direct) | "
            f"{mib(row['direct_rn_payload_compressed_bytes'])} MiB "
            f"({pct_field(row, 'direct_rn_payload_compressed_pct_dump_ipa')}% dump / "
            f"{pct_field(row, 'direct_rn_payload_compressed_pct_source_ipa')}% source) | {files} |"
        )

    top_members = sorted(members, key=lambda member: int_field(member, "bytes"), reverse=True)[:15]
    if top_members:
        lines.extend(
            [
                "",
                "## Top Component Members",
                "",
                "| App | Version | Component | Member | Uncompressed | Compressed | Role |",
                "| --- | --- | --- | --- | ---: | ---: | --- |",
            ]
        )
        for member in top_members:
            app = member["app_name"] or member["bundle_id"]
            version = f"{member['app_version']} ({member['app_build']})"
            role = "context only" if member.get("context_only") == "true" else "direct floor"
            lines.append(
                f"| {app} | `{version}` | {component_label(str(member['component']))} | "
                f"`{short_member(str(member['member'])).replace('|', '/')}` | "
                f"{mib(member['bytes'])} MiB | {mib(member['compressed_bytes'])} MiB | {role} |"
            )

    if delta_rows:
        lines.extend(
            [
                "",
                "## Sampled Same-App Deltas",
                "",
                "| App | Versions | Evidence | Source IPA | Primary App | Direct RN | Direct Compressed | JS | Native Runtime | Carrier Context |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for delta in delta_rows:
            lines.append(
                f"| {delta['app']} | `{delta['from_version']}` -> `{delta['to_version']}` | "
                f"{delta['evidence']} | {signed_mib(delta['source_delta'])} MiB | "
                f"{signed_mib(delta['main_app_delta'])} MiB | {signed_mib(delta['direct_delta'])} MiB | "
                f"{signed_mib(delta['direct_compressed_delta'])} MiB | {signed_mib(delta['js_delta'])} MiB | "
                f"{signed_mib(delta['native_delta'])} MiB | {signed_mib(delta['carrier_delta'])} MiB |"
            )

    if rn_rows:
        by_app: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rn_rows:
            by_app[row["app_name"] or row["bundle_id"]].append(row)
        lines.extend(["", "## App-Level Takeaways", ""])
        for app, app_rows in sorted(by_app.items()):
            ordered = sorted(
                app_rows,
                key=lambda row: (row.get("build_timestamp", ""), row.get("external_version_id", ""), row.get("app_version", "")),
            )
            first = ordered[0]
            latest = ordered[-1]
            max_direct = max(int_field(row, "direct_rn_payload_bytes") for row in app_rows)
            max_direct_compressed = max(int_field(row, "direct_rn_payload_compressed_bytes") for row in app_rows)
            max_native = max(int_field(row, "rn_named_native_bytes") for row in app_rows)
            max_js = max(int_field(row, "js_bundle_bytes") for row in app_rows)
            max_carrier = max(int_field(row, "rn_carrier_macho_bytes") for row in app_rows)
            delta = int_field(latest, "direct_rn_payload_bytes") - int_field(first, "direct_rn_payload_bytes")
            delta_text = f"; sampled direct delta {mib(delta)} MiB" if len(ordered) > 1 else ""
            lines.append(
                f"- {app}: RN-associated payload up to {mib(max_direct)} MiB "
                f"({mib(max_direct_compressed)} MiB compressed; JS/Hermes up to {mib(max_js)} MiB, "
                f"named native runtime up to {mib(max_native)} MiB); "
                f"largest RN carrier Mach-O context {mib(max_carrier)} MiB; "
                f"latest analyzed row `{latest['app_version']} ({latest['app_build']})`{delta_text}."
            )

    lines.extend(
        [
            "",
            "## Interpretation Limits",
            "",
            "- Treat `direct_rn_payload_bytes` as an RN-associated packaging floor, not a pure framework tax. It includes the app's JavaScript bundle because that bundle is required by the RN architecture, but app logic would exist in some form in a native implementation too.",
            "- Do not add `rn_carrier_macho_bytes` to `direct_rn_payload_bytes`. Carrier rows are context for Mach-O files that contain RN markers and can overlap with named native runtime files.",
            "- Treat `rn_carrier_macho_bytes` as context. When RN is statically linked into a large main executable, this field can be much larger than the actual RN symbols inside it.",
            "- Compressed byte columns are generated from the dumped IPA ZIP entries. They are useful for comparing sampled dumps, but source App Store packaging may differ.",
            "- Rows with `remaining_encrypted_non_extension_count > 0` may hide additional native bytes outside the main app process that the current dump did not decrypt.",
            "- Negative/control rows are important: they keep native or web-hybrid apps from being charged RN overhead just because generic React, JSI, or Yoga-like strings appear elsewhere.",
        ]
    )

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze RN size overhead in accepted decrypted iOS dumps.")
    parser.add_argument("--apps", type=Path, default=Path("apps.json"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    parser.add_argument("--dumps-dir", type=Path, default=Path("tmp/ios-dumps"))
    parser.add_argument("--out-prefix", type=Path, default=Path("reports/rn-binary-size-overhead"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    apps = app_entries(args.apps)
    apps_by_bundle = {str(app.get("bundle_id", "")): app for app in apps if app.get("bundle_id")}
    rows = report_rows(args.reports_dir)
    dump_reports = accepted_dump_reports(args.dumps_dir)
    chosen = choose_reports(dump_reports, rows)
    output_rows = [inspect_dump(path, report, row, apps_by_bundle) for path, report, row in chosen]
    members = component_rows(output_rows)
    deltas = same_app_deltas(output_rows)

    write_csv(args.out_prefix.with_suffix(".csv"), output_rows)
    write_json(args.out_prefix.with_suffix(".json"), output_rows)
    member_prefix = args.out_prefix.with_name(args.out_prefix.name + "-members")
    write_component_csv(member_prefix.with_suffix(".csv"), members)
    write_component_json(member_prefix.with_suffix(".json"), members)
    delta_prefix = args.out_prefix.with_name(args.out_prefix.name + "-deltas")
    write_delta_csv(delta_prefix.with_suffix(".csv"), deltas)
    write_delta_json(delta_prefix.with_suffix(".json"), deltas)
    args.out_prefix.with_suffix(".md").write_text(markdown(output_rows, members, deltas))

    print(f"analyzed {len(output_rows)} accepted decrypted dump rows across {len({r['bundle_id'] for r in output_rows})} apps")
    print(f"wrote {len(members)} component member rows")
    print(f"wrote {len(deltas)} same-app delta rows")
    for row in output_rows:
        print(
            f"{row['app_name'] or row['bundle_id']} {row['app_version']} ({row['app_build']}): "
            f"direct {mib(row['direct_rn_payload_bytes'])} MiB, carrier {mib(row['rn_carrier_macho_bytes']) or '0.0'} MiB, "
            f"{row['rn_evidence_class']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
