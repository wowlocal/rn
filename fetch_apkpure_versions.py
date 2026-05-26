#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
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


def parse_download_entry(source_url: str, source_html: str, package_name: str) -> dict[str, str]:
    document = html.fromstring(source_html)
    page_data_match = re.search(r"window\.apkpure\s*=\s*\{pageData:\s*(\{.*?\})\}\s*</script>", source_html)
    page_data = json.loads(page_data_match.group(1)) if page_data_match else {}
    direct_links = [
        href
        for href in document.xpath("//a[@href]/@href")
        if "d.apkpure.net/b/" in href and "versionCode=" in href
    ]
    direct_url = direct_links[0] if direct_links else ""
    version_code_match = re.search(r"versionCode=([0-9]+)", direct_url)
    version_code = str(page_data.get("versionCode") or (version_code_match.group(1) if version_code_match else ""))
    version_name = str(page_data.get("versionName") or document.xpath("string(//*[contains(concat(' ', normalize-space(@class), ' '), ' version-name ')][1])")).strip()
    package_type = "XAPK" if "/b/XAPK/" in direct_url else "APK"
    publish_date_raw = document.xpath("string(//*[contains(concat(' ', normalize-space(@class), ' '), ' date ')][1])").strip()
    file_size = document.xpath("string(//*[contains(concat(' ', normalize-space(@class), ' '), ' version-file-size ')][1])").strip()
    android_requirement = document.xpath("string(//*[contains(concat(' ', normalize-space(@class), ' '), ' version-require ')][1])").strip()

    return {
        "source": "APKPure",
        "source_order": "",
        "package_name": package_name,
        "version_name": version_name,
        "version_code": version_code,
        "package_file_type": package_type,
        "supported_abis": "",
        "split_metadata": package_type,
        "source_publish_date": parse_date(publish_date_raw),
        "source_publish_date_raw": publish_date_raw,
        "file_size": file_size,
        "android_requirement": android_requirement,
        "download_url": source_url,
        "stable_source_identifier": urlparse(source_url).path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch an APKPure Android version catalog.")
    parser.add_argument("--url", required=True, help="APKPure /versions URL.")
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--extra-download-url", action="append", default=[])
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
    for extra_url in args.extra_download_url:
        versions.append(
            parse_download_entry(extra_url, fetch_html(extra_url, args.timeout), args.package_name)
        )
    if not versions:
        raise RuntimeError(f"no APKPure version entries found for {args.package_name}")
    deduped = {str(row.get("version_code", "")): row for row in versions if row.get("version_code")}
    versions = sorted(deduped.values(), key=version_sort_key, reverse=True)
    for index, row in enumerate(versions):
        row["source_order"] = str(index)

    output = {
        "schema_version": 1,
        "source": "APKPure",
        "source_url": args.url,
        "extra_source_urls": args.extra_download_url,
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
