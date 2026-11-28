# CLI Manual: `sentinel-ctl` (Edge Appliance Operator & Vault)

* **Binary:** `/usr/local/bin/sentinel-ctl`
* **Source:** `/home/kami/blackbox-sentinel/tools/{sentinel_ctl.cpp,sentinel_ctl/*.hpp}`
* **Duty:** Governs day-to-day edge appliance health, Hub authentication, content-addressable asset caching, cache-first dependency resolution, TPM 2.0 attestation, frontier security subsystems (`5g`, `sbom`, `trism`), scenario authoring, and bare-metal production blueprints.
* **Automated Test Suite:** `bash /home/kami/sentinel-stack/tests/cli_verification/03_test_sentinel_ctl_commands.sh` (**37/37 PASS**)

---

## 1. Authentication & Registry Identity

| Command | Duty & Mechanics |
| :--- | :--- |
| `sentinel-ctl login --jwt <JWT> [--hub-url <URL>]` | Exchanges a Hub JWT at `POST /api/v1/registry/tokens` for a 365-day scoped CLI API key (`packages:publish`, `packages:validate`), saves `credentials.json` to SSFS `ObjectClass::Config`, and verifies whether local `developer_private.pem` matches the Hub-enrolled `author_public_key`. |
| `sentinel-ctl whoami` | Displays active credentials path, truncated API key, enrolled 64-char hex Ed25519 author public key, and active Hub URL. |

> **URL Precedence:** `SENTINEL_HUB_URL` env var > `credentials.json` (`hub_url`) > `https://backend.aryorithm.com`.

---

## 2. Appliance Health, Hardware Root & Commercial Licensing

| Command | Duty & Mechanics |
| :--- | :--- |
| `sentinel-ctl status` | Audits five pillars: (1) License status (`/etc/sentinel/license.lic` or SSFS config), (2) Physical TPM 2.0 (`/dev/tpmrm0` / `/dev/tpm0`) vs. DMI UUID fallback, (3) Pinned eBPF maps (`/sys/fs/bpf/blackbox_blocked_ips`), (4) Central cache & active Tier A/B/C extension counts, (5) Active `model_routes.yaml` DAG path. |
| `sentinel-ctl hardware status` | Queries `TpmEnrollmentManager` for architecture profile, TPM device path, DMI system UUID, hardware token hash, and silicon binding verification. |
| `sudo sentinel-ctl hardware enroll` | Generates and persists the silicon-bound hardware token to `/etc/sentinel/hardware_identity.token`. |
| `sentinel-ctl license inspect <file.lic>` | Prints file size and commercial entitlement metadata. |
| `sentinel-ctl license apply <file.lic>` | Installs license to `/etc/sentinel/license.lic` (when `UID == 0`) or SSFS `Config/license.lic` (non-root). |
| `sentinel-ctl appliance pull <slug>` | Downloads an official sealed `.aryopack` release from `GET /api/v1/hub/appliances/{slug}/download`. |

---

## 3. Cache-First Dependency Resolution & Runtime Deployment

| Command | Duty & Mechanics |
| :--- | :--- |
| `sentinel-ctl check [routes.yaml]` | Parses `package_id` and `model_id` entries from `model_routes.yaml` and verifies all required `.spkg` and `.onnx` assets resolve locally or from cache without mutating runtime directories. |
| `sentinel-ctl sync [routes.yaml]` | Resolves every dependency (Cache Hit -> local SSFS fallback -> Hub canonical download `/hub/assets/{type}/{slug}/download` -> root alias fallback) and installs `.spkg` + `.onnx` into active runtime directories. |
| `sentinel-ctl launch [routes.yaml]` | Executes `sync` and, if 100% of dependencies resolve, launches `sudo ./build/sentinel --routes <routes.yaml>`. |
| `sentinel-ctl install <file.spkg>` *(or `appliance install`)* | Verifies the 4-way SHA-256 Merkle Ed25519 signature (Tier 1: Official Authority Root CA -> Tier 2: Embedded `author_public_key`) and extracts the payload into `plugins.d/*.so` (Tier 0), `wasm.d/*.wasm` (Tier 1), or `rules.d/*.lua` (Tier 2) under `/etc/sentinel/` (root) or SSFS `SpkgInstalled` (non-root). |

---

## 4. Content-Addressable Cache & Air-Gapped USB Sneakernet

Cache root is resolved via `SENTINEL_CACHE_DIR` or SSFS `ObjectClass::ArtifactDownload`.

| Command | Duty |
| :--- | :--- |
| `sentinel-ctl cache list` | Recursively lists all cached files, categories, and total KB footprint. |
| `sentinel-ctl cache search <query> [--type <cat>]` | Filters cached files by filename substring and asset category (`packages`, `models`, `datasets`, `pcaps`, `scenarios`, `blueprints`). |
| `sentinel-ctl cache export <out.tar.gz>` | Archives the entire cache directory into a portable sneakernet tarball. |
| `sentinel-ctl cache import <in.tar.gz>` | Restores a sneakernet tarball into the local cache root. |
| `sentinel-ctl cache clean` | Recursively purges the local cache directory. |

---

## 5. Global Hub Discovery & Symmetrical Asset Vaults

| Command | Duty & REST Endpoint |
| :--- | :--- |
| `sentinel-ctl hub search [query] [--type <t>]` / `hub list` | Queries `GET /api/v1/hub/search?q=...&type=...` (falls back gracefully to verified offline reference catalog when air-gapped). |
| `sentinel-ctl hub info <type> <slug>` | Previews cloud manifest URL, cryptographic root, and compliance invariants without downloading. |
| `sentinel-ctl hub visibility <type> <slug> [public\|private]` | Toggles asset visibility via `PUT /api/v1/hub/assets/{type}/{slug}/visibility`. *(Alias: `package visibility <slug> [mode]`)* |
| `sentinel-ctl hub yank <type> <slug>` | Permanently deletes/yanks an asset via `DELETE /api/v1/hub/assets/{type}/{slug}`. |
| `sentinel-ctl package pull <slug>` / `package list` | Pulls & installs `.spkg` / Lists cached `.spkg` and active Tier A/B/C runtime plugins. |
| `sentinel-ctl model pack <m.onnx> [--precision INT8\|FP32] [--domain <d>]` | Auto-detects INT8 from filename and writes `manifest.json` + `<m.onnx>.manifest.json` ready for `aryo publish`. |
| `sentinel-ctl model pull <slug>` / `model list` | Stages `.onnx` into SSFS `ModelRegistry` / Lists cached and staged models. |
| `sentinel-ctl dataset pull <slug>` / `dataset list` | Stages `.slab` into SSFS `ArtifactDownload/datasets` / Lists cached and staged datasets. |
| `sentinel-ctl slab stream <file.slab> [port]` | Streams 144-byte zero-copy binary SLAB records over UDP to `127.0.0.1:<port>` (default `9999`) and reports achieved EPS. |
| `sentinel-ctl pcap pack <f.pcap> [--category <c>] [--protocol <p>] [--attack <a>]` | Generates Hub companion manifests (`manifest.json` + `<f>.manifest.json`) for raw PCAP uploads. |
| `sentinel-ctl pcap pull <slug>` / `pcap list` | Stages `.pcap` into SSFS `ArtifactPcap` / Lists cached and staged captures. |

---

## 6. Frontier Security Engines (`5g`, `sbom`, `trism`, `threat`)

| Subsystem | Commands | Duty & Behavior |
| :--- | :--- | :--- |
| **5G/6G Slicing** | `5g enable [iface] [cfg.yaml]`<br>`5g status` | Provisions URLLC (TEID `0x00000100`, ports 502/102/2404) & eMBB (TEID `0x00000200`) slices and reports in-kernel `< 0.84 µs` drop counters. |
| **Live-SBOM W^X** | `sbom generate`<br>`sbom enforce`<br>`sbom status`<br>`sbom test-drift`<br>`sbom drift-events [--limit N]` | Computes SHA-256 & inode CycloneDX 1.6 manifest (`live_sbom.json`) across core binaries/libs, enrolls running daemons, tests anonymous `mmap` + `mprotect(PROT_EXEC)` interception in a forked child, and queries `GET /api/v1/compliance/sbom/drift-events`. |
| **AI TRiSM** | `trism status`<br>`trism inspect --prompt "<text>"`<br>`trism test-jailbreak`<br>`trism policy [show\|pull\|push] [path]` | Inspects LLM prompts via `TrismFirewall` (**exit `0` = PERMIT**, **exit `1` = DROP**), executes the 5-vector red-team suite, and syncs/pushes fleet policy via `GET`/`PUT /api/v1/ai/trism/policy`. |
| **Collective Defense** | `threat vaccine-share <file.spkg>`<br>`threat vaccine-feed [limit]` | Uploads synthesized `.spkg` vaccine via `POST /api/v1/threats/vaccines/share` and queries live fleet vaccines via `GET /api/v1/threats/vaccines/feed`. |

---

## 7. Scenarios & Production Site Blueprints

### Scenario Authoring (`sentinel-ctl scenario ...`)
* `scenario new <name> [--sector <s>]`: Scaffolds `manifest.json`, `scenario.yaml`, `configs/plc_register_map.json`, and `run_demo.sh` inside SSFS `ScenarioCatalog`.
* `scenario add <dir|slug> <asset> [--embed]`: Resolves an asset from disk, SSFS stores, runtime, or cache; registers it in `manifest.json` (and copies binary when `--embed` is set).
* `scenario pack <dir|slug> [out.tar.gz] [--embed]`: Packs either a lightweight declarative bundle (~15 KB, excluding `.spkg`/`.onnx`) or an air-gapped `--embed` standalone tarball.
* `scenario pull <slug>` / `scenario list`: Pulls and unpacks a Hub scenario into SSFS `ScenarioCatalog` / Lists cached archives and staged catalog entries.

### Production Site Blueprints (`sentinel-ctl blueprint ...`)
* `blueprint new <name> [--site <s>]`: Scaffolds `manifest.json`, `blueprint.yaml` (NIC, AF_XDP mode, RSS queues, CPU affinity, TPM requirement), `model_routes.yaml` (4-stage DAG), and `deploy.sh`.
* `blueprint add <dir> <asset> [--embed]`: Registers (and optionally embeds) `.spkg` or `.onnx` dependencies.
* `blueprint pack <dir> [out.blueprint] [--embed]`: Archives directory into `.blueprint` + companion manifest.
* `blueprint inspect <file|dir>`: Displays `blueprint.yaml` hardware bindings and `manifest.json` (or `tar -tf` for archives).
* `sudo blueprint deploy <file|dir>`: Requires root. Backs up `/etc/sentinel/model_routes.yaml` to `/etc/sentinel/.blueprint_backup/`, installs `.spkg` rules, stages `.onnx` models & configs, and sends `SIGHUP` to `/usr/local/bin/sentinel` for zero-downtime `< 2 ms` RCU pointer swap.
* `sudo blueprint rollback`: Restores `/etc/sentinel/.blueprint_backup/model_routes.yaml` and triggers `SIGHUP` RCU swap.
* `blueprint pull <slug>` / `blueprint list` / `blueprint raw-dag <slug>`: Downloads `.blueprint` from Hub, lists cached/active blueprints, or streams raw 4-stage YAML from `GET /api/v1/hub/blueprints/{slug}/raw-dag`.
* `blueprint from-scenario <path|slug> [--site S] [--interface NIC] [--af-xdp MODE] [--arch ARCH] [--no-pack]`: Automatically converts a validated digital twin scenario into a bare-metal production blueprint directory (migrating `.spkg`, `.onnx`, `configs/`, synthesizing `blueprint.yaml` + `model_routes.yaml`) and auto-packs `.blueprint`.
