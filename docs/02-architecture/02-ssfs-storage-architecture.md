# The Sovereign Sentinel Filesystem (SSFS) Architecture

The **Sovereign Sentinel Filesystem (SSFS)**, implemented in **Tier 0 `sentinel-fs`**, permanently decouples dynamic runtime artifacts from git repository trees.

---

## 1. Privilege-Aware Root Anchor Resolution

All binaries (`aryo`, `sentinel`, `sentinel-ctl`, `sentinel-nexus`) and Python tools (`scenario_engine.py`, `fetch_scenario_assets.py`) resolve storage paths through `sentinel::fs::PathResolver` using strict precedence:

1. **Explicit Argument Override:** `--sentinel-root <path>`
2. **Environment Variable:** `export SENTINEL_ROOT="<path>"`
3. **Privilege Detection:**
   * **System Daemon Mode (`UID == 0` / Root):** `/var/lib/sentinel`
   * **User Mode (`UID != 0` / Non-Root):** `${HOME}/.sentinel`

---

## 2. The 7 Primary Artifact Classes

```text
${SENTINEL_ROOT}/
├── spkg/                       <-- Sentinel Distribution Packages (.spkg.zst)
│   ├── installed/              <-- Active unpacked plugins (/web, /plugins.d)
│   ├── cache/                  <-- Signed package tarballs
│   └── staging/                <-- Atomic verification workspace
│
├── scenarios/                  <-- Digital Twin Simulation Meshes
│   ├── catalog/                <-- Declarative scenario definitions (scenario.yaml)
│   ├── workspaces/             <-- Rendered Docker Compose workspaces (<slug>/)
│   └── snapshots/              <-- Incident memory & telemetry dumps
│
├── blueprints/                 <-- Hardware & Network Topology Blueprints
│   ├── hardware/               <-- PCIe BDF addresses, AF_XDP NIC bindings
│   ├── apparatus/              <-- Plant ODE descriptors & 3D keep-out meshes
│   └── tsn/                    <-- IEEE 802.1Qbv cycle slot schedules
│
├── models/                     <-- Machine Learning Model Substrate
│   ├── registry/<sha256>       <-- Content-Addressable Storage (CAS) of verified base models
│   ├── calibrated/             <-- Domain-specific autoencoders (water_dosing_ae.onnx, etc.)
│   └── forge/checkpoints/      <-- xinfer-forge continual learning representations
│
├── slab/                       <-- Sentinel Lab Research Testbed
│   ├── experiments/            <-- 14-D state trajectories & Lyaponuv metrics
│   ├── benchmarks/             <-- Sub-120 ns hardware cycle histograms
│   └── trajectories/           <-- Runge-Kutta 4th-Order phase space logs
│
├── artifacts/                  <-- Heavy Binary Asset Ingress
│   ├── pcaps/                  <-- Raw wire captures cataloged by protocol
│   └── downloads/              <-- Transient HTTPS & Git LFS download buffers
│
├── pki/                        <-- Hardware Silicon Identity & mTLS
│   ├── ca/                     <-- Root & Intermediate authority certs
│   ├── certs/                  <-- Node cryptographic credentials
│   └── tpm/                    <-- Physical TPM 2.0 SRK handles & PCR quotes
│
└── runtime/                    <-- Volatile IPC descriptor handles
    ├── sockets/                <-- AF_UNIX domain bridges (can://bus0)
    └── locks/                  <-- Kernel advisory concurrency locks
```

---

## 3. Content-Addressable Storage (CAS) Deduplication

Heavy binary assets (such as multi-megabyte PCAPs and ONNX weight tensors) are never duplicated across scenario directories. When `fetch_scenario_assets.py` or `models_downloader.sh` retrieves an asset:

1. `CasStore` computes its OpenSSL EVP SHA-256 digest with zero memory copies.
2. The file is committed to `${SENTINEL_ROOT}/models/registry/<sha256>` or `${SENTINEL_ROOT}/artifacts/pcaps/<sha256>`.
3. Active scenario staging areas create POSIX hardlinks (`link_or_copy()`) pointing to the CAS store. If two scenarios use identical 50 MB PCAP baselines, disk consumption is exactly 50 MB, not 100 MB.
