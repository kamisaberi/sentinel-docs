# Cartridge & 3-Tier Plugin SDK Specification

Every domain cartridge exposes a modular dissector interface dynamically ingested by `blackbox-sentinel`'s `PluginSupervisor`.

---

## 1. The 3 Extensibility Tiers

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE 3-TIER EXTENSIBILITY TAXONOMY                                    │
├──────┬──────────────────────┬──────────────────┬──────────────┬────────────────────────────────────────┤
│ Tier │ Language / Engine    │ Binary Extension │ Mean SLA     │ Primary Use Case                       │
├──────┼──────────────────────┼──────────────────┼──────────────┼────────────────────────────────────────┤
│ A    │ Native C++20         │ .so              │ < 120 ns     │ Deterministic line-rate protocol gates │
│ B    │ Rust Wasm3 (no_std)  │ .wasm            │ < 1.50 µs    │ Memory-safe sandboxed third-party logic│
│ C    │ LuaJIT C-FFI         │ .lua             │ < 450 ns     │ Zero-downtime hot-reloadable rules     │
└──────┴──────────────────────┴──────────────────┴──────────────┴────────────────────────────────────────┘
```

---

## 2. Tier A: Native C++20 Dissector Contract

Native dissectors implement the `sentinel::sdk` C ABI, compiling with zero runtime heap allocation:

```cpp
#include <sentinel/sdk/plugin.hpp>

using namespace sentinel::sdk;

static SentinelDissectorResult custom_dissect(const SentinelRawPacket* raw_pkt) {
    if (!raw_pkt || !raw_pkt->data || raw_pkt->length < 8) {
        return VerdictBuilder::Pass();
    }
    
    // Constant-time inspect bytes
    if (raw_pkt->data[7] == 0x05) { // e.g. Modbus Write Single Coil
        return VerdictBuilder::Drop(9001, "UNAUTHORIZED_COIL_WRITE").build();
    }
    return VerdictBuilder::Pass();
}
```

Dissectors are compiled to shared objects and deployed to `/usr/local/lib/blackbox/` or SSFS `${SENTINEL_ROOT}/spkg/installed/<cartridge>/`.
