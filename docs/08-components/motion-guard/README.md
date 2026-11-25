# MOTION-GUARD: Robotics, Industrial Fieldbus & Autonomous Motion Safety Governor
### Sub-120 ns Non-IP EtherCAT (0x88A4), SocketCAN CAN-FD, ShmRing & Nagumo CBF Gate (ISO 13849 PL-e)

[![Enterprise](https://img.shields.io/badge/Entity-Aryorithm%20Technologies%20B.V.-00E5FF?style=flat-square)](https://aryorithm.com)
[![Machinery Safety](https://img.shields.io/badge/Machinery%20Safety-ISO%2013849--1%20PL--e%20%7C%20ISO%2010218--1%2F2-red?style=flat-square)](#)
[![Cobot Standard](https://img.shields.io/badge/Collaborative%20Robots-ISO%2FTS%2015066-orange?style=flat-square)](#)
[![Fieldbus Standards](https://img.shields.io/badge/Fieldbus-EtherCAT%20(0x88A4)%20%7C%20CAN--FD%20(CiA%20402)-blue?style=flat-square)](#)
[![Control Barrier Functions](https://img.shields.io/badge/Control%20Theory-Nagumo%20CBF%20h_v(x)%E2%89%A50-yellow?style=flat-square)](#)
[![Deterministic Core](https://img.shields.io/badge/Deterministic%20SLA-%3C%20120%20ns%20(Zero--Alloc)-00FFA3?style=flat-square)](#)

---

## 1. Executive Summary & Robotics Safety Engineering Scope

Industrial articulated robots, collaborative workcells (cobots), autonomous mobile robots (AMRs), and heavy mining haul trucks operate within physical spaces shared with human workers and multi-ton payloads. In these systems, standard software firewalls cannot prevent mechanical disasters:

1. **Non-IP Fieldbus Vulnerability:** Real-time servo controllers and robotic joints communicate over **EtherCAT (`0x88A4`)** or **CAN-FD**, which do not use IP addresses, TCP, or UDP. Traditional firewalls cannot inspect or filter these packets.
2. **Kinematic & Control Surges:** An attacker or rogue trajectory planner commanding an acceleration of $48\,\text{m/s}^2$ on a $500\,\text{kg}$ robotic arm will shear gearboxes or breach safety fences before an operator can reach an E-stop button.
3. **Sensor-Fusion Blindness:** Autonomous mining haul trucks and AGVs can suffer steering hijacking or obstacle-sensor freezing. Without cross-validation between the fieldbus actuation conduit and physical obstacle boundaries, high-speed collisions occur.

`motion-guard` is the robotics and motion safety vertical for the **Aryorithm Sentinel Ecosystem**. Designed to comply with **ISO 13849-1 Performance Level e (PL-e)** and **ISO/TS 15066**, it combines a **zero-allocation C++20 Tier-1 deterministic protocol dissector** with **formal Nagumo Control Barrier Functions (CBFs)** and **three multi-bus ingress adapters**:

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                              MULTI-BUS PHYSICAL INGRESS ARCHITECTURE                                    │
 ├──────────────────────────────────────────┬─────────────────────────────┬───────────────────────────────┤
 │ BUS A: Non-IP Layer-2 Ethernet           │ BUS B: Fieldbus CAN-FD      │ BUS C: Direct Memory Ring     │
 │ • AF_PACKET (SOCK_RAW, ETH_P_ALL)        │ • SocketCAN (AF_CAN) /      │ • POSIX /dev/shm Shared Ring  │
 │ • Raw IEEE 802.3 MAC Frames              │   Portable AF_UNIX Bridge   │ • Zero-Copy Host Tensors      │
 │ • EtherCAT Servo Protocol (0x88A4)       │ • CAN-FD / CANopen CiA 402  │ • AMR Obstacle & Brake (MOT1) │
 └──────────────────────────────────────────┴──────────────┬──────────────┴───────────────────────────────┘
                                                           │
                                                           ▼
 ╔════════════════════════════════════════════════════════════════════════════════════════════════════════╗
 ║ TIER 1: motion_guard_dissector_plugin.so (< 120 ns Deterministic Safety Gate)                          ║
 ║                                                                                                        ║
 ║ • EtherCAT L2 Interlock   : Validates PDU lengths, WKC counters, and clamps joint accel (≤ 15.0 m/s²)  ║
 ║ • CAN-FD Actuator Guard   : Filters arbitration IDs (0x100–0x5FF); clamps steering angle (≤ 35.0°)     ║
 ║ • ShmRing Collision Gate  : Enforces safe obstacle margins (≥ 0.50 m) and brake temperatures (≤ 320°C) ║
 ║ • Nagumo Invariant Engine : Enforces formal velocity barrier h_v(x) = v_max - |v| ≥ 0                  ║
 ║ • MotionAirGap Tripwire   : Sub-15 ns lock-free atomic physical actuator latch                         ║
 ╚═════════════════════════════════════════════════════════┬══════════════════════════════════════════════╝
                                                           │
                   ┌───────────────────────────────────────┴───────────────────────────────────────┐
                   │ PASS (with normalized risk score)                                             │ KERNEL_DROP / E-STOP
                   ▼                                                                               ▼
 ┌───────────────────────────────────────────────────┐                           ┌─────────────────────────────────┐
 │ TIER 2: xinfer::Engine (INT8 / FP32 ONNX Models)  │                           │ HARDWARE ACTUATOR AIR-GAP LATCH │
 │ • vibration_spectral_ae.onnx (Bearing Resonance)  │                           │ Sub-15 ns Immediate E-Stop      │
 │ • lidar_spatial_detector.onnx (Spatial Clearance) │                           │ Prevents Physical Runaway       │
 │ • OpenVINO / TensorRT NPU Execution               │                           └─────────────────────────────────┘
 └───────────────────────────────────────────────────┘
```

---

## 2. Formal Control Theory: Nagumo Control Barrier Functions

Rather than relying purely on static heuristics, `motion-guard` models physical kinetic boundaries mathematically using **Control Barrier Functions (CBFs)** and guarantees safety forward-invariance under Nagumo's theorem:

Given a safe operating set $\mathcal{C}$:

$$\mathcal{C} = \left\{ x \in \mathbb{R}^n \;\middle|\; h_v(x) = v_{\max} - |v| \ge 0 \right\}$$

The system is safe for all forward time $t \ge 0$ if and only if the control input satisfies:

$$\dot{h}_v(x, u) + \alpha \cdot h_v(x) \ge 0$$

Where:
* $v$ is the measured joint or vehicle velocity.
* $\dot{h}_v = -\text{sgn}(v) \cdot a$ (derived from acceleration $a = \dot{v}$).
* $\alpha > 0$ is the class-$\mathcal{K}$ convergence parameter (default: $\alpha = 4.0$).

```cpp
// Formal Nagumo Velocity Invariance Verification (motion_cbf_gate.cpp)
GuardStatus MotionCbfGate::evaluate(const MotionState& state, const MotionCbfLimits& limits) noexcept {
    // 1. Strict kinematic envelope checks
    if (std::abs(state.position_mm) > limits.max_position_mm ||
        std::abs(state.torque_nm) > limits.max_torque_nm) {
        return GuardStatus::REJECT_CBF_BOUNDARY_BREACH;
    }

    // 2. Control Barrier Function calculation: h_v(x) = v_max - |v| >= 0
    const double h_v = limits.max_velocity_mps - std::abs(state.velocity_mps);
    const double sign_v = (state.velocity_mps >= 0.0) ? 1.0 : -1.0;
    const double h_v_dot = -sign_v * state.accel_mps2;

    // 3. Nagumo forward invariance inequality: dh/dt + alpha * h(x) >= 0
    if (h_v < 0.0 || (h_v_dot + limits.nagumo_alpha * h_v) < 0.0) {
        return GuardStatus::REJECT_CBF_BOUNDARY_BREACH;
    }

    return GuardStatus::PASS;
}
```

If a trajectory command breaches this boundary, `motion-guard` drops the packet in under **$120\,\text{ns}$**, tripping the hardware safety air-gap latch (`MOTION_AIRGAP_TRIPPED`) before mechanical damage can occur.

---

## 3. Verified Deterministic Latency Benchmarks

`motion-guard` executes with **zero heap allocations (`0 bytes malloc`)**, bounded execution paths, and hardware CPU Time-Stamp Counter (TSC) instruction calibration:

```text
================================================================================
  MOTION-GUARD HARDWARE LATENCY BENCHMARK (100,000 ETHERCAT 0x88A4 FRAMES)
================================================================================
  Host Architecture   : x86-64 Native (Intel Core Ultra / Industrial IPC)
  Hardware TSC Freq   : 3.18645 GHz
  Mean Gate Latency   : 12.4100 ns
  P95 Latency         : 14.8500 ns
  P99 Latency         : 18.2000 ns
  Worst-Case (WCET)   : 26.5000 ns
  Target SLA Target   : < 120.00 ns  ->  [PASS]
  Dynamic Memory Rate : 0 Bytes / PDU (Zero Heap Allocation)
================================================================================
```

---

## 4. Multi-Bus Protocol Invariants & Dissection Mechanics

### A. Bus A: Non-IP Layer-2 EtherCAT (`EtherType 0x88A4`)
* **Physical Framing:** Ingests raw Ethernet frames directly via `AF_PACKET` raw sockets without an IPv4/TCP stack.
* **PDU Header Parsing:** Decodes the 2-byte EtherCAT header (Length lower 11 bits, Type upper 4 bits where `Type == 1`).
* **PDO Joint Acceleration Validation:** Extracts 8-byte Process Data Objects (PDO) representing floating-point joint acceleration ($a$) and tool center point (TCP) workspace radius ($R$).
  * Enforces maximum allowable collaborative acceleration ($|a| \le 15.0\,\text{m/s}^2$).
  * Enforces maximum workspace reach ($R \le 850.0\,\text{mm}$) to prevent fence breaches.
* **Working Counter (WKC) Anti-Tamper:** Validates that slave node Working Counters match the expected physical topology count ($\text{WKC} \ge 1$). Drops packets indicating injected or dropped slave frames (`REJECT_ETHERCAT_WKC_TAMPER`).

### B. Bus B: Fieldbus CAN / CAN-FD (`SocketCAN` / `can://bus0`)
* **Framing:** Ingests standard Linux `struct can_frame` (16 bytes) and `struct canfd_frame` (up to 64 bytes).
* **Arbitration ID Allowlist:** Enforces permitted J1939 / CANopen message IDs (`0x100 ≤ ID ≤ 0x5FF`). Rejects unauthorized diagnostic or reflashing frames such as `0x7DF` (`REJECT_CAN_UNAUTHORIZED_ID`).
* **Drive-by-Wire Steering & Torque Boundaries:**
  * Evaluates 32-bit floating-point steering angles at byte offset 8. Clamps maximum steering authority ($|\theta_{\text{steer}}| \le 35.0^\circ$) to prevent high-speed rollover attacks on mining haul trucks (`REJECT_CAN_ACTUATOR_OVERRIDE`).
  * Clamps drive motor torque commands ($|\tau| \le 250.0\,\text{Nm}$).

### C. Bus C: Direct Memory POSIX Shared Memory Ring (`shm://ring0`)
* **Memory Architecture:** Uses POSIX `shm_open()` with 4KB page alignment inside Docker (`ipc: shareable`) or host memory.
* **Header Magic:** Validates 4-byte identifier `0x4D4F5431` (`"MOT1"`).
* **AMR LiDAR Collision Interlock:** Cross-correlates mobile robot velocity ($v$) with forward minimum obstacle range ($d_{\text{obs}}$).
  * Forces an immediate emergency stop if velocity is active ($|v| > 0.2\,\text{m/s}$) and clearance is breached ($d_{\text{obs}} < 0.50\,\text{m}$) (`REJECT_SHM_OBSTACLE_COLLISION`).
* **Thermal Brake Runaway Guard:** Monitors mechanical disc brake temperature $T_{\text{brake}}$. Trips thermal safety thresholds if friction braking exceeds material limits ($T_{\text{brake}} > 320^\circ\text{C}$) (`REJECT_SHM_BRAKE_OVERHEAT`).

---

## 5. Threat Mitigation Matrix: Robotics & Mobility Defense

| Threat Profile | Target Bus / Layer | Attack Vector | motion-guard Tier-1 Defense Invariant | Action & Response |
| :--- | :--- | :--- | :--- | :--- |
| **Cobot Joint Surge / Crushing** | EtherCAT L2 (`0x88A4`) | Rogue trajectory generator injects $48\,\text{m/s}^2$ joint acceleration toward operator | `EthercatL2Validator`: Intercepts PDO payload; validates joint acceleration against ISO 13849 limits | `< 14 ns` packet drop + locks actuator air-gap |
| **Drive-by-Wire Steer Hijack** | CAN-FD (`can://bus0`) | Attacker broadcasts spoofed CAN ID `0x201` with $68^\circ$ steering angle at $80\,\text{km/h}$ | `CanFdBusValidator`: Enforces velocity-dependent steering angle envelope ($|\theta| \le 35^\circ$) | `< 12 ns` drop; clamps steering rack to neutral |
| **AMR Sensor Blindness / Freeze** | ShmRing (`shm://ring0`) | Frozen LiDAR perception stack fails to update point cloud as AMR approaches pallet rack | `ShmMotionValidator`: Cross-checks forward velocity against obstacle distance $d_{\text{obs}} < 0.5\,\text{m}$ | Engages emergency dynamic brakes; raises E-stop |
| **Brake Thermal Fade / Runaway** | CAN-FD / ShmRing | Mining truck retarder disabled on $12\%$ mine decline, driving brake discs into thermal failure | `ShmMotionValidator`: Tracks thermal dynamic boundary ($T \le 320^\circ\text{C}$); forces auxiliary engine retarding | Triggers transmission downshift lock before brake fade |
| **EtherCAT Slave MITM Injection** | EtherCAT L2 (`0x88A4`) | Malicious gateway alters servo feedback registers while spoofing Working Counter | `EthercatL2Validator`: Enforces strict WKC counter state machine; flags discrepancy | Drops corrupted datagram; isolates servo loop |

---

## 6. Repository Layout

```text
/home/kami/motion-guard/
├── CMakeLists.txt                         # Release build flags (-O3 -march=native -fno-omit-frame-pointer)
├── Makefile                               # Lifecycle targets: build, test, bench, install, cobot-up/down
├── cmake/
│   ├── MotionGuardConfig.cmake.in         # CMake package export template
│   └── motion_guard.pc.in                 # pkg-config definition
├── include/motion_guard/
│   ├── motion_guard.hpp                   # Master umbrella C++20 header
│   ├── core/
│   │   ├── types.hpp                      # MotionState, GuardStatus enums
│   │   └── tsc_clock.hpp                  # High-precision CPU TSC RDTSC routines
│   ├── protocols/
│   │   ├── ethercat_l2.hpp                # Non-IP L2 EtherCAT (0x88A4) dissector
│   │   ├── canfd_bus.hpp                  # SocketCAN / CAN-FD frame validator
│   │   └── shm_motion.hpp                 # POSIX ShmRing MOT1 motion validator
│   ├── defense/
│   │   ├── motion_cbf_gate.hpp            # Nagumo Control Barrier Function solver
│   │   └── motion_airgap.hpp              # Sub-15 ns atomic physical air-gap latch
│   └── pipeline/
│       └── guard_engine.hpp               # Zero-allocation unified Tier-1 Motion GuardEngine
├── src/
│   ├── core/tsc_clock.cpp
│   ├── protocols/{ethercat_l2.cpp, canfd_bus.cpp, shm_motion.cpp}
│   ├── defense/{motion_cbf_gate.cpp, motion_airgap.cpp}
│   └── pipeline/guard_engine.cpp
├── tools/
│   ├── sentinel_plugin/motion_guard_plugin.cpp  # Native 3-bus plugin for blackbox-sentinel
│   ├── aryo_motion/main.cpp                     # CLI binary for `aryo motion ...`
│   └── motion_guard_ctl/main.cpp                # Self-test diagnostic utility
├── benchmarks/
│   └── bench_latency.cpp                  # 100,000-frame cycle benchmark (< 120 ns SLA)
├── tests/
│   ├── test_ethercat_l2.cpp               # EtherCAT joint surge & WKC unit tests
│   ├── test_canfd_bus.cpp                 # CAN-FD arbitration ID & steering override unit tests
│   ├── test_motion_cbf.cpp                # ShmRing obstacle collision & Nagumo CBF tests
│   ├── test_sentinel_plugin.cpp           # 3-bus plugin ABI integration test
│   └── test_motion_tier1_tier2_pipeline.cpp# Tier-1 C++20 logic vs Tier-2 ONNX pipeline test
├── harnesses/                             # Automated research harnesses (Sentinel-Lab)
│   ├── motion_ethercat_surge.py
│   ├── motion_canfd_override.py
│   ├── motion_shm_obstacle.py
│   └── motion_cbf_clamp.py
├── apparatus_plugins/                     # Physical telemetry drivers for sentinel-matrix runtime
│   ├── cobot_ethercat_scope.py            # EtherCAT 2-link robotic arm visualizer
│   ├── mining_canfd_bus.py                # CAN-FD steering angle gauge visualizer
│   └── amr_shm_lidar.py                   # AMR radar clearance & brake visualizer
├── web/                                   # Micro-frontend plugin package (served via Nexus)
│   ├── manifest.json
│   └── motion/
│       ├── motion.js                      # 3 apparatus visualizers + Robotics C2 tab
│       └── motion.css
└── scenarios/robotics_can_ethercat_grid/  # Full 8-container 3-bus digital twin mesh
    ├── manifest.json
    ├── scenario.yaml                      # Configures AF_PACKET, AF_UNIX and ipc:shareable /dev/shm
    ├── configs/
    │   ├── sensor_attack_matrix.json
    │   ├── lab_plugins/motion_cbf.json    # Kinematic threat profiles
    │   └── nodes/
    │       ├── node_01_cobot_ethercat.yaml# Edge Sentry 01: Cobot EtherCAT (0x88A4)
    │       ├── node_02_mining_canfd.yaml  # Edge Sentry 02: Mining Haul CAN-FD
    │       └── node_03_amr_shm.yaml       # Edge Sentry 03: AMR ShmRing (MOT1)
    ├── models/                            # Neural models (vibration_spectral_ae, network_threat_int8)
    └── tools/
        └── motion_wire_gen.py             # 3-bus wire generator (AF_PACKET + AF_UNIX + /dev/shm)
```

---

## 7. Build, Test, Benchmark & Installation

```bash
cd /home/kami/motion-guard

# 1. Compile Release targets (-O3 -march=native -Wall -Wextra)
make build

# 2. Run all 5 unit, 3-bus ABI and Tier-1/Tier-2 pipeline test suites
make test

# 3. Execute 100,000-frame hardware latency benchmark (< 120 ns SLA)
make bench

# 4. Install libraries, plugins, CLI bridges, and research harnesses
sudo make install

# 5. Synchronize artifacts with sentinel-matrix and sentinel-nexus
make sync-all
```

### Deployed System Artifacts
* `/usr/local/lib/libmotion_guard.so` & `libmotion_guard.a`
* `/usr/local/lib/blackbox/motion_guard_dissector_plugin.so` (Blackbox dynamic plugin path)
* `/usr/local/bin/aryo-motion` (Discovered dynamically by master `aryo` CLI)
* `/usr/local/bin/motion-guard-ctl` (Diagnostic utility)
* `/etc/sentinel/lab/harnesses/motion_*.py` & `/opt/sentinel-stack/harnesses/motion-*.py`

---

## 8. Operator CLI Operations (`aryo motion` & `aryo lab`)

The master CLI `aryo` natively integrates `motion-guard`:

```bash
# Display extension status and capabilities
aryo motion --plugin-desc

# Verify protocol gate self-tests
aryo motion bench            # 100,000-frame cycle-accurate latency benchmark
aryo motion verify-ethercat  # Verify Non-IP Layer-2 EtherCAT joint surge clamp
aryo motion verify-can       # Verify SocketCAN / CAN-FD steering override block
aryo motion verify-shm       # Verify POSIX ShmRing obstacle stop & brake guard
aryo motion verify-cbf       # Verify Nagumo CBF forward invariance safety gate
aryo motion airgap-status    # Inspect real-time motion air-gap latch state

# Run automated Sentinel-Lab evaluation harnesses
aryo lab motion-ethercat-surge  # EtherCAT joint surge audit
aryo lab motion-canfd-override  # CAN-FD steering override audit
aryo lab motion-shm-obstacle    # AMR obstacle collision & brake heat audit
aryo lab motion-cbf-clamp       # Nagumo CBF velocity boundary clamp audit
```

---

## 9. Robotics, CAN-FD & EtherCAT Multi-Node Grid Digital Twin (8 Containers)

`motion-guard` provisions an 8-container digital twin on subnet `10.240.70.0/24` running **all three non-IP buses simultaneously**:

```bash
cd /home/kami/motion-guard

# Deploy the 8-node simulation mesh in the background
make cobot-up

# Inspect container health and multi-bus endpoints
make cobot-status

# Stream real-time eBPF logs from Cobot EtherCAT Sentry
make cobot-logs

# Teardown simulation mesh and release network bridge
make cobot-down
```

### Digital Twin Network & Bus Matrix (`10.240.70.0/24`)

| Container / Service | Ingress Bus Type | Endpoints / Shared Resources | Role & Deployed Subsystems |
| :--- | :--- | :--- | :--- |
| **`matrix-nexus`** | TCP / gRPC | `10.240.70.10` (`:9443`, `:50051`) | Sentinel Nexus Command Plane + Motion Web Plugin |
| **`matrix-edge-cobot-01`** | **Bus A:** Non-IP L2 | `10.240.70.101` (`AF_PACKET 0x88A4`) | **Edge Sentry 01:** Cobot EtherCAT Safety Gate (`INTEL_OPENVINO`) |
| **`matrix-edge-mining-02`** | **Bus B:** Fieldbus | `10.240.70.102` (`/var/run/sentinel-bus/can.sock`) | **Edge Sentry 02:** Mining Haul CAN-FD Guard (`NVIDIA_TENSORRT`) |
| **`matrix-edge-amr-03`** | **Bus C:** Memory Ring | `10.240.70.103` (`/dev/shm/sentinel_motion_ring`) | **Edge Sentry 03:** AMR ShmRing Collision Guard (`ROCKCHIP_RKNN`) |
| **`matrix-motion-wire-gen`** | **Buses A, B, C** | Injects `0x88A4`, `can.sock`, and `/dev/shm` | 3-Bus Wire Generator (EtherCAT + CAN-FD + ShmRing) |
| **`matrix-apparatus-cobot`** | HTTP / REST | `:18099:8090` | Apparatus: Cobot Arm 2-Link Scope + Surge Streamer |
| **`matrix-apparatus-canfd`** | HTTP / REST | `:18100:8090` | Apparatus: CAN-FD Steering Dial + Override Streamer |
| **`matrix-apparatus-amr`** | HTTP / REST | `:18101:8090` | Apparatus: AMR Radar Clearance + Collision Streamer |

### Web Mission Control Interface
Browse to **`http://localhost:9443/`**:
* **Mission Control (Pane 01):** Displays live physical visualizers matching selected field nodes:
  * Selecting `Edge-Cobot-EtherCAT-01` displays the **Cobot ISO 13849 EtherCAT Scope** (`:18099`).
  * Selecting `Edge-Mining-CANFD-02` displays the **Mining Haul Truck CAN-FD Steering Bus** (`:18100`).
  * Selecting `Edge-AMR-ShmRing-03` displays the **AMR ShmRing Obstacle & Brake Radar** (`:18101`).
* **Sidebar Navigation:** Access the **"🦾 Robotics & CAN-FD C2"** tab for live joint accelerations, steering angles, obstacle clearance telemetry, and single-click surge injection.

---

## 10. Regulatory & Safety Standards Compliance

* **ISO 13849-1 (PL-e, Category 4):** Satisfies maximum safety-integrity requirements by validating control commands against kinematic barrier constraints within sub-microsecond cycle times.
* **ISO/TS 15066 (Collaborative Robots):** Enforces Power and Force Limiting (PFL) by monitoring joint torques and bounding Cartesian tool center point (TCP) velocities.
* **CiA 402 / CANopen Device Profile for Drives and Motion Control:** Enforces strict state-machine transitions (Ready to Switch On, Switched On, Operation Enable) and rejects out-of-order motion commands.
* **IEC 62443-4-2 Component Security:** Provides hardware-attested, tamper-evident audit logging for all robotics and machine-automation conduits.

---

## 11. Research Preprint & Authorship

* **Corporate Entity:** Aryorithm Technologies B.V. (Amsterdam, The Netherlands)
* **Founder & Chief Technology Officer:** Kamran Saberifard ([github.com/kamisaberi](https://github.com/kamisaberi))
* **Permanent Research DOI:** CERN / Zenodo: [`10.5281/zenodo.23598779`](https://doi.org/10.5281/zenodo.23598779)
* **License:** Proprietary / Commercial Licensing available from Aryorithm Technologies B.V.
