#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def sort_key(row: dict[str, str]) -> tuple[str, int]:
    value = row.get("version_code", "")
    return (
        row.get("source_publish_date", ""),
        int(value) if value.isdigit() else -1,
    )


def rn_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("rn_guess", ""),
        row.get("react_renderer", ""),
        row.get("confidence", ""),
    )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return sorted(list(csv.DictReader(f)), key=sort_key)


def make_ranges(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    ranges: list[dict[str, Any]] = []
    for row in rows:
        key = rn_key(row)
        if not ranges or ranges[-1]["key"] != key:
            ranges.append({"key": key, "start": row, "end": row, "build_count": 1})
        else:
            ranges[-1]["end"] = row
            ranges[-1]["build_count"] += 1

    output: list[dict[str, Any]] = []
    for item in ranges:
        start = item["start"]
        end = item["end"]
        output.append(
            {
                "rn_guess": item["key"][0],
                "react_renderer": item["key"][1],
                "confidence": item["key"][2],
                "start_app_version": start.get("version_name", ""),
                "start_app_build": start.get("version_code", ""),
                "start_external_version_id": start.get("version_code", ""),
                "start_build_timestamp": start.get("source_publish_date", ""),
                "end_app_version": end.get("version_name", ""),
                "end_app_build": end.get("version_code", ""),
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
