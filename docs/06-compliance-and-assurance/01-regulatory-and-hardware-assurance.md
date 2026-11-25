# Statutory Compliance & Hardware Assurance Framework

Blackbox Sentinel bridges the gap between regulatory mandates and low-level kernel enforcement, auto-generating audit-ready attestation reports directly from `sentinel-nexus`.

---

## 1. EU NIS2 Directive (2022/2555) Compliance

`sentinel-nexus` implements continuous, dynamic assessment against Article 21 risk-management requirements:

* **Article 21(2)(a) — Risk Analysis & Asset Inventory:** Dynamically discovers all active sentries and policy routes (`GET /api/v1/fleet/nodes`).
* **Article 21(2)(b) — Incident Handling & Sub-ms Mitigation:** Proves that all hostile wire events are dropped in `< 0.84 µs` at the XDP driver level, with zero packet leakage into the host IP stack.
* **Article 21(2)(d) — Supply-Chain & Artifact Integrity:** Every `.spkg` package and ONNX neural model is cryptographically verified via Ed25519 Merkle roots and SHA-256 CAS indexing before execution.
* **Article 21(2)(h) — Cryptographic Hardware Attestation:** Every node identity is rooted in a physical Infineon/Nuvoton TPM 2.0 silicon chip.
* **Sovereignty Guarantee:** **`$0.00` Cloud Egress**. Telemetry and model adaptation execute entirely on-premises, satisfying strict European data residency mandates.

---

## 2. IEC 62443 Industrial Cybersecurity Standards
* **IEC 62443-3-3 / IEC 62443-4-2 (Foundational Requirements):**
  * **FR3 (System Integrity):** Embedded Nagumo Control Barrier Functions (CBFs) reject syntactically valid commands that would push physical plant dynamics into unsafe thermodynamic states.
  * **FR5 (Network Segmentation & Zone Isolation):** 5G network slicing and multi-bus ingress guarantee strict conduit isolation between safety-instrumented systems (SIS) and supervisory networks.

---

## 3. CMMC 2.0 & Defense Assurance
* **CMMC Level 2 (SI.L2-3.14.1 — Flaw Remediation):** In-kernel eBPF drop map updates occur in `< 50 ms` fleet-wide via `IocBroadcaster`.
* **In-Kernel W^X Enforcement (`live_sbom.o`):** Traps unauthorized `PROT_EXEC` memory transitions on running binaries (`sentinel`, `mock_plc`), delivering an instantaneous `SIGKILL` in `< 1.0 µs` to prevent fileless memory corruption exploits.
