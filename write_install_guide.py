#!/usr/bin/env python3
import pathlib

GUIDE_PATH = pathlib.Path("/home/kami/sentinel-docs/docs/05-operations-and-cli/00-master-installation-guide.md")
MKDOCS_YML = pathlib.Path("/home/kami/sentinel-docs/mkdocs.yml")

guide_content = """# Master Installation & Verification Guide

This document is the authoritative installation handbook for the **Aryorithm / Blackbox Sentinel 14-Repository Ecosystem**, synchronized 1-to-1 with the 7-phase `sentinel-stack` installer (`v2.0.0`).

---

## 1. Hardware & Operating System Prerequisites

| Requirement | Minimum Baseline | Production Recommendation |
| :--- | :--- | :--- |
| **Operating System** | Ubuntu 24.04 LTS / Debian 12 | Ubuntu 24.04 LTS or 26.04 (`x86_64` / `aarch64`) |
| **Linux Kernel** | `>= 6.5` with eBPF JIT | `>= 6.8` with `CONFIG_DEBUG_INFO_BTF=y` (`/sys/kernel/btf/vmlinux`) |
| **CPU & Memory** | 4 vCPUs, 4 GB RAM (auto-throttles to `-j2`) | 8+ Cores (`isolcpus`), 16+ GB RAM |
| **Compiler & Crypto** | GCC 13+ (C++20), CMake 3.20+, OpenSSL 3.x | GCC 15+, Clang/LLVM + `bpftool`, OpenSSL 3.5+ (FIPS 203 ML-KEM) |
| **Container Runtime** | Docker Engine + Compose v2 | Docker Engine (for `sentinel-matrix` Digital Twins) |
| **Hardware Root** | DMI UUID / vTPM fallback | Physical TPM 2.0 (`/dev/tpmrm0`) |

---

## 2. Method A: 1-Click Automated Installation (Recommended)

The `sentinel-stack` meta-installer orchestrates all **7 installation phases** in strict topological order (Tier 0 through Tier 4):

```bash
# Clone the master orchestrator repository
git clone https://github.com/kamisaberi/sentinel-stack.git
cd sentinel-stack

# Execute the full 7-phase installation (dependencies, 14 repos, 5 cartridges, 50 scenarios)
sudo ./install.sh
```

### Supported Installer Flags
* `sudo ./install.sh --skip-deps`: Skip `apt-get` and Python virtual environment provisioning (useful for pre-configured hosts).
* `sudo ./install.sh --skip-scenarios`: Compile and verify all 14 repositories without downloading/provisioning the 50 scenario recipes.
* `bash ./install.sh --scenarios-only`: Execute Phase 5 exclusively to populate `${SENTINEL_ROOT}/scenarios/catalog/`.

---

## 3. The 7 Automated Installation Phases

| Phase | Script | Execution Responsibilities |
| :--- | :--- | :--- |
| **Phase 0** | `scripts/00_check_system.sh` | Validates OS, CPU arch, Kernel BTF, OpenSSL version, mounts `/sys/fs/bpf`, creates `/etc/sentinel/` and `/opt/sentinel/packs/`. |
| **Phase 1** | `scripts/01_install_dependencies.sh` | Installs C++20, Clang/LLVM, `libbpf-dev`, `libxdp-dev`, gRPC/Protobuf, LuaJIT, and creates PEP 668 isolated `/opt/sentinel-stack/venv`. |
| **Phase 2** | `scripts/02_clone_repositories.sh` | Synchronizes all 14 ecosystem repositories into `${SENTINEL_WORKSPACE}` (sibling directory of `sentinel-stack`). |
| **Phase 3** | `scripts/03_build_all_tiers.sh` | Compiles and installs in strict DAG order: **Tier 0** (`sentinel-fs`, `xinfer-essential`, `blackbox-essential`) $\\to$ **Tier 1** (`blackbox-sentinel`, `xinfer-forge`) $\\to$ **Tier 2** (all 5 Domain Cartridges + `/opt/sentinel/packs/`) $\\to$ **Tier 3** (`sentinel-lab`, `sentinel-matrix`) $\\to$ **Tier 4** (`sentinel-nexus`, `aryo`). |
| **Phase 4** | `scripts/04_setup_systemd.sh` | Initializes SSFS (`sfs init`), deploys `sentinel-nexus.service` and `blackbox-sentinel.service`, and enables daemon supervision. |
| **Phase 5** | `scripts/05_provision_scenarios.sh` | Provisions all 50 real-world scenario recipes (`01_*.sh` – `50_*.sh`) into `${SENTINEL_ROOT}/scenarios/catalog/` with SHA-256 CAS deduplication. |
| **Phase 6** | `scripts/06_verify_installation.sh` | Executes the 30-point Sovereign Ecosystem Verification Suite (`ldd` linkage to `libsentinelfs.so`, dissectors, packs, and CLIs). |

---

## 4. Method B: Manual Tier-by-Tier Compilation (Developers)

If compiling individual tiers manually, always enforce the **Tier 0 $\\to$ Tier 4** order so shared libraries resolve cleanly in `/usr/local/lib`:

```bash
# 1. Tier 0: Sovereign Sentinel Filesystem (MUST BE BUILT FIRST)
cd sentinel-fs && cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc)
sudo cmake --install build && sudo ldconfig
sfs init

# Register Python sentinel_fs (PEP 668 compliant)
sudo /opt/sentinel-stack/venv/bin/pip install -e . --no-deps
USER_SITE="$(python3 -c 'import site; print(site.getusersitepackages())')"
mkdir -p "${USER_SITE}" && echo "$(pwd)/python" > "${USER_SITE}/sentinel_fs.pth"

# 2. Tier 0: xinfer-essential & blackbox-essential
cd ../xinfer-essential && cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cmake --install build && sudo ldconfig
cd ../blackbox-essential && cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cmake --install build && sudo ldconfig

# 3. Tier 1: blackbox-sentinel
cd ../blackbox-sentinel && cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc) --target sentinel sentinel_ctl sentinel_artifact sentinel_plugin_pack
sudo cmake --install build

# 4. Tier 2: Build All 5 Production Domain Cartridges
for cart in ics-guard ccsds-guard net-guard motion-guard vision-guard; do
    cd "../${cart}" && cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cmake --install build && sudo ldconfig
done

# 5. Tier 4: sentinel-nexus & aryo Master CLI
cd ../sentinel-nexus && cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) --target sentinel-nexus nexus-ctl && sudo cmake --install build
cd ../sentinel-stack && cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) --target aryo && sudo cmake --install build
```

---

## 5. Method C: Air-Gapped Offline Deployment (`.aryopack`)

For completely disconnected OT networks (`$0.00` cloud egress):

```bash
# On an internet-connected staging build host:
cd sentinel-stack
sudo bash scripts/export_system.sh sentinel_release_v2.aryopack

# Transfer sentinel_release_v2.aryopack via physical media to the air-gapped target host, then run:
sudo ./sentinel_release_v2.aryopack
```

The self-extracting installer unpacks all executables, `libsentinelfs.so`, all five cartridge libraries/dissectors, `/opt/sentinel/packs/`, the isolated Python virtual environment, Docker images, and the SSFS vault directly into `/var/lib/sentinel/`.

---

## 6. Provisioning All 50 Real-World Scenarios

To stage the complete 50-scenario catalog into `${SENTINEL_ROOT}/scenarios/catalog/`:

```bash
# Provision all 50 recipes (uses SHA-256 CAS hardlinks to avoid duplicate downloads)
bash /home/kami/sentinel-stack/scripts/05_provision_scenarios.sh

# Or provision selected recipes by prefix:
bash /home/kami/sentinel-stack/scripts/05_provision_scenarios.sh 01 05 11 21 31 43
```

---

## 7. Post-Installation 30-Point Verification

Confirm 100% ecosystem integrity after installation:

```bash
# Run the automated 30-point verifier (Must report 30/30 PASS)
bash /home/kami/sentinel-stack/scripts/06_verify_installation.sh

# Inspect Sovereign Filesystem anchor & appliance health
sfs status
sentinel-ctl status

# Verify all 5 domain cartridge extensions
for bin in aryo-ics aryo-aerospace aryo-net aryo-motion aryo-vision; do
    "${bin}" --plugin-desc && echo ""
done
```

---

## 8. Troubleshooting Reference

* **Ubuntu 24.04/26.04 PEP 668 (`externally-managed-environment`):** Never invoke `pip install` against the host system Python. Always target `/opt/sentinel-stack/venv/bin/pip` or drop a `.pth` pointer inside `$(python3 -c 'import site; print(site.getusersitepackages())')`.
* **Shared Library Not Found (`libsentinelfs.so`):** Execute `sudo ldconfig` after installing any Tier 0 or Tier 2 library into `/usr/local/lib`.
* **VMware Virtual NIC XDP Attachment:** Virtual adapters (`vmxnet3` / `veth`) automatically fall back to `SKB` generic XDP mode; bare-metal Intel/Mellanox NICs utilize zero-copy native `DRV` mode.
"""

GUIDE_PATH.write_text(guide_content.strip() + "\n", encoding="utf-8")
print(f"✓ Written Master Installation Guide: {GUIDE_PATH} ({len(guide_content):,} bytes)")

# Register in mkdocs.yml under Section 5 if not already linked
mk = MKDOCS_YML.read_text(encoding="utf-8")
entry = "      - Master Installation Guide: 05-operations-and-cli/00-master-installation-guide.md\n"
if "00-master-installation-guide.md" not in mk:
    mk = mk.replace(
        "  - 5. Operations & Scenarios:\n",
        "  - 5. Operations & Scenarios:\n" + entry
    )
    MKDOCS_YML.write_text(mk, encoding="utf-8")
    print("✓ Registered Master Installation Guide in mkdocs.yml under Section 5.")
else:
    print("✓ Master Installation Guide already registered in mkdocs.yml.")
