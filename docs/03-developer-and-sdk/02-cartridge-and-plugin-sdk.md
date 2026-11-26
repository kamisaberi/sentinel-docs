# Cartridge & 3-Tier Plugin SDK Specification

Every domain cartridge exposes a modular dissector interface dynamically ingested by `blackbox-sentinel`'s `PluginSupervisor`.

---

## 1. The 3 Extensibility Tiers

| Tier | Language / Engine | Binary Extension | Mean SLA | Primary Operational Scope |
| :--- | :--- | :--- | :--- | :--- |
| **Tier A** | Native C++20 | `.so` | `< 120 ns` | Deterministic line-rate protocol gates |
| **Tier B** | Rust Wasm3 (`no_std`) | `.wasm` | `< 1.50 µs` | Memory-safe sandboxed third-party logic |
| **Tier C** | LuaJIT C-FFI | `.lua` | `< 450 ns` | Zero-downtime hot-reloadable rules |

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
    if (raw_pkt->data[7] == 0x05) { // e.g., Modbus Write Single Coil
        return VerdictBuilder::Drop(9001, "UNAUTHORIZED_COIL_WRITE").build();
    }
    return VerdictBuilder::Pass();
}

static SentinelPluginDescriptor g_descriptor = {
    SENTINEL_SDK_MAGIC,
    SENTINEL_SDK_VERSION_MAJOR,
    SENTINEL_SDK_VERSION_MINOR,
    SENTINEL_TIER_NATIVE_CPP,
    "org.aryorithm.package.custom_guard",
    "custom_guard",
    "1.0.0",
    "CUSTOM",
    502,
    0,
    nullptr,
    nullptr,
    custom_dissect
};

SENTINEL_REGISTER_PLUGIN(g_descriptor)
```

Dissectors are compiled to shared objects and deployed to `/usr/local/lib/blackbox/` or SSFS `${SENTINEL_ROOT}/spkg/installed/<cartridge>/`.
