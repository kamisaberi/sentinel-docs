# Master CLI Reference Manual (`aryo`, `sentinel-ctl`, `sfs`)

The Aryorithm toolchain unifies command-line operations across three dedicated utilities, bridging low-level filesystem management, appliance administration, and high-level fleet orchestration.

---

## 1. The Master Ecosystem CLI: `aryo`

The `aryo` binary (`/usr/local/bin/aryo`) is the primary operations interface, dynamically routing commands to domain cartridges, simulation engines, and provisioning scripts.

```bash
# General Syntax
aryo <domain|subsystem> <action> [arguments]
```

### Core Subcommands
* **Cartridge Execution:**
  * `aryo ics (bench, verify-modbus, verify-s7, verify-iec104, grid-up)`
  * `aryo aerospace (bench, verify-stanag, verify-ccsds, sim-swarm)`
  * `aryo net (bench, verify-gtpu, verify-goose, verify-itch, telco-up)`
  * `aryo motion (bench, verify-ethercat, verify-can, verify-shm, cobot-up)`
  * `aryo vision (bench, verify-shm, verify-rtsp, verify-gige, vision-up)`
* **Digital Twin Scenarios:**
  * `aryo scenario list-recipes`: Enumerate all 50 turnkey real-world recipes.
  * `aryo scenario provision <slug> [--up]`: Download assets, calibrate ONNX autoencoders, stage FHS directories, and optionally launch.
  * `aryo scenario up <slug>` / `aryo scenario down <slug>`: Deterministic container orchestration.
* **Scientific Research (`sentinel-lab`):**
  * `aryo lab <module> --attack <slug>`: Execute 14-D hardware-in-the-loop physics evaluation.

---

## 2. Appliance & Registry CLI: `sentinel-ctl`

The `sentinel-ctl` utility (`/usr/local/bin/sentinel-ctl`) manages local node security, TPM attestation, and artifact packaging.

```bash
# Node Health & Hardware Attestation
sentinel-ctl status
sentinel-ctl hardware status
sudo sentinel-ctl hardware enroll

# Extension & Package Administration
sentinel-ctl package list
sentinel-ctl scenario list

# Cryptographic Identity & Hub Login
sentinel-ctl login --jwt <TOKEN>
sentinel-ctl whoami
```

---

## 3. Sovereign Filesystem Diagnostic Utility: `sfs`

Compiled from Tier 0 `sentinel-fs`, `sfs` (`/usr/local/bin/sfs`) verifies path containment and Content-Addressable Storage (CAS) integrity.

```bash
# Initialize Canonical Directory Tree
sfs init

# Display Authoritative Anchor Roots
sfs status

# Resolve Symbolic Cartridge URIs
sfs resolve pack://ics-guard/web

# Compute OpenSSL EVP SHA-256 Digest
sfs cas-hash <path-to-binary>
```
