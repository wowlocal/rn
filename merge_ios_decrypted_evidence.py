#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


DECRYPTED_FIELDS = [
    "decrypted_evidence",
    "source_ipa_sha256",
    "source_ipa_size",
    "decrypted_dump_sha256",
    "decrypted_dump_size",
    "dump_tool",
    "dump_command",
    "dump_device_context",
    "decrypted_coverage",
    "decrypted_main_cryptid",
    "mach_o_cryptid_summary",
    "remaining_encrypted_appex",
    "remaining_encrypted_non_extension",
]

ANALYZER_FIELDS = [
    "has_native_react_native_marker",
    "has_native_hermes_marker",
    "has_native_jsi_marker",
    "has_native_yoga_marker",
    "unknown_reason",
    "next_action",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def relpath(path: str) -> str:
    try:
        return str(Path(path).resolve().relative_to(Path.cwd()))
    except ValueError:
        return path


def external_id_from_path(path: str) -> str:
    match = re.search(r"_([0-9]+)\.ipa$", Path(path).name)
    return match.group(1) if match else ""


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_rows(csv_path: Path, json_path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")


def find_analysis_row(analysis_rows: list[dict[str, str]], dump_report: dict[str, Any]) -> dict[str, str]:
    metadata = dump_report["output"]["metadata"]
    for row in analysis_rows:
        if (
            row.get("bundle_id") == str(metadata.get("bundle_id", ""))
            and row.get("app_version") == str(metadata.get("version", ""))
            and row.get("app_build") == str(metadata.get("build", ""))
        ):
            return row
    raise ValueError(
        "analysis rows do not contain dumped metadata "
        f"{metadata.get('bundle_id')} {metadata.get('version')} ({metadata.get('build')})"
    )


def find_target_row(rows: list[dict[str, str]], dump_report: dict[str, Any]) -> dict[str, str]:
    source = dump_report["source"]
    source_path = relpath(str(source.get("path", "")))
    external_id = external_id_from_path(source_path)
    for row in rows:
        if row.get("ipa") == source_path:
            return row
    for row in rows:
        if (
            row.get("external_version_id") == external_id
            and row.get("bundle_id") == str(source.get("bundle_id", ""))
            and row.get("app_version") == str(source.get("version", ""))
            and row.get("app_build") == str(source.get("build", ""))
        ):
            return row
    raise ValueError(
        "versions report does not contain source IPA row "
        f"{source_path} {source.get('version')} ({source.get('build')})"
    )


def compact_inventory_summary(inventory: dict[str, Any]) -> str:
    summary = {
        "mach_o_count": inventory.get("mach_o_count"),
        "encrypted_count": inventory.get("encrypted_count"),
        "unknown_cryptid_count": inventory.get("unknown_cryptid_count"),
        "counts_by_category": inventory.get("counts_by_category", {}),
    }
    return json.dumps(summary, sort_keys=True, separators=(",", ":"))


def merge_evidence(row: dict[str, str], dump_report: dict[str, Any], analysis_row: dict[str, str]) -> None:
    verification = dump_report["verification"]
    coverage = verification["decrypted_coverage"]
    inventory = verification["mach_o_cryptid_inventory"]
    command = dump_report["dumper"].get("command", [])
    row.update(
        {
            "decrypted_evidence": str(bool(verification.get("accepted_decrypted_evidence"))).lower(),
            "source_ipa_sha256": str(dump_report["source"].get("sha256", "")),
            "source_ipa_size": str(dump_report["source"].get("size", "")),
            "decrypted_dump_sha256": str(dump_report["output"].get("sha256", "")),
            "decrypted_dump_size": str(dump_report["output"].get("size", "")),
            "dump_tool": str(dump_report["dumper"].get("method", "")),
            "dump_command": " ".join(str(part) for part in command),
            "dump_device_context": json.dumps(
                dump_report["device"].get("context", {}),
                sort_keys=True,
                separators=(",", ":"),
            ),
            "decrypted_coverage": str(coverage.get("coverage_class", "")),
            "decrypted_main_cryptid": str(
                verification.get("main_executable_encryption", {}).get("cryptid", "")
            ),
            "mach_o_cryptid_summary": compact_inventory_summary(inventory),
            "remaining_encrypted_appex": ";".join(coverage.get("remaining_encrypted_appex_members", [])),
            "remaining_encrypted_non_extension": ";".join(
                coverage.get("remaining_encrypted_non_extension_members", [])
            ),
        }
    )
    for field in ANALYZER_FIELDS:
        if field in analysis_row:
            row[field] = analysis_row[field]

    existing_notes = row.get("notes", "")
    decrypted_notes = analysis_row.get("notes", "")
    if decrypted_notes:
        decrypted_notes = f"Decrypted dump analysis: {decrypted_notes}"
    evidence_note = (
        f"Decrypted dump accepted as {row['decrypted_coverage']} with main cryptid "
        f"{row['decrypted_main_cryptid']}; source SHA-256 {row['source_ipa_sha256']}; "
        f"dump SHA-256 {row['decrypted_dump_sha256']}."
    )
    notes = [existing_notes]
    if decrypted_notes and decrypted_notes not in existing_notes:
        notes.append(decrypted_notes)
    notes.append(evidence_note)
    row["notes"] = " ".join(note for note in notes if note)


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge verified decrypted iOS dump evidence into version reports.")
    parser.add_argument("--versions-csv", type=Path, required=True)
    parser.add_argument("--versions-json", type=Path, required=True)
    parser.add_argument("--dump-report", type=Path, action="append", required=True)
    parser.add_argument("--analysis-json", type=Path, action="append", required=True)
    args = parser.parse_args()

    if len(args.dump_report) != len(args.analysis_json):
        raise SystemExit("--dump-report and --analysis-json must be supplied in matching counts")

    rows, fieldnames = read_rows(args.versions_csv)
    for field in ANALYZER_FIELDS + DECRYPTED_FIELDS:
        if field not in fieldnames:
            fieldnames.append(field)
        for row in rows:
            row.setdefault(field, "")

    for dump_report_path, analysis_json_path in zip(args.dump_report, args.analysis_json):
        dump_report = load_json(dump_report_path)
        analysis_rows = load_json(analysis_json_path)
        analysis_row = find_analysis_row(analysis_rows, dump_report)
        target_row = find_target_row(rows, dump_report)
        merge_evidence(target_row, dump_report, analysis_row)

    write_rows(args.versions_csv, args.versions_json, rows, fieldnames)
    print(f"updated {args.versions_csv}")
    print(f"updated {args.versions_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
