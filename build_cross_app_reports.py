#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


TIMELINE_FIELDS = [
    "app_slug",
    "app_name",
    "app_status",
    "platform",
    "rn_guess",
    "react_renderer",
    "confidence",
    "start_app_version",
    "start_app_build",
    "start_external_version_id",
    "start_build_timestamp",
    "end_app_version",
    "end_app_build",
    "end_external_version_id",
    "end_build_timestamp",
    "build_count",
]

TRANSITION_FIELDS = [
    "app_slug",
    "app_name",
    "app_status",
    "platform",
    "from_rn_guess",
    "from_app_version",
    "from_app_build",
    "from_external_version_id",
    "from_build_timestamp",
    "to_rn_guess",
    "to_app_version",
    "to_app_build",
    "to_external_version_id",
    "to_build_timestamp",
    "version_list_gap_size",
    "version_list_boundary_exact",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def app_entries(apps_data: Any) -> list[dict[str, Any]]:
    if isinstance(apps_data, dict):
        apps = apps_data.get("apps", [])
    else:
        apps = apps_data
    if not isinstance(apps, list):
        raise ValueError("apps.json must contain an apps list")
    return [app for app in apps if isinstance(app, dict)]


def version_position_info(report_dir: Path, platform: str) -> tuple[dict[str, int], bool]:
    if platform == "android":
        version_list_path = report_dir / "android-version-list.json"
        if not version_list_path.exists():
            return {}, False
        data = load_json(version_list_path)
        versions = data.get("versions", [])
        if not isinstance(versions, list):
            return {}, False
        codes = sorted(
            {
                str(row.get("version_code", ""))
                for row in versions
                if isinstance(row, dict) and str(row.get("version_code", "")).isdigit()
            },
            key=int,
        )
        notes = " ".join(str(note).lower() for note in data.get("notes", []))
        source_limited = "limited" in notes or bool(data.get("extra_source_urls"))
        return {version_code: index for index, version_code in enumerate(codes)}, source_limited

    version_list_path = report_dir / "version-list.json"
    if not version_list_path.exists():
        return {}, False
    data = load_json(version_list_path)
    ids = data.get("externalVersionIdentifiers", [])
    if not isinstance(ids, list):
        return {}, False
    return {str(external_id): index for index, external_id in enumerate(ids)}, False


def transition_gap(row: dict[str, Any], positions: dict[str, int], source_limited: bool) -> tuple[str, str]:
    from_id = str(row.get("from_external_version_id", ""))
    to_id = str(row.get("to_external_version_id", ""))
    if not from_id or not to_id or from_id not in positions or to_id not in positions:
        return "", ""
    gap = abs(positions[to_id] - positions[from_id]) - 1
    exact = gap == 0 and not source_limited
    return str(gap), str(exact).lower()


def collect_reports(apps: list[dict[str, Any]], reports_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    timeline: list[dict[str, Any]] = []
    transitions: list[dict[str, Any]] = []

    for app in apps:
        slug = str(app.get("app_slug", ""))
        if not slug:
            continue
        report_dir = Path(str(app.get("reports_path") or reports_dir / slug))
        platform_reports = [
            ("ios", report_dir / "ranges.json", report_dir / "transitions.json"),
            ("android", report_dir / "android-ranges.json", report_dir / "android-transitions.json"),
        ]
        for platform, ranges_path, transitions_path in platform_reports:
            app_prefix = {
                "app_slug": slug,
                "app_name": app.get("app_name", ""),
                "app_status": app.get("status", ""),
                "platform": platform,
            }

            if ranges_path.exists():
                for row in load_json(ranges_path):
                    timeline.append({**app_prefix, **row})

            positions, source_limited = version_position_info(report_dir, platform)
            if transitions_path.exists():
                for row in load_json(transitions_path):
                    gap_size, exact = transition_gap(row, positions, source_limited)
                    transitions.append(
                        {
                            **app_prefix,
                            **row,
                            "version_list_gap_size": gap_size,
                            "version_list_boundary_exact": exact,
                        }
                    )

    return timeline, transitions


def summary_markdown(apps: list[dict[str, Any]], timeline: list[dict[str, Any]], transitions: list[dict[str, Any]]) -> str:
    analyzed = [app for app in apps if app.get("status") == "done"]
    queued = [app for app in apps if app.get("status") == "queued"]
    skipped = [app for app in apps if app.get("status") == "skipped"]
    review = [app for app in apps if app.get("status") == "needs_manual_review"]
    in_progress = [
        app
        for app in apps
        if app.get("status") not in {"done", "queued", "skipped", "needs_manual_review"}
    ]
    exact = [row for row in transitions if row.get("version_list_boundary_exact") == "true"]
    approximate = [
        row
        for row in transitions
        if row.get("version_list_boundary_exact") and row.get("version_list_boundary_exact") != "true"
    ]

    lines = [
        "# Popular React Native Mobile Apps Timeline Summary",
        "",
        "## Methodology",
        "",
        "Reports keep platform-specific package timelines separate, then merge them here with platform labels. iOS reports use IPA internal zip timestamps from app bundle `Info.plist` members unless an App Store date is independently verified. Android APK/APKS/XAPK/APKM analysis is first-class evidence when packages are available, with Android ordering based on versionCode and source publish dates when available. Source-limited Android catalogs can guide ranges but do not make transition boundaries exact merely because adjacent fetched rows have no known row between them. Exact RN patch versions are reported only when strong markers are exposed; encrypted native binaries generally limit results to RN version bands inferred from JS bundle markers.",
        "",
        "## App Status",
        "",
        f"- Analyzed successfully: {len(analyzed)}",
        f"- Queued: {len(queued)}",
        f"- In progress: {len(in_progress)}",
        f"- Needs manual review: {len(review)}",
        f"- Skipped: {len(skipped)}",
        "",
    ]

    if analyzed:
        lines.extend(["## Analyzed Apps", ""])
        for app in analyzed:
            lines.append(
                f"- {app.get('app_name', app.get('app_slug'))}: {app.get('external_version_count', '')} iOS external versions; reports in `{app.get('reports_path', '')}`"
            )
        lines.append("")

    if queued:
        lines.extend(["## Queued Apps", ""])
        for app in queued:
            lines.append(
                f"- {app.get('app_name', app.get('app_slug'))}: App Store ID {app.get('app_id', '')}; bundle ID {app.get('bundle_id', '')}"
            )
        lines.append("")

    if in_progress:
        lines.extend(["## In Progress Apps", ""])
        for app in in_progress:
            lines.append(
                f"- {app.get('app_name', app.get('app_slug'))}: status `{app.get('status', '')}`; last completed `{app.get('last_completed_step', '')}`; reports in `{app.get('reports_path', '')}`"
            )
        lines.append("")

    if review:
        lines.extend(["## Manual Review Apps", ""])
        for app in review:
            lines.append(
                f"- {app.get('app_name', app.get('app_slug'))}: last completed `{app.get('last_completed_step', '')}`; reports in `{app.get('reports_path', '')}`"
            )
        lines.append("")

    if skipped:
        lines.extend(["## Skipped Apps", ""])
        for app in skipped:
            note = "; ".join(str(item) for item in app.get("notes", []))
            lines.append(f"- {app.get('app_name', app.get('app_slug'))}: {note}")
        lines.append("")

    if timeline:
        lines.extend(["## RN Ranges", ""])
        lines.append("| App | Platform | RN guess | Renderer | Confidence | Start | End | Builds |")
        lines.append("|---|---|---|---:|---|---|---|---:|")
        for row in timeline:
            lines.append(
                "| {app_name} | {platform} | {rn_guess} | {react_renderer} | {confidence} | {start_app_version} ({start_app_build}) | {end_app_version} ({end_app_build}) | {build_count} |".format(
                    **{key: row.get(key, "") for key in TIMELINE_FIELDS}
                )
            )
        lines.append("")

    if transitions:
        lines.extend(["## RN Transitions", ""])
        lines.append("| App | Platform | From | To | Last old | First new | Known-list gap | Exact? |")
        lines.append("|---|---|---|---|---|---|---:|---|")
        for row in transitions:
            lines.append(
                "| {app_name} | {platform} | {from_rn_guess} | {to_rn_guess} | {from_app_version} ({from_app_build}) | {to_app_version} ({to_app_build}) | {version_list_gap_size} | {version_list_boundary_exact} |".format(
                    **{key: row.get(key, "") for key in TRANSITION_FIELDS}
                )
            )
        lines.append("")

    lines.extend(
        [
            "## Boundary Confidence",
            "",
            f"- Exact by transition IDs: {len(exact)}",
            f"- Approximate by transition IDs: {len(approximate)}",
            "- Per-app notes may refine duplicate-build boundary cases where multiple external IDs map to the same app build.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build cross-app React Native timeline reports.")
    parser.add_argument("--apps", type=Path, default=Path("apps.json"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()

    apps = app_entries(load_json(args.apps))
    timeline, transitions = collect_reports(apps, args.reports_dir)
    write_csv(args.reports_dir / "all-apps-rn-timeline.csv", timeline, TIMELINE_FIELDS)
    write_json(args.reports_dir / "all-apps-rn-timeline.json", timeline)
    write_csv(args.reports_dir / "all-apps-rn-transitions.csv", transitions, TRANSITION_FIELDS)
    write_json(args.reports_dir / "all-apps-rn-transitions.json", transitions)
    (args.reports_dir / "summary.md").write_text(summary_markdown(apps, timeline, transitions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
