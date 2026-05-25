#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from pathlib import Path
from typing import Any


def build_sort_key(row: dict[str, str]) -> tuple[int, str]:
    build = row.get("app_build", "")
    return (int(build) if build.isdigit() else -1, row.get("ipa", ""))


def zip_build_timestamp(path: str) -> str:
    if not path:
        return ""
    ipa = Path(path)
    if not ipa.exists():
        return ""
    with zipfile.ZipFile(ipa) as zf:
        members = [
            name
            for name in zf.namelist()
            if name.startswith("Payload/") and name.endswith("/Info.plist") and ".app/" in name
        ]
        if not members:
            return ""
        info = zf.getinfo(sorted(members, key=lambda item: (len(item), item))[0])
        y, m, d, hh, mm, ss = info.date_time
        return f"{y:04d}-{m:02d}-{d:02d}T{hh:02d}:{mm:02d}:{ss:02d}"


def external_id_from_path(path: str) -> str:
    match = re.search(r"_([0-9]+)\.ipa$", Path(path).name)
    return match.group(1) if match else ""


def normalized_row(row: dict[str, str]) -> dict[str, str]:
    row = dict(row)
    row.setdefault("external_version_id", "")
    row.setdefault("build_timestamp", "")
    if not row["external_version_id"]:
        row["external_version_id"] = external_id_from_path(row.get("ipa", ""))
    if not row["build_timestamp"]:
        row["build_timestamp"] = zip_build_timestamp(row.get("ipa", ""))
    return row


def dedupe_builds(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped: dict[str, dict[str, str]] = {}
    for row in rows:
        build = row.get("app_build", "")
        if not build:
            continue
        current = deduped.get(build)
        if current is None:
            deduped[build] = row
            continue
        current_id = current.get("external_version_id", "")
        new_id = row.get("external_version_id", "")
        if new_id.isdigit() and (not current_id.isdigit() or int(new_id) > int(current_id)):
            deduped[build] = row
    return sorted(deduped.values(), key=build_sort_key)


def rn_key(row: dict[str, str]) -> tuple[str, str]:
    return (row.get("rn_guess", ""), row.get("react_renderer", ""))


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
                "confidence": start.get("confidence", ""),
                "start_app_version": start.get("app_version", ""),
                "start_app_build": start.get("app_build", ""),
                "start_external_version_id": start.get("external_version_id", ""),
                "start_build_timestamp": start.get("build_timestamp", ""),
                "end_app_version": end.get("app_version", ""),
                "end_app_build": end.get("app_build", ""),
                "end_external_version_id": end.get("external_version_id", ""),
                "end_build_timestamp": end.get("build_timestamp", ""),
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


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def parse_args(
    argv: list[str] | None = None,
    *,
    default_report: Path | None = None,
    default_out_prefix: Path | None = None,
    description: str | None = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=description or "Summarize IPA React Native version ranges."
    )
    parser.add_argument("--app-slug", default="app")
    parser.add_argument("--report", type=Path, default=default_report)
    parser.add_argument("--out-prefix", type=Path, default=default_out_prefix)
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Write app-layout outputs: timeline.json, ranges.csv/json, and transitions.csv/json.",
    )
    args = parser.parse_args(argv)
    if args.report is None:
        args.report = Path("reports") / args.app_slug / "versions.csv"
    if args.out_prefix is None and args.out_dir is None:
        args.out_dir = Path("reports") / args.app_slug
    return args


def main(
    argv: list[str] | None = None,
    *,
    default_report: Path | None = None,
    default_out_prefix: Path | None = None,
    description: str | None = None,
) -> int:
    args = parse_args(
        argv,
        default_report=default_report,
        default_out_prefix=default_out_prefix,
        description=description,
    )

    rows = [normalized_row(row) for row in csv.DictReader(args.report.open())]
    builds = dedupe_builds(rows)
    ranges = make_ranges(builds)
    transitions = make_transitions(ranges)
    data = {"build_count": len(builds), "ranges": ranges, "transitions": transitions}

    if args.out_prefix is not None:
        write_json(args.out_prefix.with_suffix(".json"), data)
        write_csv(args.out_prefix.with_name(args.out_prefix.name + "-ranges").with_suffix(".csv"), ranges)
        write_csv(args.out_prefix.with_name(args.out_prefix.name + "-transitions").with_suffix(".csv"), transitions)
    if args.out_dir is not None:
        write_json(args.out_dir / "timeline.json", data)
        write_json(args.out_dir / "ranges.json", ranges)
        write_json(args.out_dir / "transitions.json", transitions)
        write_csv(args.out_dir / "ranges.csv", ranges)
        write_csv(args.out_dir / "transitions.csv", transitions)

    if builds:
        first, last = builds[0], builds[-1]
        print(
            f"covered {len(builds)} unique app builds: "
            f"{first.get('app_version')} ({first.get('app_build')}) {first.get('build_timestamp')} -> "
            f"{last.get('app_version')} ({last.get('app_build')}) {last.get('build_timestamp')}"
        )
    for item in ranges:
        renderer = item["react_renderer"] or "unknown"
        print(
            f"{item['start_app_version']} ({item['start_app_build']}) {item['start_build_timestamp']} -> "
            f"{item['end_app_version']} ({item['end_app_build']}) {item['end_build_timestamp']}: "
            f"{item['rn_guess']} [{item['confidence']}], renderer {renderer}, builds {item['build_count']}"
        )
    if transitions:
        print("transitions:")
        for item in transitions:
            print(
                f"{item['from_rn_guess']} at {item['from_app_version']} ({item['from_app_build']}) "
                f"{item['from_build_timestamp']} -> {item['to_rn_guess']} at "
                f"{item['to_app_version']} ({item['to_app_build']}) {item['to_build_timestamp']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
