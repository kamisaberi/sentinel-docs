# Master Build Order & Dynamic Linkage DAG (14 Repositories)

To ensure reproducible, zero-circular-dependency compilation across clean air-gapped environments, the Aryorithm ecosystem enforces a strict bottom-up compilation order from Tier 0 to Tier 4.

---

## 1. Topologically Sorted Compilation Sequence

```mermaid
graph TD
    subgraph Step1["Step 1: Tier 0 Cores (Parallel)"]
        FS["sentinel-fs -> libsentinelfs.so, sfs"]
        BB["blackbox-essential -> libblackbox.so, xdp_drop.o"]
        XI["xinfer-essential -> libxinfer.so"]
    end

    subgraph Step2["Step 2: Tier 1 Ingress & Routing"]
        BS["blackbox-sentinel -> sentinel, sentinel-ctl, sentinel-artifact"]
        XF["xinfer-forge -> forge-cli"]
    end

    subgraph Step3["Step 3: Tier 2 Production Cartridges (Parallel)"]
        ICS["ics-guard -> libics_guard.so, aryo-ics"]
        CCSDS["ccsds-guard -> libccsds_guard.so, aryo-aerospace"]
        NET["net-guard -> libnet_guard.so, aryo-net"]
        MOT["motion-guard -> libmotion_guard.so, aryo-motion"]
        VIS["vision-guard -> libvision_guard.so, aryo-vision"]
    end

    subgraph Step4["Step 4: Tier 3 & Tier 4 Top-Level Stacks"]
        NEXUS["sentinel-nexus -> sentinel-nexus C2"]
        MATRIX["sentinel-matrix -> scenario_engine.py"]
        LAB["sentinel-lab -> Research Verification Harnesses"]
        STACK["sentinel-stack -> master aryo CLI"]
    end

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
```

---

## 2. Standard Toolchain Invariants
* **C++ Compiler:** Modern GCC (>= 13.0) or Clang (>= 16.0) supporting `-std=c++20`.
* **Optimization Flags:** `-O3 -march=native -Wall -Wextra -pthread -fno-omit-frame-pointer`.
* **Runtime Pathing (RPATH):** All binaries set `CMAKE_INSTALL_RPATH "/usr/local/lib"` to locate shared ecosystem libraries dynamically without brittle `LD_LIBRARY_PATH` overrides.
* **Kernel Dependencies:** `libbpf-dev`, `libelf-dev`, and `bpftool` for eBPF CO-RE bytecode generation.
