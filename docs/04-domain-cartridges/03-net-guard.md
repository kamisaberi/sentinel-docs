# Cartridge #3: `net-guard` (5G Telecom & FinTech Infrastructure)

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
