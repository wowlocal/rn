#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from lxml import html


def text_content(node: html.HtmlElement) -> str:
    return " ".join(node.text_content().split())


def parse_date(value: str) -> str:
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def fetch_html(url: str, timeout: int) -> str:
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


def detail_value(details: list[str], label: str) -> str:
    prefix = f"{label}:"
    for item in details:
        if item.startswith(prefix):
            return item[len(prefix) :].strip()
    return ""


def parse_versions(source_url: str, source_html: str, package_name: str) -> list[dict[str, str]]:
    document = html.fromstring(source_html)
    versions: list[dict[str, str]] = []

    for index, article in enumerate(document.xpath("//article")):
        direct_links = article.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' buttonDownload ')]/@href")
        if not direct_links:
            continue

        version_label = text_content(
            article.xpath(".//*[contains(concat(' ', normalize-space(@class), ' '), ' limit-line ')][1]")[0]
        )
        match = re.search(r"(.+?)\s*\((\d+)\)", version_label)
        if not match:
            continue

        details = [
            text_content(node)
            for node in article.xpath(".//*[contains(concat(' ', normalize-space(@class), ' '), ' date-on-tax ')]/div")
        ]
        file_size = detail_value(details, "File Size")
        android_requirement = detail_value(details, "Minimum")
        supported_abis = detail_value(details, "Architecture")
        screen_dpi = detail_value(details, "Screen DPI")
        md5 = detail_value(details, "MD5")
        publish_date_raw = detail_value(details, "Updated")
        download_url = direct_links[0]

        versions.append(
            {
                "source": "AndroidAPKsFree",
                "source_order": str(index),
                "package_name": package_name,
                "version_name": match.group(1).strip(),
                "version_code": match.group(2),
                "package_file_type": "APK",
                "supported_abis": supported_abis,
                "split_metadata": ";".join(value for value in ("APK", supported_abis, screen_dpi) if value),
                "source_publish_date": "",
                "source_publish_date_raw": publish_date_raw,
                "source_updated_date": parse_date(publish_date_raw),
                "file_size": file_size,
                "android_requirement": android_requirement,
                "download_url": download_url,
                "stable_source_identifier": urlparse(download_url).path,
                "source_md5": md5,
            }
        )

    return versions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch an AndroidAPKsFree Android version catalog.")
    parser.add_argument("--url", required=True, help="AndroidAPKsFree old versions URL.")
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def version_sort_key(row: dict[str, str]) -> tuple[str, int]:
    version_code = str(row.get("version_code", ""))
    return (
        str(row.get("source_publish_date", "")),
        int(version_code) if version_code.isdigit() else -1,
    )


def main() -> int:
    args = parse_args()
    source_html = fetch_html(args.url, args.timeout)
    versions = parse_versions(args.url, source_html, args.package_name)
    if not versions:
        raise RuntimeError(f"no AndroidAPKsFree version entries found for {args.package_name}")
    deduped = {str(row.get("version_code", "")): row for row in versions if row.get("version_code")}
    versions = sorted(deduped.values(), key=version_sort_key, reverse=True)
    for index, row in enumerate(versions):
        row["source_order"] = str(index)

    output = {
        "schema_version": 1,
        "source": "AndroidAPKsFree",
        "source_url": args.url,
        "extra_source_urls": [],
        "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "package_name": args.package_name,
        "entry_count": len(versions),
        "notes": [
            "AndroidAPKsFree exposes a source-limited historical APK catalog; treat missing versions as source limitations, not absence of releases.",
            "Rows use direct APK URLs exposed by the source page. Source-provided Updated dates are preserved as raw context but are not treated as release dates for ordering.",
        ],
        "versions": versions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(versions)} AndroidAPKsFree entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
