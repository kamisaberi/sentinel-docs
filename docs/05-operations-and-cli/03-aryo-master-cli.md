# CLI Manual: `aryo` (Master Umbrella CLI v2.5.0)

* **Binary:** `/usr/local/bin/aryo`
* **Source:** `/home/kami/sentinel-stack/src/{aryo.cpp,common.hpp,help_manuals.hpp,domain_router.hpp}`
* **Duty:** Single pane of glass for the entire Aryorithm ecosystem. Parses `<domain> <action> [args]` and delegates execution to specialized Tier 1–4 binaries, `systemd`, research harnesses, and dynamically discovered `aryo-*` cartridge plugins.
* **Automated Test Suite:** `bash /home/kami/sentinel-stack/tests/cli_verification/01_test_aryo_commands.sh` (**33/33 PASS**)

---

## 1. Global Flags

| Command | Duty |
| :--- | :--- |
| `aryo` / `aryo --help` / `aryo -h` / `aryo help` | Display all 18 core domains, the 5 platform cartridges, supported multi-bus ingress cores, and all dynamically discovered `aryo-*` plugins. |
| `aryo --version` / `aryo -v` / `aryo version` | Display the ASCII banner, version (`v2.5.0`), corporate URL, and Hub backend URL. |
| `aryo <domain> --help` | Display the built-in operational manual and copy-paste examples for any domain. |

---

## 2. Complete Domain-to-Binary Delegation Map

| Domain | Subcommands / Actions | Delegated Target | Primary Duty |
| :--- | :--- | :--- | :--- |
| **`login` / `whoami`** | `login --jwt <T> [--hub-url <U>]`, `whoami` | `sentinel-ctl` | Authenticate CLI against Registry Hub and inspect active credentials. |
| **`auth`** | `login`, `register`, `status`, `update-key` | `nexus-ctl` | Fleet C2 identity & key management against `sentinel-nexus`. |
| **`status`** | *(none)* | `sentinel-ctl status` | Full appliance health audit (license, TPM 2.0, eBPF maps, cache, extensions, DAG). |
| **`appliance`** | `sync`, `check`, `launch`, `install`, `pull` | `sentinel-ctl` | Dependency resolution, `.spkg` deployment, daemon launch, and `.aryopack` pull. |
| **`hardware` / `license`** | `hardware status\|enroll`, `license apply\|inspect` | `sentinel-ctl` | Physical TPM 2.0 silicon attestation and commercial license enforcement. |
| **`stack`** | `install`, `build`, `verify`, `uninstall`, `purge`, `env` | `sentinel-stack/*.sh` | Master 7-phase installation, DAG build, 30-point verification, and host env audit. |
| **`service`** | `start\|stop\|restart\|status\|logs [sentinel\|nexus\|all] [-f]` | `systemctl` / `journalctl` | Manage `blackbox-sentinel` and `sentinel-nexus` systemd daemons. |
| **`hub`** | `search`, `list`, `info`, `visibility`, `yank` | `sentinel-ctl` | Cloud Hub discovery, visibility toggling, and asset yanking. |
| **`hub`** | `broadcast <file.spkg>`, `new` | `nexus-ctl` | Sub-50ms gRPC fleet-wide `.spkg` broadcast. |
| **`publish`** | `publish <file> [--token <K>] [--hub-url <U>]` | `sentinel-artifact` | Sign and publish any of the 6 supported asset classes to Hub. |
| **`visibility`** | `visibility <type> <slug> [public\|private]` | `sentinel-ctl hub visibility` | Shortcut to promote or demote a published Hub asset's visibility. |
| **`sensor`** | `list [--category\|--search\|--domain\|--limit]`, `inspect <id>`, `fault <id> <act> [val]` | `sentinel-matrix/tools/sensor_ctl.py` | Query the 570-sensor industrial catalog and inject live `:8088` chaos faults. |
| **`package` / `artifact`** | `new`, `keygen`, `pack`, `inspect`, `verify`, `test`, `extract-source`, `synthesize-vaccine` | `sentinel-artifact` | Developer SDK authoring, cryptographic sealing, audit, and vaccine synthesis. |
| **`package` / `artifact`** | `pull <slug>`, `list`, `visibility` | `sentinel-ctl package` | Pull verified `.spkg` from Hub/cache and list active Tier A/B/C runtime plugins. |
| **`model` / `dataset` / `pcap`** | `pack`, `pull`, `list` | `sentinel-ctl` | Manage local vaults and companion manifests for `.onnx`, `.slab`, and `.pcap` assets. |
| **`scenario`** | `list-recipes`, `provision <recipe> [--up]` | `sentinel-stack/scenarios/scripts/*.sh` | Enumerate and provision all 50 real-world scenario recipes with CAS deduplication. |
| **`scenario`** | `up <slug>`, `down <slug>` | `sentinel-matrix/tools/scenario_engine.py` | Compile and launch/teardown isolated Docker Compose scenario topologies. |
| **`scenario`** | `new`, `add`, `pack`, `pull`, `list` | `sentinel-ctl scenario` | Author custom scenario bundles and manage the SSFS scenario catalog. |
| **`fleet` / `ota` / `report`** | `fleet list\|vaccine-audit`, `ota status\|stage\|advance\|rollback`, `report cmmc\|scada\|nis2` | `nexus-ctl` | Sovereign fleet C2, canary OTA model rollouts, and regulatory compliance exports. |
| **`threat`** | `drop <IP>` | `nexus-ctl` | Instant sub-50ms fleet-wide eBPF IP drop broadcast. |
| **`threat`** | `vaccine-share <file>`, `vaccine-feed [limit]` | `sentinel-ctl threat` | Share synthesized `.spkg` vaccines to the collective feed and inspect live vaccines. |
| **`forge`** | `run [--remote]`, `quantize`, `finetune` | `forge-cli` | Continual learning (Tabular MAE + InfoNCE) and INT8 PTQ quantization. |
| **`slab`** | `convert`, `verify` | `sentinel-artifact slab` | Convert CSV to `0x534C4142` binary SLAB and validate integrity. |
| **`slab`** | `stream <file.slab> [port]` | `sentinel-ctl slab stream` | Blast zero-copy binary SLAB records over UDP at 65k+ EPS. |
| **`lab`** | `daemon` + 23 core modules + dynamic harnesses | `sentinel_lab` / Python venv | 14-dimensional scientific testbed (RK4 ODEs, CBFs, FDIA, PQC, fuzzing). |
| **`matrix`** | `plc`, `honeynet-autohunt`, `scenario load\|down\|status`, `sim-finetune`, `attack <name>`, `up\|down\|status\|tui` | `mock_plc` / `scenario_engine.py` / `Makefile` | Digital twin range mesh orchestration and autonomous honeynet loop. |
| **`cache`** | `list`, `search`, `clean`, `export`, `import` | `sentinel-ctl cache` | Local asset cache inspection and offline USB sneakernet bundling. |
| **`system`** | `export [out.aryopack]`, `import <in.aryopack>` | `sentinel-stack/scripts/{export,import}_system.sh` | Standalone zero-dependency air-gapped full-ecosystem bundle export/restore. |
| **`5g`** | `blast-test [iface]` | `gtp_slice_blaster.py` | Synthetic 3GPP 5G GTP-U slice-hopping attack drill. |
| **`5g`** | `enable <iface> [cfg]`, `status` | `sentinel-ctl 5g` | Provision and inspect in-kernel 5G N3 GTP-U network slice isolation. |
| **`sbom`** | `generate`, `enforce`, `status`, `test-drift`, `attest`, `drift-events` | `sentinel-ctl sbom` | Live-SBOM runtime memory integrity and `< 1.0 µs` W^X `SIGKILL` defense. |
| **`space`** | `status`, `ccsds`, `blast-sim` | `ccsds-guard` / `space_link_blaster.py` | CCSDS 133 / NATO STANAG 4586 orbital telemetry audit and link simulation. |
| **`trism`** | `status`, `inspect`, `test-jailbreak`, `policy [show\|pull\|push]` | `sentinel-ctl trism` | Inline GenAI / LLM prompt injection firewall and tool-calling governor. |
| **`blueprint`** | `publish <file.blueprint>` | `sentinel-artifact publish` | Publish a production site blueprint to `/api/v1/hub/blueprints/publish`. |
| **`blueprint`** | `new`, `add`, `pack`, `inspect`, `deploy`, `rollback`, `pull`, `list`, `raw-dag`, `from-scenario` | `sentinel-ctl blueprint` | Physical edge appliance blueprint authoring and atomic `< 2 ms` RCU deployment. |

---

## 3. Dynamic Tier-2 Platform Cartridge Plugins (`aryo-<domain>`)

When an unrecognized domain `<d>` is passed, `aryo` scans `/usr/local/bin`, `/usr/bin`, and `/etc/sentinel/plugins` for an executable named `aryo-<d>`. All five production cartridges register automatically:

| Command | Binary | Protected Domain & SLA |
| :--- | :--- | :--- |
| `aryo ics <action>` | `/usr/local/bin/aryo-ics` | Modbus TCP, S7Comm, IEC-104, IEEE C37.118 PMU, RK4 ODE + Nagumo CBF (`11.96 ns` mean). |
| `aryo aerospace <action>` | `/usr/local/bin/aryo-aerospace` | STANAG 4586 DLI, CCSDS 132/133, 3D Teleport, Planetary Rover Slip CBF (`23.77 ns` mean). |
| `aryo net <action>` | `/usr/local/bin/aryo-net` | 3GPP 5G UPF GTP-U, Non-IP L2 GOOSE/SV, NASDAQ ITCH 5.0, O-RAN E2AP, FIPS 203 ML-KEM (`18.42 ns` mean). |
| `aryo motion <action>` | `/usr/local/bin/aryo-motion` | ISO 13849 PL-e, EtherCAT L2 (`0x88A4`), CAN-FD, AMR ShmRing, Surgical TSN (`14.10 ns` mean). |
| `aryo vision <action>` | `/usr/local/bin/aryo-vision` | Air-gapped 4K RTSP, GigE Vision GVCP, HIPAA RAM-only ShmRing (`VIS1`), NIR DMS PERCLOS (`16.30 ns` mean). |

---

## 4. `aryo lab` Scientific Research Modules

`aryo lab <action> [args]` resolves `/opt/sentinel-stack/venv/bin/python3` and dispatches either to the native C++20 `sentinel_lab` daemon, one of the 23 built-in harnesses, or any dynamically discovered Python harness in `/etc/sentinel/lab/harnesses`, `/usr/local/share/sentinel/lab/harnesses`, or `ccsds-guard/harnesses`:

* **Core C++ & Simulation:** `daemon`, `inspect-matrix`, `blast`, `evasion`, `drift`, `hil`, `fuzzer`, `fdia`, `quant`, `pqc`, `stateful`, `sidechannel`, `cbf`, `federated`, `patch-regression`.
* **Physical Domain Audits:** `sensor-audit`, `rf-sdr`, `acoustic-tdoa`, `fluid-shock`, `space-avionics`, `quantum-metrology`, `power-grid`, `chemical-gas`, `fab-extreme`.
* **Dynamic Cartridge Harnesses:** `ics-*`, `uav-*`, `net-*`, `motion-*`, `vision-*` (auto-discovered via `resolve_dynamic_lab_harness()`).

```bash
# Example: Run a 60-second closed-loop RK4 ODE hardware-in-the-loop audit
aryo lab hil --duration 60

# Example: Run an Industroyer2 IEC-104 breaker trip evaluation
aryo lab ics-iec104-trip
```
