# CLI Manual: `sentinel-matrix` (Digital Twin & Sensor Chaos)

* **Directory:** `/home/kami/sentinel-matrix/`
* **Tools:** `tools/scenario_engine.py`, `tools/sensor_ctl.py`, `tools/matrix_ctl.sh`, `Makefile`
* **Duty:** Compiles declarative `scenario.yaml` topologies into isolated Docker Compose digital twin networks (anchored via Tier 0 `sentinel_fs` `pack://` URIs), catalogs and injects real-time physical chaos across 570 industrial sensors, and replays malware PCAPs at wire rate.
* **Automated Test Suite:** `bash /home/kami/sentinel-stack/tests/cli_verification/04_test_sentinel_matrix_commands.sh` (**9/9 PASS**)

---

## 1. Universal Scenario Compiler & Orchestrator (`scenario_engine.py`)

Invoked directly via `python3 /home/kami/sentinel-matrix/tools/scenario_engine.py` or through `aryo scenario up|down` and `aryo matrix scenario load|down|status`.

| Command | Duty & SSFS Mechanics |
| :--- | :--- |
| `scenario_engine.py load <target>` | Resolves `<target>` (SSFS catalog slug, `.tar.gz`/`.tgz` archive, directory, or direct `.yaml`), translates symbolic `pack://` volume mounts via `SentinelPathResolver.resolve_pack_uri()`, writes `docker-compose.<name>.yml` into isolated SSFS `SCENARIO_WORKSPACE` (zero repo pollution), and launches `docker compose -p matrix_<name> up -d`. |
| `scenario_engine.py down [--name <slug>]` | Dismantles the specified scenario project (`--remove-orphans`) and removes its SSFS workspace. When `--name` is omitted, tears down **all** active scenario workspaces cleanly. |
| `scenario_engine.py status [--name <slug>]` | Displays running `matrix-*` containers, health status, port bindings, and attached Docker subnets. |

```bash
# Launch a cataloged scenario by slug (recommended umbrella form)
aryo scenario up 05_drinking_water_dosing_guard

# Inspect active containers and tear down cleanly
aryo matrix scenario status --name 05_drinking_water_dosing_guard
aryo scenario down 05_drinking_water_dosing_guard
```

---

## 2. 570-Sensor Industrial Catalog & Chaos Controller (`sensor_ctl.py`)

Invoked via `aryo sensor <action>` or `python3 /home/kami/sentinel-matrix/tools/sensor_ctl.py`. Reads YAML profiles from `/home/kami/sentinel-matrix/catalogs/sensors/` and injects live faults via HTTP POST to `http://localhost:8088/fault`.

| Command | Duty & Options |
| :--- | :--- |
| `aryo sensor list [--category <C>] [--search <Q>] [--domain <ID>] [--limit <N>]` | Renders a 120-column numerically sorted table (`#001`–`#570`) showing sensor name, category, default Modbus port, interface, and physics ODE engine. |
| `aryo sensor inspect <sensor_id>` | Displays vendor, wire protocol, physics engine, baseline value, noise sigma, Modbus holding register map, and available chaos fault hook IDs. Supports partial substring matching. |
| `aryo sensor fault <sensor_id> <action> [value]` | Sends a live JSON chaos payload `{"sensor_id", "action", "value"}` to the running Sensor Multiplexer (`:8088/fault`). |

```bash
# Search for pressure sensors and inspect the first match
aryo sensor list --search pressure --limit 10
aryo sensor inspect s052

# Inject a live water-hammer pressure spike into a running digital twin
aryo sensor fault siemens_sitrans_p320 step_increase 8.5
```

---

## 3. Cyber-Range Helper (`matrix_ctl.sh`) & `Makefile` Targets

### `tools/matrix_ctl.sh`
| Command | Duty |
| :--- | :--- |
| `matrix_ctl.sh status` | Lists active containers on `matrix-net` (`10.240.0.0/24`). |
| `matrix_ctl.sh sync-pcaps` | Pulls certified PCAPs from Hub via `make sync-hub-pcaps`. |
| `matrix_ctl.sh scenario <name>` | Pulls and unpacks a named digital twin scenario. |
| `matrix_ctl.sh replay <pcap_name>` | Replays `shared/datasets/<pcap_name>` at wire rate via `tcpreplay` inside `matrix-traffic-gen` (or host loopback fallback). |

### `sentinel-matrix/Makefile` (also reachable via `aryo matrix <target>`)
| Target | Duty |
| :--- | :--- |
| `make init` | Syncs compiled `sentinel`, `sentinel-nexus`, `nexus-ctl`, shared libraries (`ldd`), web UI, and ONNX models into `shared/`. |
| `make build-device-runtime` | Builds `sentinel-matrix/device-runtime:latest` (universal parameterized PLC/RTU/IED container). |
| `make build-apparatus-runtime` | Builds `sentinel-matrix/apparatus-runtime:latest` (pluggable dual-PCAP traffic/attack generator). |
| `make scenario-up [SCENARIO=<path>]` | Compiles and launches a scenario via `scenario_engine.py load`. |
| `make scenario-down [NAME=<slug>]` | Dismantles active scenario(s) via `scenario_engine.py down`. |
| `make scenario-status [NAME=<slug>]` | Displays running scenario containers. |
| `make scenario-pack NAME=<folder> [EMBED=1]` | Delegates to `aryo scenario pack`. |
| `make port-clean` | Releases occupied C2/twin ports (`9443`, `9444`, `50051`, `15501`, `15502`, `8554`, `8889`). |
| `make fix-docker` | Resets AppArmor profiles, restarts `containerd`/`docker`, and removes stale `matrix-*` containers. |
| `make clean` | Purges temporary datasets and logs in `shared/`. |
