# Binary Formats Specification (.spkg, .slab, .blueprint, .aryopack)

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

$$\text{MerkleRoot} = \text{SHA256}(\text{SHA256}(\text{manifest}) \parallel \text{SHA256}(\text{payload}) \parallel \text{SHA256}(\text{source}) \parallel \text{SHA256}(\text{test\_vector}))$$

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
