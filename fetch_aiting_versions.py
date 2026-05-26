#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from lxml import html


def fetch_html(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def extract_version_code(version_name: str) -> str:
    parts = version_name.split(".")
    for part in reversed(parts):
        if part.isdigit() and len(part) >= 4:
            return part
    for part in reversed(parts):
        if part.isdigit():
            return part
    return ""


def direct_apk_url(download_page_url: str, timeout: int) -> tuple[str, str]:
    document = html.fromstring(fetch_html(download_page_url, timeout))
    hrefs = document.xpath("//a[contains(@class, 'download-btn')]/@href")
    direct = next((href for href in hrefs if href.lower().endswith(".apk")), "")
    requirement = " ".join(document.xpath("//span[normalize-space()='Requires Android']/following-sibling::div[1]//text()")).strip()
    return direct, requirement


def parse_versions(url: str, package_name: str, timeout: int) -> list[dict[str, Any]]:
    document = html.fromstring(fetch_html(url, timeout))
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(document.xpath("//li[contains(@class, 'ov-body')]")):
        href = item.xpath(".//a[contains(@class, 'name')]/@href")
        version_text = " ".join(item.xpath(".//span[contains(@class, 'name-v')]//text()")).strip()
        size_text = " ".join(item.xpath(".//div[contains(@class, 'ov2')]//text()")).strip()
        if not href or not version_text:
            continue
        download_page = urljoin(url, href[0])
        if download_page in seen:
            continue
        seen.add(download_page)
        direct_url, android_requirement = direct_apk_url(download_page, timeout)
        rows.append(
            {
                "android_requirement": android_requirement,
                "download_url": direct_url or download_page,
                "file_size": size_text,
                "package_file_type": "APK",
                "package_name": package_name,
                "source": "Aiting",
                "source_order": str(index),
                "source_publish_date": "",
                "source_publish_date_raw": "",
                "split_metadata": "APK",
                "stable_source_identifier": download_page,
                "supported_abis": "",
                "version_code": extract_version_code(version_text),
                "version_name": version_text,
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch an Aiting Android version catalog.")
    parser.add_argument("--url", required=True, help="Aiting /versions URL.")
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    versions = parse_versions(args.url, args.package_name, args.timeout)
    if not versions:
        raise RuntimeError(f"no Aiting version entries found for {args.package_name}")
    payload = {
        "entry_count": len(versions),
        "extra_source_urls": [],
        "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "notes": [
            "Aiting exposes a source-limited visible old-version catalog; treat missing Android versions as source limitations, not absence of releases.",
            "Rows use direct APK URLs exposed by Aiting download pages. Source pages do not expose publish dates in the current parser.",
        ],
        "package_name": args.package_name,
        "schema_version": 1,
        "source": "Aiting",
        "source_url": args.url,
        "versions": versions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(versions)} Aiting entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
