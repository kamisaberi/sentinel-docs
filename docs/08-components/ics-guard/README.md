# ICS-GUARD: Sovereign Deterministic OT & SCADA Security Engine
### Sub-120 ns Physical Invariant Verification & Active Conduit Defense (IEC 62443 Levels 1–2)

[![Enterprise](https://img.shields.io/badge/Entity-Aryorithm%20Technologies%20B.V.-00E5FF?style=flat-square)](https://aryorithm.com)
[![Standard](https://img.shields.io/badge/Security%20Standard-IEC%2062443--3--3%20%7C%20IEC%2062443--4--2-orange?style=flat-square)](#)
[![Compliance](https://img.shields.io/badge/Regulatory-EU%20NIS2%20(2022%2F2555)%20%7C%20NERC%20CIP-blueviolet?style=flat-square)](#)
[![Deterministic Core](https://img.shields.io/badge/Deterministic%20Core-C%2B%2B20%20Zero--Heap%20(11.96%20ns)-00FFA3?style=flat-square)](#)
[![Physical Integrity](https://img.shields.io/badge/Control%20Theory-Nagumo%20CBF%20h(x)%E2%89%A50-yellow?style=flat-square)](#)

---

## 1. Executive Summary & OT Engineering Rationale

Standard IT cybersecurity appliances fail in Operational Technology (OT) environments because they optimize for **data confidentiality over physical safety and availability**. Deep packet inspection engines that introduce non-deterministic buffering (> 5 ms jitter), rely on cloud lookups, or enforce blind TCP resets can trip high-voltage breakers, cause pump cavitation, or induce compressor surges.

`ics-guard` is a **zero-allocation, hardware-rooted cyber-physical security appliance** designed for deployment at **Purdue Model Levels 1 and 2** (Control Conduits and Industrial LANs). 

Operating as an active in-line safety interlock or a non-intrusive optical TAP listener, `ics-guard` inspects industrial protocol commands at **wire speed (`11.96 ns` mean verification latency)**, cross-correlating digital network packets with **Runge-Kutta 4th-Order (RK4) continuous physical dynamics and formal Control Barrier Functions (CBFs)** before malicious setpoints reach physical field actuators.

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                      PURDUE MODEL FOR CONTROL SYSTEMS (ISA-95 / IEC 62443)                             │
 ├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ LEVEL 4/5: Enterprise Network & Business ERP                                                           │
 ├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ LEVEL 3.5: Industrial DMZ (Historians, Patching, Remote Access Jump Hosts)                             │
 ├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ LEVEL 3: Site Operations & Supervisory Control (SCADA HMI Servers, Engineering Workstations - EWS)    │
 │   ▲                                                                                                    │
 │   │ Industrial Ethernet Conduit (Modbus TCP, Siemens S7Comm, IEC 60870-5-104, IEEE C37.118)          │
 │   ▼                                                                                                    │
 │ ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗ │
 │ ║  ics-guard DEPLOYMENT ZONE: LEVEL 1/2 CONDUIT SECURITY APPLIANCE                                  ║ │
 │ ║  • Hardware Fail-Open Bypass Relay / Passive Optical Splitter                                      ║ │
 │ ║  • Sub-120 ns Tier-1 Deterministic Protocol Dissector (Zero Heap / Zero Dynamic Alloc)           ║ │
 │ ║  • Continuous Physics Boundary Evaluation (Nagumo Invariant Gate: dh/dt + α·h(x) ≥ 0)             ║ │
 │ ║  • Sub-15 ns Hardware Actuator Air-Gap Tripping Engine                                             ║ │
 │ ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝ │
 │   ▲                                                                                                    │
 │   │ Hardwire Actuation / Fieldbus Conduits (Coils, Holding Registers, Analog Voltage, 4-20mA)         │
 │   ▼                                                                                                    │
 │ LEVEL 1: Local Control & Protection (PLCs, RTUs, Protection IEDs, Safety Instrumented Systems - SIS)   │
 ├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ LEVEL 0: Physical Process (Reactors, High-Voltage Busbars, Centrifuges, Valves, Hydraulic Piping)     │
 └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Verified Deterministic Benchmarks

All hot-path protocol decoders in `ics-guard` execute with zero heap allocation (`0 bytes malloc/new`), zero lock contention on hot paths, and bounded instruction depth. Latencies are measured using CPU Time-Stamp Counter (RDTSC) hardware register cycles calibrated against host hardware.

```text
================================================================================
  ICS-GUARD HARDWARE LATENCY BENCHMARK (100,000 MODBUS TCP FRAMES)
================================================================================
  Host Architecture   : x86-64 Native (Intel Xeon / Industrial Core Ultra)
  Hardware TSC Freq   : 3.18645 GHz
  Mean Gate Latency   : 11.9573 ns
  P95 Latency         : 12.4200 ns
  P99 Latency         : 12.8670 ns
  Worst-Case (WCET)   : 19.4500 ns
  IEC 62443 SLA Target: < 120.00 ns  ->  [PASS]
  Allocation on Ingress: 0 Bytes (Fixed Ring / Static Stack Storage)
================================================================================
```

---

## 3. Supported Industrial Protocols & Deep Invariant Dissection

`ics-guard` implements native C++20 dissectors covering critical industrial infrastructure protocols:

### A. Modbus TCP / IP (Port 502)
* **MBAP Bounds Checking:** Validates Transaction ID, Protocol Identifier (`0x0000`), Length byte calculation, and Unit ID consistency.
* **Function Code Whitelisting:** Enforces read-only policies (`FC01` Coils, `FC02` Discrete Inputs, `FC03` Holding Registers, `FC04` Input Registers).
* **Write-Lock & Range Isolation:** Intercepts `FC05` (Write Single Coil), `FC06` (Write Single Register), and `FC15/16` (Multiple Write). Blocks writes targeting safety-critical memory ranges (e.g., setpoints in registers `40001–40100`).
* **Diagnostic & Smuggling Mitigation:** Drops unauthorized diagnostic commands (`FC08`), encapsulated interface commands (`FC2B`), and malformed frames used for protocol tunneling.

### B. Siemens S7Comm (Port 102)
* **TPKT / COTP Framing:** Verifies TPKT Version 3 (`0x03`) and ISO 8073 COTP connection state machine (Connection Request `0xE0`, Confirm `0xD0`).
* **S7 PDU ROSCTR Inspection:** Inspects S7 Comm Protocol Data Unit (`0x32`), verifying Job Requests (`ROSCTR 0x01`) and Userdata (`ROSCTR 0x07`).
* **Stuxnet PLC-State Override Prevention:** Detects and drops CPU Control commands targeting PLC mode switches:
  * Blocks CPU STOP (`Function 0x29`).
  * Blocks Program Invocations (`Function 0x28`).
  * Blocks unauthorized variable writes (`Function 0x05`) and block downloads (`0x1A..0x1C`) targeting Safety Data Blocks (DBs).

### C. IEC 60870-5-104 Telecontrol (Port 2404)
* **APCI Frame State Machine:** Validates Start-Frame `0x68`, Length byte, and supervisory frames (U-frames: `TESTFR`, `STARTDT`, `STOPDT`; S-frames: sequence confirmation).
* **ASDU Command Filtering (Industroyer / CrashRAT Mitigation):**
  * Dissects Type Identifier commands (Type 45: Single Command, Type 46: Double Command, Type 47: Regulating Step Command, Types 58–64: Time-Tagged Setpoints).
  * **Breaker Trip Lockout:** Detects Cause of Transmission (`COT 6` - Activation / `COT 8` - Deactivation) directed at high-voltage transmission substation breakers and triggers line-rate drop.

### D. IEEE C37.118.2 Synchrophasor Power Grid Standards (Port 15501)
* **Frame Synchronization:** Validates IEEE Sync bytes (`0xAA`) and P/M-class data frames.
* **Frequency Band Enforcement:** Monitors high-voltage transmission grid frequency with sub-millihertz precision, enforcing tight grid bounds (`49.50 Hz ≤ f ≤ 50.50 Hz`).
* **Rate-of-Change-of-Frequency (ROCOF):** Clamps transient frequency drift rate ($|\text{ROCOF}| \le 1.0\,\text{Hz/s}$) to prevent cascading blackout trips.
* **Total Harmonic Distortion (THD):** Inspects 1st, 2nd, 3rd, and 5th harmonic spectral energy, triggering alert thresholds when $\text{THD} > 8.0\%$.

---

## 4. Physics-Informed Control Theory: Nagumo Control Barrier Functions

Pure signature and protocol checks cannot identify an attacker who uses authentic, authorized protocol frames to drive a physical process into catastrophic runaway (e.g., slowly increasing chemical reactor pressure or heating an exothermic catalyst).

`ics-guard` integrates an embedded **Runge-Kutta 4th-Order (RK4)** numerical ODE solver and enforces **Nagumo Forward Invariance via Control Barrier Functions (CBFs)**:

$$\mathcal{C} = \{ x \in \mathbb{R}^n \mid h(x) \ge 0 \}$$

$$\dot{h}(x, u) + \alpha(h(x)) \ge 0$$

```c
// Example: Thermal Runway Invariant Check (plant_ode.c)
double plant_cbf_evaluate(const plant_state_t *state, double max_temp_c) {
    // Safe set boundary: h(x) = T_max - T(t) >= 0
    return max_temp_c - state->temperature;
}

bool plant_cbf_check_invariance(const plant_state_t *state, const plant_control_t *control, double max_temp_c, double alpha) {
    double h_val = plant_cbf_evaluate(state, max_temp_c);
    double h_dot_val = plant_cbf_dot_evaluate(state, control);
    // Nagumo invariance: dh/dt + alpha * h(x) >= 0
    return (h_dot_val + alpha * h_val) >= 0.0;
}
```

If an incoming Modbus or S7 command requests a control input $u(t)$ that violates the invariance inequality—meaning the physical plant will breach critical operating boundaries within the critical time horizon $T_\text{crit}$—the command is dropped immediately at the kernel boundary (`ACTUATOR_AIRGAP_TRIPPED`), independent of what SCADA or HMI dashboards report.

---

## 5. Threat Mitigation Matrix: Real-World ICS Attack Vector Defense

| Industrial Threat / Malware | Target Protocols | Attack Mechanism | ics-guard Tier-1 Defense Invariant | Enforcement Action |
| :--- | :--- | :--- | :--- | :--- |
| **Industroyer / Industroyer2** | IEC 60870-5-104 | Spurious breaker open commands (`COT 6`, Type 45/46) across 110kV–330kV substations | `Iec104Validator`: Drops unauthorized command ASDUs targeting breaker IOAs | Line-rate drop (`< 12 ns`) + latches substation interlock |
| **Stuxnet (Centrifuge Attack)** | Siemens S7Comm | Modifies S7-300 DB89 variables to alter variable frequency drive (VFD) rotor speed | `S7CommValidator`: Enforces DB write-lock (`0x05`) + RK4 centrifugal resonance CBF | Drops S7 PDU + trips mechanical safety air-gap |
| **TRITON / TRISIS** | Triconex TriStation / Modbus | Overwrites Safety Instrumented System (SIS) firmware logic to permit thermal runaway | `IndustrialThermalPlugin`: Cross-correlates radiometric thermal grid with SIS command stream | Rejects SIS logic alteration + initiates nitrogen quench |
| **Oldsmar Water Treatment** | Modbus TCP | Unauthorized operator setpoint modification increasing NaOH (Lye) dosing rate to lethal levels | `CbfSafetyGate`: Chemical titration corridor monitoring ($6.5 \le \text{pH} \le 8.5$) | Drops `FC05/06` writes breaching chemical boundary |
| **Ukraine 2015 Blackout** | IEC 60870-5-104 / S7 | Remote operator station hijacking followed by sequential substation blackout commands | Protocol state machine: Rate-limits and flags anomalous operator command bursts | Freezes unauthorized command conduits; locks HMI bridge |

---

## 6. Hardware & Network Deployment Architecture

`ics-guard` supports two physical deployment topologies based on facility safety requirements:

```text
TOPOLOGY 1: BUMP-IN-THE-WIRE (BITW) IN-LINE ACTIVE INTERLOCK
┌──────────────────────┐       ┌──────────────────────────────────────────────┐       ┌──────────────────────┐
│  SCADA Supervisory   │       │               ics-guard SENTRY               │       │   Field Controller   │
│  HMI / Engineering   │──────▶│ [NIC 0] ──▶ Hardware Relay ──▶ [NIC 1]       │──────▶│      PLC / RTU       │
│  Workstation (EWS)   │       │                 │                            │       │   Siemens / Rockwell │
└──────────────────────┘       │                 ▼ Line-Rate In-Kernel Engine │       └──────────────────────┘
                               │        [eBPF / AF_XDP Driver Ring]           │
                               │        Sub-120 ns Tier-1 Safety Gate         │
                               └──────────────────────────────────────────────┘
                               * Note: Hardware Fail-Open Relay ensures physical cable continuity during power loss.

TOPOLOGY 2: PASSIVE NON-INTRUSIVE OPTICAL TAP AUDIT (ZERO OPERATIONAL RISK)
┌──────────────────────┐                                                              ┌──────────────────────┐
│  SCADA Supervisory   │─────────────────────────────────────────────────────────────▶│   Field Controller   │
│  HMI / Engineering   │◀─────────────────────────────────────────────────────────────│      PLC / RTU       │
└──────────────────────┘                                                              └──────────────────────┘
            │                                                                                     │
            └───────────────┐                                                     ┌───────────────┘
                            ▼                                                     ▼
                     ┌──────────────────────────────────────────────────────────────────┐
                     │          Fiber-Optic Passive Tap / Network Regeneration Unit      │
                     └────────────────────────────────┬─────────────────────────────────┘
                                                      │ Monitor (Rx Only)
                                                      ▼
                                       ┌──────────────────────────────┐
                                       │       ics-guard SENTRY       │
                                       │   Passive Line-Rate Auditor  │
                                       └──────────────────────────────┘
```

### Physical Hardware Specifications (Industrial Field Appliance)
* **Form Factor:** DIN-Rail or 1U Ruggedized Rackmount (Fanless conduction cooling).
* **Power Supply:** Redundant dual $24\,\text{V DC}$ inputs ($9–36\,\text{V DC}$ wide-input tolerance).
* **Operating Temperature:** $-40^\circ\text{C}$ to $+75^\circ\text{C}$ (IEC 60068-2 cold/heat compliant).
* **Physical Relays:** Dual hardware watchdog fail-open bypass relays (Zero-Packet-Loss power-fail pass-through).
* **Root-of-Trust:** Dedicated discrete Infineon OPTIGA™ TPM 2.0 cryptoprocessor.

---

## 7. Integrated Honeytap Decoy PLC (Mock PLC)

`ics-guard` compiles and deploys an authentic, multi-threaded industrial honeytap decoy PLC (`shared/bin/mock_plc`) directly into industrial conduits:
* **Multi-Protocol Simulation:** Simultaneously binds and answers on Modbus TCP (`:502`), Siemens S7Comm (`:102`), and IEC 60870-5-104 (`:2404`).
* **Continuous Physical Dynamics:** Solves continuous thermal, pressure, and centrifugal vibration ODEs via an internal RK4 integration loop (`100 ms` step).
* **Automated Forensic Spooling:** When an adversary issues write commands (`FC05`, `FC06`, S7 `0x28/0x29`, IEC `COT=6`), the honeytap captures the full raw hex packet payload, timestamps, originating IP/port, and physical barrier margins into structured JSON spool archives (`/var/run/sentinel/honeynet_spool/exploit_*.json`).

---

## 8. Repository Layout & Component Architecture

```text
/home/kami/ics-guard/
├── CMakeLists.txt                       # Build definition (-O3 -march=native -fno-omit-frame-pointer)
├── Makefile                             # Lifecycle orchestration: build, test, bench, install, grid-up
├── cmake/
│   ├── IcsGuardConfig.cmake.in          # CMake package discovery export
│   └── ics_guard.pc.in                  # pkg-config export definition
├── include/ics_guard/
│   ├── ics_guard.hpp                    # Master umbrella C++20 header
│   ├── core/
│   │   ├── types.hpp                    # GuardStatus enums & Synchrophasor structures
│   │   └── tsc_clock.hpp                # Cycle-accurate TSC RDTSC calibration routines
│   ├── protocols/
│   │   ├── modbus_tcp.hpp               # Modbus MBAP & Function Code zero-alloc validator
│   │   ├── s7comm.hpp                   # Siemens S7Comm & COTP PDU validator
│   │   ├── iec104.hpp                   # IEC 60870-5-104 APCI/ASDU telecontrol validator
│   │   └── synchrophasor.hpp            # IEEE C37.118 frequency, ROCOF & THD validator
│   ├── defense/
│   │   ├── plant_ode.h                  # Continuous differential equations & Nagumo CBF headers
│   │   ├── cbf_safety_gate.hpp          # Formal Nagumo invariance gate (dh/dt + alpha*h >= 0)
│   │   └── actuator_airgap.hpp          # Sub-15 ns lock-free atomic safety tripwire latch
│   └── pipeline/
│       └── guard_engine.hpp             # Unified zero-allocation Tier-1 Industrial GuardEngine
├── src/
│   ├── core/tsc_clock.cpp
│   ├── protocols/{modbus_tcp.cpp, s7comm.cpp, iec104.cpp, synchrophasor.cpp}
│   ├── defense/{plant_ode.c, cbf_safety_gate.cpp, actuator_airgap.cpp}
│   └── pipeline/guard_engine.cpp
├── tools/
│   ├── sentinel_plugin/ics_guard_plugin.cpp  # Native ABI dissector for blackbox-sentinel eBPF daemon
│   ├── aryo_ics/main.cpp                     # Subcommand extension for `aryo ics ...`
│   ├── ics_guard_ctl/main.cpp                # Diagnostic and self-test utility
│   └── mock_plc/mock_plc.c                   # Standalone decoy PLC twin with plant ODE solvers
├── benchmarks/
│   └── bench_latency.cpp                     # 100,000-frame cycle-accurate latency benchmark (< 120 ns)
├── tests/
│   ├── test_modbus_validation.cpp            # Modbus FC whitelisting & write-lock unit tests
│   ├── test_s7_iec104_validation.cpp         # S7 CPU STOP & IEC-104 breaker trip unit tests
│   ├── test_cbf_invariance.cpp               # Runge-Kutta 4 & Nagumo barrier invariance tests
│   ├── test_sentinel_plugin.cpp              # Dynamic dlopen() plugin ABI integration test
│   └── test_ics_tier1_tier2_pipeline.cpp     # Tier-1 C++20 logic vs Tier-2 xinfer OpenVINO ONNX test
├── harnesses/                                # Hard-copied permanent research harnesses (no symlinks)
│   ├── ics_modbus_tamper.py
│   ├── ics_iec104_trip.py
│   ├── ics_s7_runaway.py
│   ├── ics_triton_sis.py
│   ├── ics_pmu_harmonics.py
│   └── ics_airgap_tripwire.py
├── apparatus_plugins/                        # Physical telemetry drivers for sentinel-matrix runtime
│   ├── synchrophasor.py                      # IEEE C37.118 power grid physics model
│   ├── industrial_thermal.py                 # FLIR 16x12 radiometric thermal matrix model
│   └── reactor_core.py                       # Exothermic chemical reaction vessel model
├── web/                                      # Micro-frontend plugin package (served via Nexus)
│   ├── manifest.json
│   └── industrial/
│       ├── industrial.js                     # 3 live apparatus displays + Industrial SCADA C2 tab
│       └── industrial.css
└── scenarios/production_master_grid/         # Full 17-container cyber-physical digital twin mesh
    ├── manifest.json
    ├── scenario.yaml
    ├── run_demo.sh
    ├── configs/
    │   ├── plc_register_map.json
    │   ├── sensor_attack_matrix.json
    │   ├── lab_plugins/industrial_ics.json   # OCP dynamic category definitions
    │   └── nodes/
    │       ├── node_01_substation_alpha.yaml # Substation Alpha (OpenVINO + Modbus/PMU)
    │       ├── node_02_hospital_pacs.yaml    # Hospital PACS (TensorRT + FLIR/LiDAR)
    │       └── node_03_refinery_plc.yaml     # Refinery Zone B (RKNN + S7Comm/Vibration)
    ├── models/                               # Verified INT8/FP32 neural models (.onnx + .data)
    └── pcaps/                                # Authentic ICS attack traces (Industroyer2, Stuxnet, Triton)
```

---

## 9. Compilation, Testing & Installation

### Build Requirements
* Modern C++20 and C11 compiler (`gcc-13+` or `clang-16+`).
* Linux Kernel 6.x / 7.x with `eBPF` and `AF_XDP` support.
* Core libraries installed system-wide: `libblackbox.so` (Blackbox Essential) and `libxinfer.so` (xInfer Essential).

```bash
cd /home/kami/ics-guard

# 1. Compile Release targets (-O3 -march=native -Wall -Wextra)
make build

# 2. Execute full verification test suite (100% pass required)
make test

# 3. Execute cycle-accurate hardware latency benchmark (< 120 ns target)
make bench

# 4. Install shared libraries, plugins, CLI bridges, and research harnesses
sudo make install

# 5. Synchronize artifacts with sentinel-matrix and sentinel-nexus
make sync-all
```

### Deployed System Artifacts
* `/usr/local/lib/libics_guard.so` & `libics_guard.a`
* `/usr/local/lib/blackbox/ics_guard_dissector_plugin.so` (Blackbox dynamic dissector path)
* `/usr/local/bin/aryo-ics` (Master CLI extension)
* `/usr/local/bin/ics-guard-ctl` (Diagnostic tool)
* `/usr/local/bin/mock_plc` (Honeytap PLC decoy)
* `/etc/sentinel/lab/harnesses/ics_*.py` & `/opt/sentinel-stack/harnesses/ics-*.py`

---

## 10. Operator CLI Operations (`aryo ics` & `aryo lab`)

The master CLI `aryo` automatically detects and delegates to `ics-guard`:

```bash
# Display extension status and capabilities
aryo ics --plugin-desc

# Verify protocol gate self-tests
aryo ics verify-modbus      # Modbus TCP FC03 read vs FC05 write lockout
aryo ics verify-s7          # Siemens S7Comm CPU STOP (0x29) interception
aryo ics verify-iec104      # IEC 60870-5-104 breaker trip (COT=6) interception
aryo ics verify-cbf         # Nagumo CBF thermal stability invariance evaluation
aryo ics airgap-status      # Inspect real-time hardware actuator air-gap latch

# Execute automated research evaluation harnesses (Sentinel-Lab)
aryo lab ics-modbus-tamper  # Modbus FC05 coil override vs illegal FC08 probe
aryo lab ics-iec104-trip    # Industroyer2 breaker trip attack evaluation
aryo lab ics-s7-runaway     # Stuxnet centrifuge overspin & DB write tamper
aryo lab ics-triton-sis     # Triconex TriStation logic tamper & thermal spike
aryo lab ics-pmu-harmonics  # Synchrophasor underfrequency & harmonic distortion
aryo lab ics-airgap-tripwire# Nagumo barrier margin & forward invariance audit
```

---

## 11. Production Master Grid Digital Twin (17 Containers)

`ics-guard` orchestrates a complete 17-container industrial digital twin mesh on isolated subnet `10.240.0.0/24`:

```bash
cd /home/kami/ics-guard

# Deploy the entire 17-node simulation mesh in the background
make grid-up

# Check container runtime health and IP/port bindings
make grid-status

# Stream real-time eBPF and inference telemetry from Substation Alpha
make grid-logs

# Dismantle simulation mesh and release all network bridges
make grid-down
```

### Digital Twin Network Matrix (`10.240.0.0/24`)

| Hostname / Service | IP Address | Host Exposed Ports | Subsystem & Deployed Role |
| :--- | :--- | :--- | :--- |
| **`nexus.matrix.internal`** | `10.240.0.10` | `9443`, `9444`, `50051` | Sentinel Nexus Command Plane + Industrial Web Plugin |
| **`forge.matrix.internal`** | `10.240.0.20` | — | Continuous Learning Daemon (`xinfer-forge`) |
| **`traffic.matrix.internal`** | `10.240.0.50` | — | Synthetic Wire Traffic & Attack Wave Streamer |
| **`monitor.matrix.internal`** | `10.240.0.60` | — | Real-Time Split-Panel Terminal UI (TUI) |
| **`adversary.matrix.internal`**| `10.240.0.99` | — | Red-Team Ingress Node (Nmap, Modbus poll, S7 tamper) |
| **`substation-01.matrix.internal`**| `10.240.0.101`| — | **Edge Sentry 01:** Substation Alpha (`INTEL_OPENVINO`) |
| **`hospital-02.matrix.internal`** | `10.240.0.102`| — | **Edge Sentry 02:** Hospital Facilities (`NVIDIA_TENSORRT`) |
| **`refinery-03.matrix.internal`** | `10.240.0.103`| — | **Edge Sentry 03:** Refinery Zone B (`ROCKCHIP_RKNN`) |
| **`camera.matrix.internal`** | `10.240.0.75` | `8554`, `8889` | Sensor: MediaMTX Radiometric RTSP Thermal Stream |
| **`vibration.matrix.internal`**| `10.240.0.76` | `15502:502` | Sensor: IFM Bearing & Agitator Vibration Probe |
| **`lidar.matrix.internal`** | `10.240.0.77` | `2368/udp` | Sensor: SICK Industrial Spatial LiDAR Scanner |
| **`power-meter.matrix.internal`**| `10.240.0.78` | `15501:502` | Sensor: Siemens PAC3200 Synchrophasor PMU |
| **`apparatus-synchrophasor`** | `10.240.0.131`| `18093:8090` | Apparatus: PMU Scope + Industroyer2 PCAP Streamer |
| **`apparatus-thermal`** | `10.240.0.132`| `18094:8090` | Apparatus: Radiometric FLIR + Triton SIS PCAP Streamer |
| **`apparatus-reactor`** | `10.240.0.133`| `18095:8090` | Apparatus: Exothermic Core + Stuxnet PCAP Streamer |
| **`plc.matrix.internal`** | `10.240.0.150`| `502`, `102`, `2404` | Decoy: Honeytap Decoy PLC Twin (Modbus/S7/IEC-104) |

### Web Mission Control Interface
Once deployed, browse to **`http://localhost:9443/`**:
* **Mission Control (Pane 01):** Inspects physical apparatus scopes matching active field nodes:
  * Selecting `Substation-01` displays the **Power Quality & Synchrophasor Scope** (`:18093`).
  * Selecting `Hospital-02` displays the **Radiometric Thermal Vision Camera** (`:18094`).
  * Selecting `Refinery-03` displays the **Exothermic Reaction Vessel Core** (`:18095`).
* **Sidebar Navigation:** Access the dedicated **"🏭 Industrial SCADA C2"** dashboard for fleet-wide telemetry, THD measurements, vessel pressure tracking, and on-demand malware replay bursts.

---

## 12. Regulatory Compliance & Standards Alignment

`ics-guard` automates continuous regulatory audit reporting via the Sentinel Nexus REST API:

### A. IEC 62443 (Industrial Cyber-Physical Systems Security)
* **IEC 62443-3-3 System Security Requirements:** Satisfies Foundational Requirements FR 3 (System Integrity) and FR 5 (Network Segmentation / Zone & Conduit boundary protection) via sub-microsecond in-kernel eBPF packet drops.
* **IEC 62443-4-2 Component Security Requirements:** Enforces local cryptoprocessor attestation (TPM 2.0) and software component verification (CycloneDX SBOM export).

### B. EU NIS2 Directive (Directive 2022/2555)
* **Article 21(2)(a) Risk Analysis & Asset Mapping:** Automated live enumeration of active OT field nodes and protocol routes.
* **Article 21(2)(b) Incident Handling & Sub-ms Mitigation:** Cryptographically verified mitigation latency SLAs ($< 0.84\,\mu\text{s}$) with automated in-kernel drop logging.
* **Article 21(2)(d) Supply Chain Security:** Mandatory OpenSSL SHA-256 digest validation of all incoming neural model weights and software extension packages.
* **Article 21(2)(h) Cryptographic Attestation:** Silicon-anchored hardware root-of-trust authentication for all telemetry and telecommand gateways.

---

## 13. Research Preprint & Authorship

* **Corporate Entity:** Aryorithm Technologies B.V. (Amsterdam, The Netherlands)
* **Founder & Chief Technology Officer:** Kamran Saberifard ([github.com/kamisaberi](https://github.com/kamisaberi))
* **Permanent Research DOI:** CERN / Zenodo: [`10.5281/zenodo.23598779`](https://doi.org/10.5281/zenodo.23598779)
* **License:** Proprietary / Commercial Licensing available from Aryorithm Technologies B.V.
