# Domain Cartridges Architecture & Portfolio Overview

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
