#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from lxml import html


def text_content(node: html.HtmlElement) -> str:
    return " ".join(node.text_content().split())


def parse_date(value: str) -> str:
    for fmt in ("%b %d, %Y", "%Y-%m-%d"):
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


def parse_versions(source_url: str, source_html: str, package_name: str) -> list[dict[str, str]]:
    document = html.fromstring(source_html)
    items = document.xpath(
        "//li[contains(concat(' ', normalize-space(@class), ' '), ' dt-version-item ')]"
    )
    versions: list[dict[str, str]] = []

    for index, item in enumerate(items):
        item_package = item.get("data-dt-package-name") or package_name
        if package_name and item_package != package_name:
            continue

        version_name = item.get("data-dt-version") or text_content(
            item.xpath(".//*[contains(concat(' ', normalize-space(@class), ' '), ' name ')][1]")[0]
        )
        version_code = item.get("data-dt-version-code", "")

        type_tags = [
            text_content(node)
            for node in item.xpath(
                ".//*[contains(concat(' ', normalize-space(@class), ' '), ' apk-type-tag ')]"
            )
        ]

        info_nodes = item.xpath(
            ".//*[contains(concat(' ', normalize-space(@class), ' '), ' additional-info ')]"
        )
        direct_spans = []
        if info_nodes:
            direct_spans = [text_content(node) for node in info_nodes[0].xpath("./span")]

        publish_date_raw = direct_spans[0] if len(direct_spans) > 0 else ""
        file_size = direct_spans[1] if len(direct_spans) > 1 else ""
        android_requirement = direct_spans[2] if len(direct_spans) > 2 else ""

        hrefs = item.xpath(
            ".//a[contains(concat(' ', normalize-space(@class), ' '), ' dt-version-title ')]/@href"
        )
        if not hrefs:
            hrefs = item.xpath(
                ".//a[contains(concat(' ', normalize-space(@class), ' '), ' download-btn ')]/@href"
            )
        stable_identifier = hrefs[0] if hrefs else ""
        download_url = urljoin(source_url, stable_identifier) if stable_identifier else ""

        versions.append(
            {
                "source": "APKPure",
                "source_order": str(index),
                "package_name": item_package,
                "version_name": version_name,
                "version_code": version_code,
                "package_file_type": ",".join(type_tags),
                "supported_abis": "",
                "split_metadata": ",".join(type_tags),
                "source_publish_date": parse_date(publish_date_raw),
                "source_publish_date_raw": publish_date_raw,
                "file_size": file_size,
                "android_requirement": android_requirement,
                "download_url": download_url,
                "stable_source_identifier": urlparse(download_url).path if download_url else "",
            }
        )

    return versions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch an APKPure Android version catalog.")
    parser.add_argument("--url", required=True, help="APKPure /versions URL.")
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_html = fetch_html(args.url, args.timeout)
    versions = parse_versions(args.url, source_html, args.package_name)
    if not versions:
        raise RuntimeError(f"no APKPure version entries found for {args.package_name}")

    output = {
        "schema_version": 1,
        "source": "APKPure",
        "source_url": args.url,
        "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "package_name": args.package_name,
        "entry_count": len(versions),
        "notes": [
            "APKPure currently exposes a limited visible version catalog on this page; treat missing historical Android versions as source limitations, not absence of releases."
        ],
        "versions": versions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(versions)} APKPure entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
