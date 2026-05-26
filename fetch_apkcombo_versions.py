#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse
from urllib.request import Request, urlopen

from lxml import html


MONTHS = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}


def fetch_html(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def parse_date(value: str) -> str:
    match = re.search(r"\b([A-Z][a-z]{2})\s+(\d{1,2}),\s+(\d{4})\b", value)
    if not match:
        return ""
    month, day, year = match.groups()
    if month not in MONTHS:
        return ""
    return f"{year}-{MONTHS[month]}-{int(day):02d}"


def decode_variant_url(href: str) -> str:
    parsed = urlparse(href)
    encoded = parse_qs(parsed.query).get("u", [""])[0]
    if not encoded:
        return ""
    padding = "=" * (-len(encoded) % 4)
    decoded = base64.urlsafe_b64decode(encoded + padding).decode("utf-8", "replace")
    if urlparse(decoded).scheme not in {"http", "https"}:
        return ""
    return decoded


def parse_download_page(url: str, timeout: int) -> dict[str, str]:
    document = html.fromstring(fetch_html(url, timeout))
    variant = document.xpath("//a[contains(@class, 'variant')][1]")
    if not variant:
        return {}
    href = urljoin(url, variant[0].get("href", ""))
    text = " ".join(variant[0].text_content().split())
    code = ""
    code_match = re.search(r"\((\d+)\)", text)
    if code_match:
        code = code_match.group(1)
    size = ""
    size_match = re.search(r"\b(\d+(?:\.\d+)?\s*(?:MB|GB))\b", text)
    if size_match:
        size = size_match.group(1)
    requirement = ""
    requirement_match = re.search(r"\bAndroid\s+[^ ]+\+", text)
    if requirement_match:
        requirement = requirement_match.group(0)
    package_type = "XAPK" if "XAPK" in text.upper() else "APK"
    return {
        "android_requirement": requirement,
        "download_url": decode_variant_url(href),
        "file_size": size,
        "package_file_type": package_type,
        "split_metadata": package_type,
        "version_code": code,
    }


def parse_versions(url: str, package_name: str, pages: int, timeout: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    source_order = 0
    for page in range(1, pages + 1):
        page_url = url if page == 1 else f"{url.rstrip('/')}/?page={page}"
        document = html.fromstring(fetch_html(page_url, timeout))
        for item in document.xpath("//a[contains(@class, 'ver-item')]"):
            href = urljoin(page_url, item.get("href", ""))
            if href in seen:
                continue
            seen.add(href)
            text = " ".join(item.text_content().split())
            match = re.search(r"\s+(XAPK|APK)\s+(.+?)\s+·\s+(Android\s+[^ ]+\+)", text)
            if match:
                package_type, date_raw, requirement = match.groups()
                name_and_version = text[: match.start()].strip()
                version_match = re.search(r"(\d[\w./-]*)$", name_and_version)
                version_name = version_match.group(1) if version_match else ""
            else:
                parts = text.split()
                version_name = parts[1] if len(parts) > 1 else ""
                package_type = "XAPK" if "XAPK" in text.upper() else "APK"
                date_raw = text
                requirement = ""
            detail = parse_download_page(href, timeout)
            if not detail.get("download_url"):
                continue
            rows.append(
                {
                    "android_requirement": detail.get("android_requirement") or requirement,
                    "download_url": detail.get("download_url", ""),
                    "file_size": detail.get("file_size", ""),
                    "package_file_type": detail.get("package_file_type") or package_type,
                    "package_name": package_name,
                    "source": "APKCombo",
                    "source_order": str(source_order),
                    "source_publish_date": parse_date(date_raw),
                    "source_publish_date_raw": date_raw,
                    "split_metadata": detail.get("split_metadata") or package_type,
                    "stable_source_identifier": href,
                    "supported_abis": "",
                    "version_code": detail.get("version_code", ""),
                    "version_name": version_name,
                }
            )
            source_order += 1
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch an APKCombo Android version catalog.")
    parser.add_argument("--url", required=True, help="APKCombo old-versions URL.")
    parser.add_argument("--package-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    versions = parse_versions(args.url, args.package_name, args.pages, args.timeout)
    if not versions:
        raise RuntimeError(f"no APKCombo version entries found for {args.package_name}")
    payload = {
        "entry_count": len(versions),
        "extra_source_urls": [f"{args.url.rstrip('/')}/?page={page}" for page in range(2, args.pages + 1)],
        "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "notes": [
            "APKCombo exposes a source-limited visible old-version catalog; treat missing Android versions as source limitations, not absence of releases.",
            "Rows use direct XAPK/APK URLs decoded from APKCombo variant links. Verify package hashes and embedded manifests before trusting historical rows.",
        ],
        "package_name": args.package_name,
        "schema_version": 1,
        "source": "APKCombo",
        "source_url": args.url,
        "versions": versions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(versions)} APKCombo entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
