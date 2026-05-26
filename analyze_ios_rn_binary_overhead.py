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
    "total_uncompressed_bytes",
    "macho_total_bytes",
    "main_executable_bytes",
    "js_bundle_bytes",
    "js_bundle_compressed_bytes",
    "rn_named_native_bytes",
    "rn_named_native_compressed_bytes",
    "direct_rn_payload_bytes",
    "direct_rn_payload_pct_main_app",
    "rn_carrier_macho_bytes",
    "rn_carrier_macho_pct_macho",
    "rn_carrier_macho_members",
    "rn_evidence_class",
    "static_linked_rn_likely",
    "rn_js_members",
    "rn_named_native_members",
    "notes",
    "dump_report",
    "dump_ipa",
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
    main_app_uncompressed = 0
    js_bytes = 0
    js_compressed = 0
    native_bytes = 0
    native_compressed = 0
    js_members: list[str] = []
    native_members: list[str] = []

    with zipfile.ZipFile(dump_ipa) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            total_uncompressed += info.file_size
            if in_primary_app_scope(info.filename):
                main_app_uncompressed += info.file_size
            if RN_JS_RE.search(info.filename) and in_primary_app_scope(info.filename):
                js_bytes += info.file_size
                js_compressed += info.compress_size
                js_members.append(info.filename)
            if in_primary_app_scope(info.filename) and rn_native_binary_name(info.filename):
                native_bytes += info.file_size
                native_compressed += info.compress_size
                native_members.append(info.filename)

    inventory_entries = inventory.get("entries", []) if isinstance(inventory, dict) else []
    macho_total = sum(int(entry.get("size") or 0) for entry in inventory_entries if isinstance(entry, dict))
    main_executable_bytes = sum(
        int(entry.get("size") or 0)
        for entry in inventory_entries
        if isinstance(entry, dict) and entry.get("category") == "main_executable"
    )
    if not main_executable_bytes:
        executable = str(source.get("executable", ""))
        payload_app_dir = str(source.get("payload_app_dir", ""))
        main_member = f"{payload_app_dir}/{executable}" if payload_app_dir and executable else ""
        if main_member:
            with zipfile.ZipFile(dump_ipa) as zf:
                try:
                    main_executable_bytes = zf.getinfo(main_member).file_size
                except KeyError:
                    main_executable_bytes = 0

    rn_evidence_class, static_linked_likely, class_note = classify_rn(row)
    carrier_macho_members: list[str] = []
    carrier_macho_bytes = 0
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
                except KeyError:
                    continue
                if has_rn_carrier_marker(data, allow_generic_runtime_markers):
                    carrier_macho_members.append(member)
                    carrier_macho_bytes += int(entry.get("size") or len(data))

    direct_rn_payload = js_bytes + native_bytes
    carrier_bytes = max(native_bytes, carrier_macho_bytes)

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

    return {
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
        "total_uncompressed_bytes": str(total_uncompressed),
        "macho_total_bytes": str(macho_total) if macho_total else "",
        "main_executable_bytes": str(main_executable_bytes) if main_executable_bytes else "",
        "js_bundle_bytes": str(js_bytes),
        "js_bundle_compressed_bytes": str(js_compressed),
        "rn_named_native_bytes": str(native_bytes),
        "rn_named_native_compressed_bytes": str(native_compressed),
        "direct_rn_payload_bytes": str(direct_rn_payload),
        "direct_rn_payload_pct_main_app": pct(direct_rn_payload, main_app_uncompressed),
        "rn_carrier_macho_bytes": str(carrier_bytes) if carrier_bytes else "",
        "rn_carrier_macho_pct_macho": pct(carrier_bytes, macho_total),
        "rn_carrier_macho_members": member_list(carrier_macho_members),
        "rn_evidence_class": rn_evidence_class,
        "static_linked_rn_likely": str(static_linked_likely).lower(),
        "rn_js_members": member_list(js_members),
        "rn_named_native_members": member_list(native_members),
        "notes": " ".join(notes),
        "dump_report": str(report_path),
        "dump_ipa": str(dump_ipa),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in FIELDS} for row in rows])


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")


def mib(value: Any) -> str:
    try:
        number = int(str(value) or "0")
    except ValueError:
        number = 0
    return f"{number / 1024 / 1024:.1f}"


def markdown(rows: list[dict[str, Any]]) -> str:
    app_count = len({row["bundle_id"] for row in rows})
    rn_rows = [row for row in rows if row["rn_evidence_class"] != "no_rn_detected"]
    lines = [
        "# React Native Binary Size Overhead From Decrypted iOS Dumps",
        "",
        "## Scope",
        "",
        f"- Accepted decrypted dump rows analyzed: {len(rows)}",
        f"- Apps represented: {app_count}",
        "- Dump IPAs are local evidence under `tmp/ios-dumps`; they are not committed.",
        "- `direct_rn_payload_bytes` is a conservative floor: JS/Hermes bundle files plus separately named React Native/Hermes/JSI/Yoga native artifacts in the primary app bundle.",
        "- Many iOS apps statically link React Native into the main executable. For those, exact RN-only native bytes cannot be separated from app code without link maps or symbol-level attribution, so `rn_carrier_macho_bytes` reports the containing Mach-O size as context, not as direct overhead.",
        "- Rows with no current RN evidence are retained as controls and should not be interpreted as RN overhead.",
        "",
        "## Observations",
        "",
    ]

    top_direct = sorted(rn_rows, key=lambda row: int(row["direct_rn_payload_bytes"] or 0), reverse=True)[:5]
    if top_direct:
        lines.append("- Largest direct RN payload floors:")
        for row in top_direct:
            app = row["app_name"] or row["bundle_id"]
            lines.append(
                f"  - {app} `{row['app_version']} ({row['app_build']})`: "
                f"{mib(row['direct_rn_payload_bytes'])} MiB "
                f"({row['direct_rn_payload_pct_main_app']}% of primary app uncompressed bytes)."
            )

    static_rows = [
        row
        for row in rn_rows
        if row["static_linked_rn_likely"] == "true" and int(row["direct_rn_payload_bytes"] or 0) == 0
    ]
    if static_rows:
        max_static = max(static_rows, key=lambda row: int(row["rn_carrier_macho_bytes"] or 0))
        lines.append(
            f"- Static-linked RN rows can have a zero direct-artifact floor; the largest carrier context is "
            f"{mib(max_static['rn_carrier_macho_bytes'])} MiB in "
            f"{max_static['app_name'] or max_static['bundle_id']} `{max_static['app_version']} ({max_static['app_build']})`."
        )

    control_apps = sorted({row["app_name"] or row["bundle_id"] for row in rows if row["rn_evidence_class"] == "no_rn_detected"})
    if control_apps:
        lines.append("- No RN overhead is attributed to current negative/control rows: " + ", ".join(control_apps) + ".")

    lines.extend(
        [
            "",
        "## Per-Dump Results",
        "",
        "| App | Version | RN evidence | Direct RN payload | Direct % of app | RN carrier Mach-O | Coverage | Notes |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        app = row["app_name"] or row["bundle_id"]
        version = f"{row['app_version']} ({row['app_build']})"
        evidence = row["rn_guess"] if row["rn_guess"] and row["rn_guess"] != "unknown" else row["rn_evidence_class"]
        direct = mib(row["direct_rn_payload_bytes"])
        carrier = mib(row["rn_carrier_macho_bytes"])
        pct = row["direct_rn_payload_pct_main_app"]
        notes = row["notes"].replace("|", "/")[:130]
        lines.append(
            f"| {app} | `{version}` | {evidence} | {direct} MiB | {pct}% | {carrier} MiB | "
            f"{row['decrypted_coverage']} | {notes} |"
        )

    if rn_rows:
        by_app: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rn_rows:
            by_app[row["app_name"] or row["bundle_id"]].append(row)
        lines.extend(["", "## App-Level Takeaways", ""])
        for app, app_rows in sorted(by_app.items()):
            latest = max(app_rows, key=lambda row: (row.get("build_timestamp", ""), row.get("app_version", "")))
            max_direct = max(int(row["direct_rn_payload_bytes"] or 0) for row in app_rows)
            max_carrier = max(int(row["rn_carrier_macho_bytes"] or 0) for row in app_rows)
            lines.append(
                f"- {app}: direct RN payload floor up to {mib(max_direct)} MiB; "
                f"largest RN carrier Mach-O context {mib(max_carrier)} MiB; "
                f"latest analyzed row `{latest['app_version']} ({latest['app_build']})`."
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

    write_csv(args.out_prefix.with_suffix(".csv"), output_rows)
    write_json(args.out_prefix.with_suffix(".json"), output_rows)
    args.out_prefix.with_suffix(".md").write_text(markdown(output_rows))

    print(f"analyzed {len(output_rows)} accepted decrypted dump rows across {len({r['bundle_id'] for r in output_rows})} apps")
    for row in output_rows:
        print(
            f"{row['app_name'] or row['bundle_id']} {row['app_version']} ({row['app_build']}): "
            f"direct {mib(row['direct_rn_payload_bytes'])} MiB, carrier {mib(row['rn_carrier_macho_bytes']) or '0.0'} MiB, "
            f"{row['rn_evidence_class']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
