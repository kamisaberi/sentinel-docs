#!/usr/bin/env bash
# ==============================================================================
# ARYORITHM SENTINEL-DOCS: FEDERATED DOCUMENTATION & BUSINESS CORPUS HARVESTER
# Non-destructively mirrors existing docs/ suites, cartridge READMEs, business
# plans, startup LOI kits, and academic papers into /home/kami/sentinel-docs.
# ==============================================================================
set -euo pipefail

DOCS_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${DOCS_REPO}/.." && pwd)"

COMP_DIR="${DOCS_REPO}/docs/08-components"
ARCH_DIR="${DOCS_REPO}/docs/09-archive-business-and-research"

mkdir -p "${COMP_DIR}" "${ARCH_DIR}"/{business_plans,startup_kits,academic_papers}

echo "========================================================================"
echo "  ARYORITHM SENTINEL-DOCS: HARVESTING ECOSYSTEM DOCUMENTATION CORPUS"
echo "========================================================================"

# 1. Sync the 8 Core Repository docs/ Suites
CORE_REPOS=(
    "blackbox-essential"
    "blackbox-sentinel"
    "xinfer-essential"
    "xinfer-forge"
    "sentinel-nexus"
    "sentinel-matrix"
    "sentinel-lab"
    "sentinel-stack"
)

for repo in "${CORE_REPOS[@]}"; do
    SRC_DOCS="${WORKSPACE_ROOT}/${repo}/docs"
    DST_DOCS="${COMP_DIR}/${repo}"
    if [[ -d "${SRC_DOCS}" ]]; then
        mkdir -p "${DST_DOCS}"
        cp -ru "${SRC_DOCS}/"* "${DST_DOCS}/" 2>/dev/null || true
        echo "  ✓ Synced docs/ suite: ${repo}"
    fi
    if [[ -f "${WORKSPACE_ROOT}/${repo}/README.md" ]]; then
        cp -u "${WORKSPACE_ROOT}/${repo}/README.md" "${DST_DOCS}/README.md" 2>/dev/null || true
    fi
done

# 2. Sync Cartridge & Tier 0 READMEs
EXTRA_REPOS=("sentinel-fs" "ics-guard" "ccsds-guard" "net-guard" "motion-guard" "vision-guard" "sentinel-hub")
for repo in "${EXTRA_REPOS[@]}"; do
    if [[ -f "${WORKSPACE_ROOT}/${repo}/README.md" ]]; then
        mkdir -p "${COMP_DIR}/${repo}"
        cp -u "${WORKSPACE_ROOT}/${repo}/README.md" "${COMP_DIR}/${repo}/README.md"
        echo "  ✓ Synced README.md: ${repo}"
    fi
done
if [[ -f "${WORKSPACE_ROOT}/ccsds-guard/models.md" ]]; then
    cp -u "${WORKSPACE_ROOT}/ccsds-guard/models.md" "${COMP_DIR}/ccsds-guard/models.md"
fi

# 3. Consolidate Scattered Business Plans & Fundraising Materials
cp -u "${WORKSPACE_ROOT}/blackbox/BUSINESS_PLAN"*.md "${ARCH_DIR}/business_plans/" 2>/dev/null || true
cp -u "${WORKSPACE_ROOT}/blackbox/BUSINESS_PLAN"*.tex "${ARCH_DIR}/business_plans/" 2>/dev/null || true
cp -u "${WORKSPACE_ROOT}/blackbox-sentinel/temp/business_plan/"* "${ARCH_DIR}/business_plans/" 2>/dev/null || true
cp -u "${WORKSPACE_ROOT}/aegis-sky/BUSINESS_"* "${ARCH_DIR}/business_plans/" 2>/dev/null || true

# 4. Consolidate Startup, LOI, Pilot & Academic Outreach Kits
cp -u "${WORKSPACE_ROOT}/sentinel-nexus/temp/startup/"* "${ARCH_DIR}/startup_kits/" 2>/dev/null || true
cp -u "${WORKSPACE_ROOT}/sentinel-nexus/temp/subscription_plan/"* "${ARCH_DIR}/startup_kits/" 2>/dev/null || true
cp -u "${WORKSPACE_ROOT}/sentinel-stack/temp/pilot_agreement.md" "${ARCH_DIR}/startup_kits/" 2>/dev/null || true

# 5. Consolidate Academic Papers & Preprints
cp -u "${WORKSPACE_ROOT}/sentinel-lab/paper.tex" "${ARCH_DIR}/academic_papers/" 2>/dev/null || true
cp -u "${WORKSPACE_ROOT}/sentinel-lab/ACADEMIC_KIT.md" "${ARCH_DIR}/academic_papers/" 2>/dev/null || true

# 6. Generate Index Stubs for Synced Sections
cat << 'EOF' > "${COMP_DIR}/README.md"
# Component Documentation Suites (Auto-Synced)

This section aggregates the native `docs/` suites and `README.md` specifications across all 14 ecosystem repositories.
Run `./sync_docs.sh` at the repository root to pull the latest documentation updates from sibling repositories.
EOF

cat << 'EOF' > "${ARCH_DIR}/README.md"
# Business Plans, Startup Kits & Academic Archive

Consolidated repository of Aryorithm Technologies B.V. commercial documents:
- `business_plans/`: Master Business Plans (Markdown & LaTeX)
- `startup_kits/`: Silicon vendor applications, shadow pilot LOI agreements, and subscription models
- `academic_papers/`: CERN / Zenodo Preprint (`10.5281/zenodo.23598779`) and Academic Kit
EOF

echo "========================================================================"
echo "  HARVEST COMPLETE: $(find "${DOCS_REPO}/docs" -type f | wc -l) total files indexed."
echo "========================================================================"