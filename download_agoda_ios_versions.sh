#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

usage() {
  cat <<'EOF'
Usage: ./download_agoda_ios_versions.sh [limit] [offset]

Downloads Agoda iOS IPAs into ipas/agoda after refreshing the App Store
version list at reports/agoda/version-list.json.

Arguments:
  limit   Number of IPAs to download. Default: 12.
  offset  Number of newest version-list entries to skip. Default: 0.

Examples:
  ./download_agoda_ios_versions.sh          # latest 12 entries
  ./download_agoda_ios_versions.sh 20       # latest 20 entries
  ./download_agoda_ios_versions.sh 20 20    # next 20 entries

Environment:
  RETRIES=4          ipatool retry count
  RETRY_DELAY=10     seconds between retries
  PURCHASE=1         pass --purchase to ipatool download
  FORCE=1            redownload existing IPA files
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

limit="${1:-12}"
offset="${2:-0}"
retries="${RETRIES:-4}"
retry_delay="${RETRY_DELAY:-10}"

if [[ ! "$limit" =~ ^[0-9]+$ || "$limit" == "0" ]]; then
  echo "limit must be a positive integer" >&2
  usage >&2
  exit 2
fi

if [[ ! "$offset" =~ ^[0-9]+$ ]]; then
  echo "offset must be a non-negative integer" >&2
  usage >&2
  exit 2
fi

common_args=(
  --app-slug agoda
  --app-name "Agoda: Cheap Flights & Hotels"
  --app-id 440676901
  --bundle-id com.agoda.consumer
  --retries "$retries"
  --retry-delay "$retry_delay"
)

env GODEBUG=http2client=0 ./check_rn_versions.py \
  "${common_args[@]}" \
  --version-list-out reports/agoda/version-list.json \
  --list-versions-only

download_args=(
  "${common_args[@]}"
  --versions-json reports/agoda/version-list.json
  --download-dir ipas/agoda
  --report reports/agoda/versions
  --include-latest
  --limit "$limit"
  --offset "$offset"
  --download-only
)

if [[ "${PURCHASE:-0}" == "1" ]]; then
  download_args+=(--purchase)
fi

if [[ "${FORCE:-0}" == "1" ]]; then
  download_args+=(--force)
fi

env GODEBUG=http2client=0 ./check_rn_versions.py "${download_args[@]}"
