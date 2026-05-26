#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    manifest_version_code = row.get("manifest_version_code", "")
    if manifest_version_code.isdigit():
        return (0, int(manifest_version_code), row.get("source_publish_date", ""))
    source_order = row.get("source_order", "")
    if source_order.isdigit():
        return (1, -int(source_order), row.get("source_publish_date", ""))
    value = row.get("version_code", "")
    return (
        2,
        int(value) if value.isdigit() else -1,
        row.get("source_publish_date", ""),
    )


def rn_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("rn_guess", ""),
        row.get("react_renderer", ""),
        row.get("confidence", ""),
    )


def app_version(row: dict[str, str]) -> str:
    return row.get("manifest_version_name") or row.get("version_name", "")


def app_build(row: dict[str, str]) -> str:
    return row.get("manifest_version_code") or row.get("version_code", "")


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return sorted(list(csv.DictReader(f)), key=sort_key)


def make_ranges(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    ranges: list[dict[str, Any]] = []
    for row in rows:
        key = rn_key(row)
        if not ranges or ranges[-1]["key"] != key:
            ranges.append(
                {
                    "key": key,
                    "start": row,
                    "end": row,
                    "build_count": 1,
                    "package_hashes": set(),
                    "sources": set(),
                    "source_dates": [],
                }
            )
        else:
            ranges[-1]["end"] = row
            ranges[-1]["build_count"] += 1
        package_hash = row.get("package_sha256", "")
        if package_hash:
            ranges[-1]["package_hashes"].add(package_hash)
        source = row.get("source", "")
        if source:
            ranges[-1]["sources"].add(source.lower())
        source_date = row.get("source_publish_date", "")
        if source_date:
            ranges[-1]["source_dates"].append(source_date)

    output: list[dict[str, Any]] = []
    for item in ranges:
        start = item["start"]
        end = item["end"]
        package_hash_count = len(item["package_hashes"])
        source_quality = ""
        if package_hash_count and package_hash_count < item["build_count"]:
            source_quality = f"duplicate package hashes ({package_hash_count}/{item['build_count']})"
        if "uptodown" in item["sources"]:
            source_note = "source-limited Uptodown catalog; source IDs are not manifest versionCodes"
            source_quality = f"{source_quality}; {source_note}" if source_quality else source_note
        source_dates = item["source_dates"]
        if any(current < previous for previous, current in zip(source_dates, source_dates[1:])):
            source_note = "source dates are non-monotonic versus manifest versionCode"
            source_quality = f"{source_quality}; {source_note}" if source_quality else source_note
        output.append(
            {
                "rn_guess": item["key"][0],
                "react_renderer": item["key"][1],
                "confidence": item["key"][2],
                "source_quality": source_quality,
                "start_app_version": app_version(start),
                "start_app_build": app_build(start),
                "start_external_version_id": start.get("version_code", ""),
                "start_build_timestamp": start.get("source_publish_date", ""),
                "end_app_version": app_version(end),
                "end_app_build": app_build(end),
                "end_external_version_id": end.get("version_code", ""),
                "end_build_timestamp": end.get("source_publish_date", ""),
                "build_count": item["build_count"],
            }
        )
    return output


def make_transitions(ranges: list[dict[str, Any]]) -> list[dict[str, str]]:
    transitions: list[dict[str, str]] = []
    for previous, current in zip(ranges, ranges[1:]):
        transitions.append(
            {
                "from_rn_guess": previous["rn_guess"],
                "from_app_version": previous["end_app_version"],
                "from_app_build": previous["end_app_build"],
                "from_external_version_id": previous["end_external_version_id"],
                "from_build_timestamp": previous["end_build_timestamp"],
                "to_rn_guess": current["rn_guess"],
                "to_app_version": current["start_app_version"],
                "to_app_build": current["start_app_build"],
                "to_external_version_id": current["start_external_version_id"],
                "to_build_timestamp": current["start_build_timestamp"],
            }
        )
    return transitions


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Android RN version ranges.")
    parser.add_argument("--report", type=Path, required=True, help="android-versions.csv path")
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = load_rows(args.report)
    ranges = make_ranges(rows)
    transitions = make_transitions(ranges)
    write_csv(args.out_dir / "android-ranges.csv", ranges)
    write_json(args.out_dir / "android-ranges.json", ranges)
    write_csv(args.out_dir / "android-transitions.csv", transitions)
    write_json(args.out_dir / "android-transitions.json", transitions)
    print(f"covered {len(rows)} Android package rows")
    for row in ranges:
        print(
            f"{row['start_app_version']} ({row['start_app_build']}) -> "
            f"{row['end_app_version']} ({row['end_app_build']}): "
            f"{row['rn_guess']} [{row['confidence']}], builds {row['build_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
