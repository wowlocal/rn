#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from lxml import html


def fetch_html(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def text_content(node: html.HtmlElement, selector: str) -> str:
    value = node.xpath(selector)
    if isinstance(value, list):
        value = value[0] if value else ""
    return " ".join(str(value).split()) if value else ""


def parse_date(value: str) -> str:
    for fmt in ("%b %d, %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def parse_versions(source_url: str, source_html: str, package_name: str) -> list[dict[str, str]]:
    document = html.fromstring(source_html)
    rows: list[dict[str, str]] = []
    for index, item in enumerate(document.xpath('//*[@id="versions-items-list"]/*[@data-version-id]')):
        version_id = item.get("data-version-id", "")
        base_url = item.get("data-url", "")
        extra_url = item.get("data-extra-url", "download")
        download_url = urljoin(base_url.rstrip("/") + "/", f"{extra_url}/{version_id}") if base_url and version_id else ""
        package_type = text_content(item, 'string(.//*[contains(concat(" ", normalize-space(@class), " "), " type ")][1])')
        publish_date_raw = text_content(item, 'string(.//*[contains(concat(" ", normalize-space(@class), " "), " date ")][1])')
        rows.append(
            {
                "source": "Uptodown",
                "source_order": str(index),
                "package_name": package_name,
                "version_name": text_content(item, 'string(.//*[contains(concat(" ", normalize-space(@class), " "), " version ")][1])'),
                "version_code": version_id,
                "package_file_type": package_type.upper(),
                "supported_abis": "",
                "split_metadata": package_type.upper(),
                "source_publish_date": parse_date(publish_date_raw),
                "source_publish_date_raw": publish_date_raw,
                "file_size": "",
                "android_requirement": text_content(item, 'string(.//*[contains(concat(" ", normalize-space(@class), " "), " sdkVersion ")][1])'),
                "download_url": download_url,
                "stable_source_identifier": download_url,
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch an Uptodown Android version catalog.")
    parser.add_argument("--url", required=True, help="Uptodown /versions URL.")
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    versions = parse_versions(args.url, fetch_html(args.url, args.timeout), args.package_name)
    if not versions:
        raise RuntimeError(f"no Uptodown version entries found for {args.package_name}")
    output = {
        "schema_version": 1,
        "source": "Uptodown",
        "source_url": args.url,
        "extra_source_urls": [],
        "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "package_name": args.package_name,
        "entry_count": len(versions),
        "notes": [
            "Uptodown exposes a source-limited visible version catalog; treat missing Android versions as source limitations, not absence of releases.",
            "Rows point at Uptodown download pages. Direct package download support may require decoding the page-specific download token.",
        ],
        "versions": versions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(versions)} Uptodown entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
