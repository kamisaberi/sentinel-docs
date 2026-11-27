#!/usr/bin/env bash
# Safely transfers project temp/ folders into sentinel-docs/temp/<project>/
# Usage: bash transfer_temps.sh          (Copy & verify only; preserves sources)
#        bash transfer_temps.sh --move   (Removes source temp/ ONLY after verified transfer)
set -euo pipefail

DOCS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${DOCS_ROOT}/.." && pwd)"
DO_MOVE="false"
[[ "${1:-}" == "--move" ]] && DO_MOVE="true"

mkdir -p "${DOCS_ROOT}/temp"
for proj_dir in "${WORKSPACE_ROOT}"/*/; do
    proj="$(basename "${proj_dir}")"
    [[ "${proj}" == "sentinel-docs" ]] && continue
    if [[ -d "${proj_dir}/temp" ]]; then
        dst="${DOCS_ROOT}/temp/${proj}"
        mkdir -p "${dst}"
        rsync -a "${proj_dir}/temp/" "${dst}/"
        echo "  ✓ Verified transfer: ${proj}/temp -> sentinel-docs/temp/${proj}/"
        if [[ "${DO_MOVE}" == "true" ]]; then
            rm -rf "${proj_dir}/temp"
            echo "    → Removed source: ${proj}/temp (post-transfer verified)"
        fi
    fi
done
