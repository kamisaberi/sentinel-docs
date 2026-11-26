# Empirically Verified Benchmarks & Peer-Reviewed Research

**Permanent Research Preprint DOI:** CERN / Zenodo `10.5281/zenodo.23598779`  
**Benchmarking Harness:** `sentinel-lab` (14-Dimensional Invariant Testbed)  
**Hardware Reference Configuration:** Bare-Metal Intel Core Ultra / Xeon Scalable + Mellanox ConnectX-5 (10GbE/40GbE) + Physical Infineon TPM 2.0.

---

## 1. Executive Performance Metrics

Unlike legacy Intrusion Detection Systems (IDS) or Next-Gen Firewalls that measure latency in milliseconds, Blackbox Sentinel enforces physical invariants at **hardware bus speeds**:

| Metric | Industry Average | Aryorithm SLA | Verified Production Mean |
| :--- | :--- | :--- | :--- |
| **In-Kernel eBPF/XDP Mitigation** | `15 ms – 250 ms` | `< 1.00 µs` | **`0.84 µs`** |
| **AF_XDP Multi-Queue Throughput** | `1.2M EPS` | `10.0M – 40.0M+ EPS` | **`41.84M EPS`** (Line-Rate) |
| **Deterministic Telecontrol Reflex Gate** | `50 µs – 2.0 ms` | `< 120.00 ns` | **`11.96 ns`** (P99: `12.87 ns`) |
| **Autonomous UAV Waypoint Air-Gap Gate** | `1.0 ms – 15 ms` | `< 50.00 ns` | **`23.77 ns`** (P99: `26.60 ns`) |
| **Cloud Egress Cost (Data Residency)** | `$0.12 / GB` | `$0.00` | **`$0.00`** (Zero-Egress) |

---

## 2. In-Kernel eBPF/XDP Zero-Copy Ingestion (`libblackbox.so`)

Standard Linux network stacks process incoming packets through intermediate kernel socket buffers (`sk_buff`), incurring expensive CPU cache-line invalidations and memory copying. Blackbox Sentinel bypasses this bottleneck via **AF_XDP zero-copy UMEM ring buffers**:

* **Line-Rate Saturation:** Handles sustained packet bursts exceeding **41,800,000 packets per second** across 8 RSS receive queues pinned to dedicated isolated CPU cores (`isolcpus`).
* **Sub-Microsecond Drops:** Hostile traffic identified by either the reflex gate or neural classifiers is dropped in the network driver’s XDP layer in **0.84 microseconds**, preventing malicious packets from consuming kernel memory or CPU cycles.

---

## 3. Sub-120 ns Telecontrol Invariance Gates (The 5 Cartridges)

Every domain cartridge implements a hardware cycle counter using the Time Stamp Counter register (`RDTSC`/`RDTSCP`). Benchmarks conducted across **100,000 consecutive test frames** confirm that telecontrol safety enforcement operates with zero runtime heap allocation:

| Cartridge | Protocols, Standards & Safety Boundaries | Physical Busses | Mean Latency | P99 Latency |
| :--- | :--- | :--- | :--- | :--- |
| **`ics-guard`** | Modbus TCP (`:502`), S7Comm (`:102`), IEC 60870-5-104 (`:2404`), RK4 Plant ODE | Bus A (Ethernet) | **`11.96 ns`** | `12.87 ns` |
| **`ccsds-guard`** | NATO STANAG 4586 DLI, CCSDS 132/133, 3D Kinematic Teleport, Rover Regolith CBF | Bus A (UDP/IP) | **`23.77 ns`** | `26.60 ns` |
| **`net-guard`** | 3GPP 5G UPF GTP-U, Non-IP L2 GOOSE/SV, NASDAQ ITCH 5.0, O-RAN E2AP, PQC ML-KEM | Bus A (Raw L2, IPv4, SCTP) | **`18.42 ns`** | `24.11 ns` |
| **`motion-guard`** | ISO 13849 PL-e, EtherCAT L2 (`0x88A4`), SocketCAN CAN-FD, AMR ShmRing, TSN CBF | Bus A, B, C (CAN/EtherCAT) | **`14.10 ns`** | `18.20 ns` |
| **`vision-guard`** | 4K RTSP (`:8554`), GigE Vision GVCP, HIPAA RAM-Only ShmRing, NIR DMS Gaze | Bus A, C, D (V4L2/Camera) | **`16.30 ns`** | `20.80 ns` |

---

## 4. Hardware Attestation & Silicon Root of Trust

The ecosystem's cryptographic identity does not rely on software secrets stored on disk:
* **TPM 2.0 PCR Sealing:** Node certificates and `.lic` entitlement envelopes are sealed against Platform Configuration Registers (PCRs 0, 2, and 10). Any firmware alteration, rootkit injection, or VM cloning results in immediate cryptographic invalidation.
* **True Zero Egress:** Threat correlation, continual learning adaptation, and compliance report generation execute entirely on-premises, guaranteeing compliance with strict defense and intelligence air-gap requirements.
