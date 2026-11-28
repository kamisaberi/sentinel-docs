# CLI Manual: `sentinel-artifact` (Cryptographic SDK & Publisher)

* **Binary:** `/usr/local/bin/sentinel-artifact`
* **Source:** `/home/kami/blackbox-sentinel/tools/sdk/{sentinel_artifact.cpp,sentinel_artifact/*.hpp}`
* **Duty:** Developer SDK for scaffolding Tier A/B/C edge extensions, generating Ed25519 keys, sealing 4-way SHA-256 Merkle `.spkg` containers, running pre-flight threat assertions, converting/verifying `0x534C4142` SLAB datasets, sealing `.spcap` captures, synthesizing autonomous honeynet vaccines, and publishing all six asset classes to the Hub.
* **Automated Test Suite:** `bash /home/kami/sentinel-stack/tests/cli_verification/02_test_sentinel_artifact_commands.sh` (**16/16 PASS**)

---

## 1. Binary Container Specifications

### `.spkg` Container Format (`SpkgHeader`)
* **Magic:** `0x474B50534F595241ULL` (`"ARYOSPKG"`, version `1`)
* **Execution Tiers:** `0` = Tier A Native C++20 (`< 120 ns`), `1` = Tier B Rust Wasm3 (`< 1.5 µs`), `2` = Tier C LuaJIT FFI (`< 450 ns`)
* **Cryptographic Sealing:** 64-byte **Ed25519** signature computed over the 128-byte concatenation of four SHA-256 digests:
  $$\text{MerkleInput} = \text{SHA256}(\text{Manifest}) \parallel \text{SHA256}(\text{Payload}) \parallel \text{SHA256}(\text{Source}) \parallel \text{SHA256}(\text{PreFlightVector})$$

### `.slab` Zero-Copy Dataset Format (`SlabRecordHeader`)
* **Magic:** `0x534C4142` (`"SLAB"`, Big-Endian)
* **Record Layout:** `[magic: u32 BE][event_id: u32 BE][ground_truth: u32 BE (0|1)][tensor_dim: u32 BE][features: float32 BE × tensor_dim]`

### `.spcap` Sealed Capture Format
* **Magic:** `0x5043415053504B47ULL` (`"SPKGPAP"`)
* **Layout:** `[magic: 8B][Ed25519_sig: 64B][manifest_len: 4B][manifest][raw_pcap]` where signature signs $\text{SHA256}(\text{Manifest}) \parallel \text{SHA256}(\text{PCAP})$.

---

## 2. `.spkg` Authoring, Sealing & Audit Commands

| Command | Duty & Behavior |
| :--- | :--- |
| `sentinel-artifact keygen <prefix>` | Generates an OpenSSL EVP Ed25519 keypair: `<prefix>_private.pem` and `<prefix>_public.pem`. |
| `sentinel-artifact new <name> [rust\|cpp\|lua]` | Scaffolds a complete extension project with `manifest.json`, `tests/preflight_frame.bin` (`0xDEADBEEF...`), and language-specific starter code (`Cargo.toml`+`src/lib.rs`, `CMakeLists.txt`+`src/plugin.cpp`, or `<name>.lua`). Default language: `rust`. |
| `sentinel-artifact pack [dir] [priv_key.pem]` | Auto-discovers signing key via SSFS PKI hierarchy (auto-generating one in `PkiCerts` if absent), injects `author_public_key` & `slug` into `manifest.json`, locates compiled binary + source + test vector, and writes `<dir>/<name>.spkg`. |
| `sentinel-artifact pack-raw <key> <tier> <manifest> <payload> <src> <test_bin> <out.spkg>` | Low-level deterministic `.spkg` packer accepting explicit paths and numeric tier (`0`, `1`, or `2`). |
| `sentinel-artifact inspect <file.spkg>` | Parses `SpkgHeader`, displays execution tier, payload/source/test-vector byte sizes, and prints the embedded `manifest.json`. |
| `sentinel-artifact verify <pub_key.pem> <file.spkg>` | Recomputes the 4-way SHA-256 Merkle digest and verifies the Ed25519 signature against `<pub_key.pem>`. |
| `sentinel-artifact extract-source <file.spkg> <out_src>` | Extracts the embedded human-readable source code from a sealed `.spkg` for compliance and security auditing. |
| `sentinel-artifact test <file.spkg>` | Runs the in-sandbox pre-flight assertion against the embedded `preflight_frame.bin` across **8 protocol threat classes**: `0xDEADBEEF` scaffold marker, IEC-104 ASDU (`0x2D`/`0x2E`), S7Comm CPU STOP (`0x29`), Modbus Write Coil (`0x05`/`0x0F`), DNP3 Direct Operate (`0x05`/`0x06`/`0x0E`), BACnet/IP, Log4j (`${jndi:`), and Triton SIS (`0xFD`/`0xFE`). |

---

## 3. SLAB Protocol, `.spcap` Sealing & Autonomous Vaccine Synthesis

| Command | Duty & Behavior |
| :--- | :--- |
| `sentinel-artifact slab convert <in.csv> <out.slab> <dim>` | Converts numeric CSV (auto-skipping header row; treating column `dim+1` as binary ground-truth label) into Big-Endian `0x534C4142` SLAB format and auto-generates companion `manifest.json` + `<out.slab>.manifest.json`. |
| `sentinel-artifact slab verify <file.slab>` | Walks every SLAB record header verifying magic `0x534C4142`, reporting total record count, feature dimensionality, and byte size. |
| `sentinel-artifact pcap pack <priv_key> <manifest.json> <in.pcap> <out.spcap>` | Computes Ed25519 signature over manifest + PCAP digests and writes a tamper-evident `.spcap` container. |
| `sentinel-artifact synthesize-vaccine <exploit.json\|dir> [out_dir]` | Ingests a honeynet exploit JSON (or newest `exploit_*.json` in a directory), parses `protocol` (`MODBUS`, `S7COMM`, `IEC104`), `function_code`, `payload_hex`, and `client_ip`, synthesizes a Tier C LuaJIT reflex rule + `manifest.json` + `preflight_frame.bin`, generates a keypair, seals `<pkg>.spkg`, and runs `test` preflight before declaring readiness for sub-50ms fleet broadcast. |

---

## 4. Universal Hub Publisher (`publish`)

```bash
sentinel-artifact publish <file> [--token <API_KEY>] [--hub-url <URL>]
# Equivalent umbrella shortcut:
aryo publish <file> [--token <API_KEY>]
```

* **Auto-Loaded Credentials:** Automatically reads `api_key` and `hub_url` from SSFS `Config/credentials.json` if `--token` is omitted.
* **Automatic Asset Type & Endpoint Routing:**
  * `.spkg` -> `package` -> `POST /api/v1/hub/publish` (inherits internal manifest & signature)
  * `.onnx` / `.engine` / `.rknn` -> `model` -> `POST /api/v1/hub/publish`
  * `.slab` -> `dataset` -> `POST /api/v1/hub/publish`
  * `.pcap` / `.spcap` -> `pcap` -> `POST /api/v1/hub/publish`
  * `.tar.gz` / `.tgz` / `.tar` -> `scenario` -> `POST /api/v1/hub/publish`
  * `.blueprint` -> `blueprint` -> `POST /api/v1/hub/blueprints/publish`
* **Manifest & Signature Assembly:** Ingests `<file>.manifest.json` or sibling `manifest.json` when present (otherwise synthesizes schema-compliant defaults), signs raw artifact bytes with the SSFS developer Ed25519 private key, and injects `slug` and `author_public_key`.
