#!/usr/bin/env python3
import pathlib

DOCS = pathlib.Path("/home/kami/sentinel-docs/docs")

files = {}

# ------------------------------------------------------------------------------
# 1. 03-developer-and-sdk/02-cartridge-and-plugin-sdk.md
# ------------------------------------------------------------------------------
files["03-developer-and-sdk/02-cartridge-and-plugin-sdk.md"] = """# Cartridge & 3-Tier Plugin SDK Specification

Every domain cartridge exposes a modular dissector interface dynamically ingested by `blackbox-sentinel`'s `PluginSupervisor`.

---

## 1. The 3 Extensibility Tiers

| Tier | Language / Engine | Binary Extension | Mean SLA | Primary Operational Scope |
| :--- | :--- | :--- | :--- | :--- |
| **Tier A** | Native C++20 | `.so` | `< 120 ns` | Deterministic line-rate protocol gates |
| **Tier B** | Rust Wasm3 (`no_std`) | `.wasm` | `< 1.50 µs` | Memory-safe sandboxed third-party logic |
| **Tier C** | LuaJIT C-FFI | `.lua` | `< 450 ns` | Zero-downtime hot-reloadable rules |

---

## 2. Tier A: Native C++20 Dissector Contract

Native dissectors implement the `sentinel::sdk` C ABI, compiling with zero runtime heap allocation:

```cpp
#include <sentinel/sdk/plugin.hpp>

using namespace sentinel::sdk;

static SentinelDissectorResult custom_dissect(const SentinelRawPacket* raw_pkt) {
    if (!raw_pkt || !raw_pkt->data || raw_pkt->length < 8) {
        return VerdictBuilder::Pass();
    }

    // Constant-time inspect bytes
    if (raw_pkt->data[7] == 0x05) { // e.g., Modbus Write Single Coil
        return VerdictBuilder::Drop(9001, "UNAUTHORIZED_COIL_WRITE").build();
    }
    return VerdictBuilder::Pass();
}

static SentinelPluginDescriptor g_descriptor = {
    SENTINEL_SDK_MAGIC,
    SENTINEL_SDK_VERSION_MAJOR,
    SENTINEL_SDK_VERSION_MINOR,
    SENTINEL_TIER_NATIVE_CPP,
    "org.aryorithm.package.custom_guard",
    "custom_guard",
    "1.0.0",
    "CUSTOM",
    502,
    0,
    nullptr,
    nullptr,
    custom_dissect
};

SENTINEL_REGISTER_PLUGIN(g_descriptor)
```

Dissectors are compiled to shared objects and deployed to `/usr/local/lib/blackbox/` or SSFS `${SENTINEL_ROOT}/spkg/installed/<cartridge>/`.
"""

# ------------------------------------------------------------------------------
# 2. 03-developer-and-sdk/03-binary-formats-specification.md
# ------------------------------------------------------------------------------
files["03-developer-and-sdk/03-binary-formats-specification.md"] = """# Binary Formats Specification (.spkg, .slab, .blueprint, .aryopack)

Aryorithm enforces strict, packed binary container layouts across all offline artifact pipelines.

---

## 1. Sentinel Distribution Package (`.spkg`)

All cryptographic reflex rules and dissectors are encapsulated within a sealed `.spkg` container:

| Field | Type | Description |
| :--- | :--- | :--- |
| **magic** | `uint64_t` (8B) | Magic identifier: `0x474B50534F595241` (`ARYOSPKG`) |
| **version** | `uint32_t` (4B) | Container format version (current: `1`) |
| **tier** | `uint32_t` (4B) | Execution Tier: `0`=Native C++, `1`=Rust Wasm, `2`=LuaJIT |
| **signature** | `uint8_t[64]` (64B) | Ed25519 digital signature over 4-way Merkle hash |
| **manifest_len** | `uint32_t` (4B) | Byte length of UTF-8 JSON manifest metadata |
| **payload_len** | `uint64_t` (8B) | Byte length of compiled executable (`.so` / `.wasm`) |
| **source_len** | `uint64_t` (8B) | Byte length of embedded auditable source code |
| **test_vector_len** | `uint32_t` (4B) | Byte length of pre-flight validation frame (`.bin`) |
| **reserved** | `uint32_t` (4B) | Reserved for future silicon alignment flags |

The 64-byte Ed25519 signature is computed over a **4-way Merkle tree**:

$$\\text{MerkleRoot} = \\text{SHA256}(\\text{SHA256}(\\text{manifest}) \\parallel \\text{SHA256}(\\text{payload}) \\parallel \\text{SHA256}(\\text{source}) \\parallel \\text{SHA256}(\\text{test\\_vector}))$$

---

## 2. Sentinel Lab Research Dataset (`.slab`)

The `.slab` format is a zero-copy, binary streaming protocol designed for high-throughput packet replay and telemetry storage (`> 40M EPS`):

| Field | Type | Description |
| :--- | :--- | :--- |
| **magic** | `uint32_t` (4B) | Magic identifier: `0x534C4142` (`SLAB`, Big-Endian) |
| **event_id** | `uint32_t` (4B) | Monotonically increasing event sequence identifier |
| **ground_truth** | `uint32_t` (4B) | Annotation label: `0`=Benign nominal, `1`=Hostile attack |
| **tensor_dim** | `uint32_t` (4B) | Feature dimension (e.g., 32, 64, or 128 float32s) |
| **features** | `float32[dim]` | Big-Endian IEEE-754 single-precision sensor readings |
"""

# ------------------------------------------------------------------------------
# 3. 04-domain-cartridges/00-cartridges-overview.md
# ------------------------------------------------------------------------------
files["04-domain-cartridges/00-cartridges-overview.md"] = """# Domain Cartridges Architecture & Portfolio Overview

Aryorithm decomposes cyber-physical threat mitigation into **five self-contained domain cartridges**, guaranteeing sub-120 ns verification across 50 industrial, defense, telecom, robotics, and edge vision verticals.

---

## 1. Architectural Cartridge Contract

Every cartridge complies with a strict structural and operational contract:

1. **Deterministic Core Library (`lib<cartridge>.so`):** Modern C++20 engine enforcing zero runtime heap allocations during telecontrol evaluation.
2. **Native Dissector Plugin (`<cartridge>_dissector_plugin.so`):** Ingested via `dlopen()` by `blackbox-sentinel` into Tier 1 of `ModelRouter`.
3. **Cartridge CLI Tool (`aryo-<domain>`):** Registered under `/usr/local/bin/` and dynamically commanded via `aryo <domain> ...`.
4. **Digital Twin Mesh:** Full Compose topology running on an isolated `/24` subnet with dedicated apparatus generators and mock field devices.
5. **Dynamic Web Micro-Frontend:** Mounted into `sentinel-nexus` via `pack://<cartridge>/web` and discovered through `/plugins/manifest.json`.

---

## 2. The 5 Production Cartridges

| Cartridge | Domain Scope | Primary Protocols | Physical Busses | SLA Benchmark | Twin Subnet |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`ics-guard`** | Industrial SCADA & Grid | Modbus TCP, S7Comm, IEC 60870-5-104, IEEE C37.118 | Bus A (Ethernet) | **11.96 ns** (P99: 12.87 ns) | `10.240.0.0/24` |
| **`ccsds-guard`** | Aerospace & UAV Swarms | NATO STANAG 4586, CCSDS 132/133, Rover Slip CBF | Bus A (UDP/IP) | **23.77 ns** (P99: 26.60 ns) | `10.240.52.0/24` |
| **`net-guard`** | 5G Telecom & FinTech | 3GPP GTP-U, Raw L2 GOOSE/SV, ITCH 5.0, PQC ML-KEM | Bus A (Raw L2/IP) | **18.42 ns** (P99: 24.11 ns) | `10.240.60.0/24` |
| **`motion-guard`** | Robotics & Motion Control | ISO 13849 PL-e, EtherCAT L2, CAN-FD, Surgical TSN | Bus A, B, C | **14.10 ns** (P99: 18.20 ns) | `10.240.70.0/24` |
| **`vision-guard`** | Air-Gapped Edge Vision | 4K RTSP, GigE Vision GVCP, HIPAA ShmRing, DMS | Bus A, C, D | **16.30 ns** (P99: 20.80 ns) | `10.240.80.0/24` |
"""

# ------------------------------------------------------------------------------
# 4. 04-domain-cartridges/01-ics-guard.md
# ------------------------------------------------------------------------------
files["04-domain-cartridges/01-ics-guard.md"] = """# Cartridge #1: `ics-guard` (Industrial SCADA & Energy Grid)

`ics-guard` delivers deterministic, sub-microsecond protection for critical industrial plants, electric substations, chemical reactors, and regional pipelines.

---

## 1. Specifications & Standards

* **Standards Compliance:** IEC 62443-4-2, IEC 60870-5-104, IEEE C37.118.2 PMU, EU NIS2.
* **Protocols Parsed:** Modbus TCP (`:502`), Siemens S7Comm (`:102`), IEC 60870-5-104 (`:2404`), IEEE C37.118 Synchrophasor (`:15501`).
* **Mean Latency:** **11.96 ns** (P99: 12.87 ns) under 100,000-frame hardware cycle benchmarks.
* **Digital Twin:** `scenarios/production_master_grid` (17 nodes on `10.240.0.0/24`, ports `:18093–18095`).

---

## 2. Mathematical Plant ODE & Control Barrier Function (CBF)

Beyond protocol syntax validation, `ics-guard` incorporates an embedded Runge-Kutta 4th-Order (RK4) ODE solver modeling plant thermal and kinetic dynamics:

$$\\dot{T} = \\frac{Q_{\\text{in}} - U \\cdot A \\cdot (T - T_{\\text{cool}})}{C_{\\text{thermal}}}$$

Physical safety invariance is enforced via a Nagumo barrier function:

$$h(T) = T_{\\text{critical}} - T \\ge 0$$

$$\\dot{h}(T) + \\gamma \\cdot h(T) \\ge 0$$

If incoming telemetry indicates that a setpoint change will breach the critical safety envelope within the critical clearing time ($t_{\\text{crit}} \\le 38.4\\text{ ms}$), the command is intercepted and dropped at line rate.
"""

# ------------------------------------------------------------------------------
# 5. 04-domain-cartridges/02-ccsds-guard.md
# ------------------------------------------------------------------------------
files["04-domain-cartridges/02-ccsds-guard.md"] = """# Cartridge #2: `ccsds-guard` (Aerospace & Autonomous UAV Swarms)

`ccsds-guard` protects autonomous drone swarms, defense datalinks, satellite downlinks, and planetary exploration rovers against telecommand hijacking and spoofing.

---

## 1. Specifications & Standards

* **Standards Compliance:** NATO STANAG 4586 (DLI), CCSDS 133.0-B-2 (Space Data Link Security), CCSDS 132.0-B-3.
* **Protocols Parsed:** STANAG 4586 DLI over UDP, CCSDS TC Frame, CCSDS Space Packet Protocol.
* **Mean Latency:** **23.77 ns** (P99: 26.60 ns) under 100,000-frame hardware cycle benchmarks.
* **Digital Twin:** `scenarios/tactical_uav_swarm_combat_grid` (6 nodes on `10.240.52.0/24`, ports `:18091–18092`).

---

## 2. Planetary Rover Regolith Slip & Rollover CBF (`rover_slip_cbf.hpp`)

`ccsds-guard` implements the Burckhardt granular regolith friction model $\\mu(\\lambda)$:

$$\\mu(\\lambda) = c_1 \\cdot (1 - e^{-c_2 \\lambda}) - c_3 \\lambda$$

It models continuous pitch and roll slope dynamics via Runge-Kutta 4th-order integration and clamps hostile drive telecommands using a Nagumo critical rollover barrier:

$$h_{\\text{tip}}(\\theta) = \\theta_{\\text{critical}} - \\|\\theta\\| \\ge 0$$

Telecommands that would cause rover wheel spinout on granular regolith or vehicle rollover on steep inclines are rejected in under 25 nanoseconds.
"""

# ------------------------------------------------------------------------------
# 6. 04-domain-cartridges/03-net-guard.md
# ------------------------------------------------------------------------------
files["04-domain-cartridges/03-net-guard.md"] = """# Cartridge #3: `net-guard` (5G Telecom & FinTech Infrastructure)

`net-guard` provides ultra-low latency filtering for 5G User Plane Functions (UPF), Open-RAN fronthaul/midhaul, non-IP Layer-2 substation buses, and high-frequency trading (HFT) feeds.

---

## 1. Specifications & Standards

* **Standards Compliance:** 3GPP Release 17 (TS 29.281 GTP-U), IEC 61850-8-1 (GOOSE), IEC 61850-9-2 (Sampled Values), O-RAN E2AP, NASDAQ ITCH 5.0, FIPS 203 (ML-KEM).
* **Protocols Parsed:** 3GPP GTP-U (`:2152`), Non-IP L2 GOOSE (`0x88B8`), Non-IP L2 SV (`0x88BA`), NASDAQ ITCH 5.0 (`:9001`), O-RAN E2AP (`:36422`).
* **Mean Latency:** **18.42 ns** (P99: 24.11 ns) under 100,000-frame hardware cycle benchmarks.
* **Digital Twin:** `scenarios/telco_5g_fintech_grid` (11 nodes on `10.240.60.0/24`, ports `:18096–18098`).

---

## 2. Post-Quantum Cryptography Engine (`pqc_kem_engine.hpp`)

`net-guard` incorporates native OpenSSL 3.5.5 FIPS 203 **ML-KEM-768** and **ML-KEM-1024** post-quantum key encapsulation mechanism (KEM) support:

* **Quantum Harvest-Now-Decrypt-Later Defense:** Enforces post-quantum cipher suites for control-plane TLS 1.3 handshakes.
* **Constant-Time Verification:** Rejects tampered ciphertexts with implicit rejection to prevent timing side-channel leakage.
"""

# ------------------------------------------------------------------------------
# 7. 04-domain-cartridges/04-motion-guard.md
# ------------------------------------------------------------------------------
files["04-domain-cartridges/04-motion-guard.md"] = """# Cartridge #4: `motion-guard` (Robotics & Time-Sensitive Networking)

`motion-guard` enforces deterministic physical safety invariants across industrial cobots, autonomous mobile robots (AMRs), automotive brake-by-wire buses, and telesurgery TSN networks.

---

## 1. Specifications & Standards

* **Standards Compliance:** ISO 13849-1 (PL-e Category 4), IEEE 802.1Qbv TSN, CiA 301 / CANopen, EtherCAT Specification.
* **Protocols & Busses:** Non-IP L2 EtherCAT (`0x88A4`) on Bus A, SocketCAN CAN-FD on Bus B, AMR ShmRing (`MOT1`) on Bus C.
* **Mean Latency:** **14.10 ns** (P99: 18.20 ns) under 100,000-frame hardware cycle benchmarks.
* **Digital Twin:** `scenarios/robotics_can_ethercat_grid` (8 nodes on `10.240.70.0/24`, ports `:18099–18101`).

---

## 2. Surgical Robotics TSN Jitter Clamp & Anatomical Keep-Out Zone (`surgical_tsn.hpp`)

`motion-guard` integrates a dedicated validator for high-precision robotic surgery:

* **TSN 802.1Qbv Jitter Enforcement:** Validates cycle arrival times using hardware PTP timestamps (`SO_TIMESTAMPING`), rejecting command packets with cycle jitter exceeding **500 microseconds**.
* **3D Anatomical Keep-Out Zone CBF:** Evaluates end-effector coordinates against patient anatomical scan keep-out zones (arteries, critical nerves):

$$h_{\\text{koz}}(x) = \\|p_{\\text{tip}} - p_{\\text{artery}}\\| - r_{\\text{safety}} \\ge 0$$

Commands commanding tool trajectories that breach the safety margin are clamped in under 15 nanoseconds.
"""

# ------------------------------------------------------------------------------
# 8. 04-domain-cartridges/05-vision-guard.md
# ------------------------------------------------------------------------------
files["04-domain-cartridges/05-vision-guard.md"] = """# Cartridge #5: `vision-guard` (Air-Gapped Optical Ingress & Privacy)

`vision-guard` protects air-gapped camera feeds, factory automation vision cameras, automotive driver monitoring sensors, and hospital surgical imaging streams.

---

## 1. Specifications & Standards

* **Standards Compliance:** HIPAA Security Rule (Zero Cloud Retention), ONVIF Profile S/T, GigE Vision 2.0 (GVCP/GVSP), Euro NCAP DMS 2026.
* **Protocols & Busses:** 4K RTSP (`:8554`) on Bus A, GVCP (`:3956`) on Bus A, HIPAA ShmRing (`VIS1`) on Bus C, V4L2 / MIPI-CSI2 on Bus D.
* **Mean Latency:** **16.30 ns** (P99: 20.80 ns) under 100,000-frame hardware cycle benchmarks.
* **Digital Twin:** `scenarios/vision_edge_grid` (8 nodes on `10.240.80.0/24`, ports `:18102–18104`).

---

## 2. Automotive In-Cabin DMS Gaze & Drowsiness Validator (`dms_gaze.hpp`)

`vision-guard` validates driver state directly from raw V4L2 camera buffers without requiring high-power external neural accelerators (< 5W envelope):

* **PERCLOS Metric:** Monitors percentage of eyelid closure over time.
* **Constant-Time $O(64)$ Strided Luma Inspection:** Evaluates illumination saturation directly on Bus D memory frames to detect optical blinding lasers or infrared dazzle attacks in real time.
"""

# Execute atomic disk writes with native newlines
for rel_path, content in files.items():
    dest = DOCS / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"✓ Re-instantiated with native newlines: {rel_path} ({len(content):,} B)")

print("\nAll 8 files regenerated successfully with 100% newline integrity.")
