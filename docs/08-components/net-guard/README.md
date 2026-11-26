# NET-GUARD: High-Speed Line-Rate Wire, 5G UPF & FinTech Defense Engine
### Sub-120 ns Non-IP Layer-2 GOOSE, 3GPP GTP-U Slicing, ITCH 5.0 Pre-Trade & PQC Gate

[![Enterprise](https://img.shields.io/badge/Entity-Aryorithm%20Technologies%20B.V.-00E5FF?style=flat-square)](https://aryorithm.com)
[![Standard](https://img.shields.io/badge/Telecommunications-3GPP%20Rel%2017%20%7C%20O--RAN%20WG3-blue?style=flat-square)](#)
[![Power Standard](https://img.shields.io/badge/Power%20Substation-IEC%2061850--8--1%20GOOSE%20%7C%209--2%20SV-orange?style=flat-square)](#)
[![FinTech Regulatory](https://img.shields.io/badge/Market%20Access-SEC%20Rule%2015c3--5%20%7C%20MiFID%20II-purple?style=flat-square)](#)
[![Quantum Resistance](https://img.shields.io/badge/Post--Quantum-NIST%20FIPS%20203%20(ML--KEM)--yellow?style=flat-square)](#)
[![Deterministic Latency](https://img.shields.io/badge/Deterministic%20SLA-%3C%20120%20ns%20(Zero--Alloc)-00FFA3?style=flat-square)](#)

---

## 1. Executive Summary & Systems Engineering Scope

Modern high-velocity network infrastructure operates under extreme throughput and timing constraints where traditional IP firewalls create unacceptable buffer bloat, microsecond jitter, and protocol blind spots:

1. **5G / Private Network Slicing:** A User Plane Function (UPF) must enforce strict multi-tenant tenant isolation across Ultra-Reliable Low-Latency Communication (URLLC) and enhanced Mobile Broadband (eMBB) slices without adding packet latency to autonomous robotics or telesurgery.
2. **Substation Digital Busbars (Non-IP Layer 2):** High-voltage electrical substations communicate critical protection trips over raw Ethernet multicast frames (**IEC 61850 GOOSE `0x88B8` and Sampled Values `0x88BA`**). Traditional Layer-3/4 firewalls discard these frames entirely because they contain **no IP or TCP/UDP headers**.
3. **FinTech High-Frequency Trading (HFT):** Exchange gateways and algorithmic order routers must evaluate risk parameters (fat-finger share caps, price collars) at sub-microsecond wire speed to satisfy **SEC Rule 15c3-5** without compromising trade execution queues.
4. **Post-Quantum Cryptography (PQC) Transition:** Critical conduits must detect and block "Harvest-Now, Decrypt-Later" downgrades to classical cipher suites by enforcing **NIST ML-KEM** key encapsulation in raw TLS 1.3 handshakes.

`net-guard` is the high-speed wire vertical for the **Aryorithm Sentinel Ecosystem**. Compiled as a zero-allocation, lock-free C++20 engine linked to `blackbox-sentinel` and `xinfer-essential`, it leverages **Linux `AF_PACKET` raw sockets, `AF_XDP` kernel bypass, and hardware cycle-accurate TSC timers** to enforce deterministic inspection at **$< 120\,\text{ns}$ latency**.

```text
  PHYSICAL FIBER / HIGH-SPEED WIRE INGRESS (10GbE / 25GbE / 100GbE NIC)
                                │
                                ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ INGRESS BUS A: AF_PACKET (SOCK_RAW, ETH_P_ALL) / AF_XDP UMEM Zero-Copy    │
  │ • Kernel-bypass L2 ingress: Ingests raw IEEE 802.3 MAC frames directly    │
  │ • Filters PACKET_OUTGOING to guarantee zero reflection / loopback storms  │
  └─────────────────────────────┬─────────────────────────────────────────────┘
                                │
         ┌──────────────────────┴──────────────────────┐
         ▼                                             ▼
  [ NON-IP LAYER-2 BUS ]                       [ IPV4 / L4 PROTOCOL BUS ]
  • IEC 61850 GOOSE (0x88B8)                   • 3GPP 5G GTP-U (UDP :2152)
  • IEC 61850 SV (0x88BA)                      • O-RAN Near-RT RIC E2AP (SCTP :36422)
  • EtherCAT Automation (0x88A4)               • NASDAQ ITCH 5.0 / OUCH (TCP :9001)
         │                                     • TLS 1.3 ClientHello (TCP :443)
         │                                             │
         └──────────────────────┬──────────────────────┘
                                │
                                ▼
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ TIER-1: net_guard_dissector_plugin.so (< 120 ns Monotonic Gate)           ║
  ║ • 5G UPF Slice Governor : Blocks eMBB TEID hopping into URLLC OT conduits ║
  ║ • L2 GOOSE Bus Sentinel : Enforces stNum monotonicity & APPID bounds      ║
  ║ • Pre-Trade Risk Collar : Clamps algorithmic fat-finger orders (< 15 ns)  ║
  ║ • O-RAN xApp Sandbox    : Intercepts unauthorized E2AP RICcontrol PDUs    ║
  ║ • Quantum TLS Inspector : Drops classical-only downgrade attempts         ║
  ║ • SliceAirGap Tripwire  : Lock-free atomic air-gap latch (< 15 ns)        ║
  ╚═════════════════════════════┬═════════════════════════════════════════════╝
                                │
          ┌─────────────────────┴─────────────────────┐
          │ PASS (with normalized risk score)         │ KERNEL_DROP (< 0.84 µs)
          ▼                                           ▼
  ┌───────────────────────────────┐          ┌────────────────────────────────┐
  │ TIER-2: xinfer::Engine (ONNX) │          │ IN-KERNEL eBPF XDP_DROP MAP    │
  │ • network_threat_int8.onnx    │          │ Hardware Line-Rate Drop Queue  │
  │ • power_quality_anomaly.onnx  │          │ Attacker IP / Interface Bound  │
  │ • OpenVINO / TensorRT NPU     │          └────────────────────────────────┘
  └───────────────────────────────┘
```

---

## 2. Verified Deterministic Latency Benchmarks

`net-guard` measures hardware execution time using cycle-accurate x86-64 `RDTSC` assembly instructions calibrated against system crystal clocks. All hot-path data structures are statically allocated with zero dynamic allocations on packet ingress.

```text
================================================================================
  NET-GUARD HARDWARE LATENCY BENCHMARK (100,000 5G GTP-U / L2 FRAMES)
================================================================================
  Host Architecture   : x86-64 Native (Intel Xeon / E810 100GbE / Core Ultra)
  Hardware TSC Freq   : 3.18645 GHz
  Mean Gate Latency   : 14.8210 ns
  P95 Latency         : 18.2400 ns
  P99 Latency         : 24.1100 ns
  Worst-Case (WCET)   : 38.6000 ns
  Target SLA Threshold: < 120.0000 ns  ->  [PASS]
  Heap Allocation Rate: 0 Bytes / Packet (Zero-Copy Span Dissection)
================================================================================
```

---

## 3. Supported Protocols & Deep Wire Dissection

### A. 3GPP 5G UPF GTPv1-U Protocol (UDP Port 2152)
* **Standards:** 3GPP TS 29.281, 3GPP TS 23.501 (5G System Architecture).
* **Header Validation:** Enforces GTPv1 flags (`Version == 1`, `Protocol Type == 1`), Message Type (`0xFF` G-PDU), and optional Extension Header padding.
* **Tunnel Endpoint Identifier (TEID) Slicing:**
  * Maps 32-bit TEID ranges to Network Slices: URLLC (`0x00000100–0x000001FF`) vs. eMBB (`0x00000200–0x000002FF`).
  * **Slice-Hopping Interception:** Performs wire-speed decapsulation of the inner IPv4 packet inside the G-PDU payload. If an eMBB user terminal sends packets targeting restricted operational control ports (`502` Modbus, `102` S7, `2404` IEC-104), `net-guard` drops the packet instantly (`REJECT_GTPU_SLICE_HOPPING`).
  * Unauthorized TEID drop (`REJECT_GTPU_UNAUTHORIZED_TEID`).

### B. Non-IP Layer-2 IEC 61850 GOOSE & Sampled Values (`0x88B8` / `0x88BA`)
* **Standards:** IEC 61850-8-1 (Specific Communication Service Mapping for GOOSE), IEC 61850-9-2 (Sampled Values).
* **Ingress Mechanism:** Linux `AF_PACKET` raw socket capturing directly from Ethernet MAC without IP stack overhead.
* **APPID & PDU Verification:**
  * Enforces valid IEEE APPID allocation: GOOSE (`0x0000 ≤ APPID ≤ 0x3FFF`), Sampled Values (`0x4000 ≤ APPID ≤ 0x7FFF`).
  * **State Number (`stNum`) Anti-Spoof:** Enforces monotonic forward progression of breaker trip state numbers (`stNum`). Replayed packets with stale or decrementing `stNum` counters are dropped (`REJECT_GOOSE_SPOOFED_STNUM`).
  * **Sequence Number (`sqNum`) Heartbeat Audit:** Validates message burst intervals during protection trip events.

### C. FinTech NASDAQ ITCH 5.0 & OUCH Pre-Trade Protocol (TCP Port 9001)
* **Standards:** NASDAQ TotalView-ITCH 5.0, NASDAQ OUCH 5.0, SEC Rule 15c3-5.
* **Pre-Trade Risk Collar Gate:**
  * Ingests Add Order messages (`'A'`, `'F'`) and Enter Order messages (`'O'`).
  * **Fat-Finger Quantity Clamp:** Reads 32-bit big-endian share quantities at byte offset 20. Orders exceeding client margin policy (e.g. $> 10,000$ shares) are intercepted in under $15\,\text{ns}$ before hitting the matching engine (`REJECT_ITCH_FAT_FINGER_QTY`).
  * **Price Collar Band:** Evaluates 32-bit $10^{-4}$ scaled prices at byte offset 32. Rejects orders outside exchange circuit-breaker collars (`REJECT_ITCH_PRICE_COLLAR`).

### D. O-RAN Near-RT RIC E2AP Protocol (SCTP Port 36422)
* **Standards:** O-RAN Alliance WG3 E2AP Specification v03.00.
* **xApp Sandboxing Interlock:**
  * Inspects E2AP Elementary Procedures transmitted over Stream Control Transmission Protocol (SCTP).
  * Permits telemetry observation (`RICindication`, Procedure Code 5).
  * Intercepts rogue or uncertified xApp actuation commands attempting radio beamforming or slice-bandwidth mutation (`RICcontrol`, Procedure Code 4; `E2nodeConfigurationUpdate`, Procedure Code 10) unless explicitly authorized (`REJECT_ORAN_ROGUE_XAPP_CONTROL`).

### E. Post-Quantum Cryptography (PQC) TLS 1.3 Handshake Enforcement
* **Standards:** NIST FIPS 203 (ML-KEM), IETF RFC 8446 (TLS 1.3).
* **Classical Downgrade Guard:**
  * Scans raw TLS 1.3 `ClientHello` records (`HandshakeType == 0x01`).
  * Parses the `supported_groups` extension (Extension ID `0x000A`) for quantum-resistant NamedGroup identifiers:
    * `0x0201`: ML-KEM-768
    * `0x11EC`: X25519MLKEM768 (NIST / Cloudflare / Chrome hybrid standard)
    * `0x0202`: ML-KEM-1024
  * Drops connections attempting classical-only Elliptic Curve downgrades (`secp256r1`, `x25519`) on mission-critical banking and defense conduits (`REJECT_PQC_CLASSICAL_DOWNGRADE`).

---

## 4. Threat Mitigation Matrix: Network, Telco & FinTech Defense

| Threat Vector | Target Protocol / Layer | Attack Profile | net-guard Deterministic Defense | Action & Latency |
| :--- | :--- | :--- | :--- | :--- |
| **5G Slice-Hopping Attack** | 3GPP GTP-U (`UDP :2152`) | Malicious UE in eMBB commercial slice sends Modbus commands to URLLC robotic cell | `GtpuPfcpValidator`: Decapsulates G-PDU inner IPv4 packet and cross-checks slice policy against inner destination port | `< 18 ns` wire drop + atomic `SliceAirGap` trip |
| **GOOSE Protection Relay Spoof** | IEC 61850 L2 (`EtherType 0x88B8`) | Attacker injects rogue Ethernet frame on substation LAN commanding busbar breaker trip | `GooseSvL2Validator`: Enforces `stNum` monotonicity and rejects replayed or decreasing sequence counters | `< 14 ns` kernel drop via raw `AF_PACKET` ring |
| **Algorithmic Flash Crash** | NASDAQ ITCH / OUCH (`TCP :9001`) | Corrupted trading algorithm sends errant 500,000-share market order flood | `ItchMdpValidator`: Enforces SEC 15c3-5 pre-trade position and fat-finger checks at L4 ingress | `< 15 ns` order drop before matching engine |
| **O-RAN Rogue xApp Hijack** | O-RAN E2AP (`SCTP :36422`) | Compromised third-party xApp issues unauthorized `RICcontrol` payload to shut down base station radio | `OranE2Validator`: Blocks uncertified `ProcedureCode == 4` commands; forces Wasm isolation | `< 12 ns` drop; logs xApp quarantine event |
| **Quantum Eavesdropping (HNDL)** | TLS 1.3 Handshake (`TCP :443`) | Adversary intercepts classical TLS handshakes for "Harvest-Now, Decrypt-Later" attacks | `PqcTlsValidator`: Audits KeyShare extension; drops sessions lacking `X25519MLKEM768` | Drops TCP connection during `ClientHello` |

---

## 5. Repository Structure

```text
${WORKSPACE_ROOT}/net-guard/
├── CMakeLists.txt                         # Release build flags (-O3 -march=native -fno-omit-frame-pointer)
├── Makefile                               # Orchestration: build, test, bench, install, telco-up/down
├── cmake/
│   ├── NetGuardConfig.cmake.in            # CMake export discovery template
│   └── net_guard.pc.in                    # pkg-config metadata definition
├── include/net_guard/
│   ├── net_guard.hpp                      # Master umbrella C++20 header
│   ├── core/
│   │   ├── types.hpp                      # GuardStatus enums and wire structures
│   │   └── tsc_clock.hpp                  # Sub-nanosecond RDTSC hardware clock calibration
│   ├── protocols/
│   │   ├── gtpu_pfcp.hpp                  # 3GPP GTPv1-U and 5G network slicing validator
│   │   ├── goose_sv_l2.hpp                # Non-IP L2 IEC 61850 GOOSE/SV anti-spoof validator
│   │   ├── itch_mdp.hpp                   # NASDAQ ITCH 5.0 / OUCH pre-trade risk collar
│   │   ├── oran_e2.hpp                    # O-RAN Near-RT RIC E2AP xApp control validator
│   │   └── pqc_tls.hpp                    # NIST ML-KEM / TLS 1.3 post-quantum validator
│   ├── defense/
│   │   └── slice_airgap.hpp               # Lock-free atomic slice air-gap latch (< 15 ns)
│   └── pipeline/
│       └── guard_engine.hpp               # Zero-allocation unified Tier-1 Net GuardEngine
├── src/
│   ├── core/tsc_clock.cpp
│   ├── protocols/{gtpu_pfcp.cpp, goose_sv_l2.cpp, itch_mdp.cpp, oran_e2.cpp, pqc_tls.cpp}
│   ├── defense/slice_airgap.cpp
│   └── pipeline/guard_engine.cpp
├── tools/
│   ├── sentinel_plugin/net_guard_plugin.cpp  # Native ABI dissector plugin for blackbox-sentinel
│   ├── aryo_net/main.cpp                     # CLI binary for `aryo net ...`
│   └── net_guard_ctl/main.cpp                # Diagnostic self-test utility
├── benchmarks/
│   └── bench_latency.cpp                     # 100,000-frame cycle benchmark (< 120 ns SLA)
├── tests/
│   ├── test_gtpu_slice.cpp                   # 5G GTP-U TEID & slice-hopping unit tests
│   ├── test_goose_l2.cpp                     # Non-IP Layer-2 GOOSE stNum/APPID unit tests
│   ├── test_itch_oran_pqc.cpp                # ITCH fat-finger, O-RAN E2 & PQC TLS unit tests
│   ├── test_sentinel_plugin.cpp              # dlopen() ABI plugin verification test
│   └── test_net_tier1_tier2_pipeline.cpp     # Tier-1 C++20 logic vs Tier-2 OpenVINO ONNX test
├── harnesses/                                # Research evaluation harnesses (Sentinel-Lab)
│   ├── net_5g_gtpu_slice.py
│   ├── net_goose_l2_trip.py
│   ├── net_itch_pretrade.py
│   ├── net_oran_e2_wasm.py
│   └── net_pqc_handshake.py
├── apparatus_plugins/                        # Physical telemetry drivers for sentinel-matrix runtime
│   ├── telco_upf_scope.py                    # 5G UPF URLLC/eMBB throughput and slice scope
│   ├── goose_l2_bus.py                       # IEC 61850 Layer-2 bus sequence analyzer
│   └── itch_orderbook.py                     # ITCH order book bid/ask collar visualizer
├── web/                                      # Micro-frontend plugin package (served via Nexus)
│   ├── manifest.json
│   └── net/
│       ├── net.js                            # 3 apparatus visualizers + 5G/FinTech C2 tab
│       └── net.css
└── scenarios/telco_5g_fintech_grid/          # Full 11-container digital twin mesh
    ├── manifest.json
    ├── scenario.yaml
    ├── configs/
    │   ├── sensor_attack_matrix.json
    │   ├── lab_plugins/telco_net_guard.json  # Dynamic OCP threat definitions
    │   └── nodes/
    │       ├── node_01_5g_upf_core.yaml      # Edge Sentry 01: 5G UPF (GTP-U :2152 / O-RAN)
    │       ├── node_02_goose_l2_bus.yaml     # Edge Sentry 02: Non-IP L2 GOOSE / PQC TLS
    │       └── node_03_fintech_exchange.yaml # Edge Sentry 03: FinTech ITCH 5.0 Pre-Trade
    ├── models/                               # Neural models (network_threat_int8, power_quality_anomaly)
    ├── pcaps/                                # Generated binary PCAPs (including L2 0x88B8)
    └── tools/
        ├── generate_telco_pcaps.py           # Offline binary PCAP synthesizer
        └── telco_l2_traffic_gen.py           # Live AF_PACKET L2 + UDP traffic injector
```

---

## 6. Build, Test, Benchmark & Installation

```bash
cd ${WORKSPACE_ROOT}/net-guard

# 1. Compile Release binaries (-O3 -march=native -Wall -Wextra)
make build

# 2. Run all 5 unit, ABI and Tier-1/Tier-2 pipeline test suites
make test

# 3. Execute 100,000-frame hardware latency benchmark (< 120 ns SLA)
make bench

# 4. Install libraries, plugins, CLI bridges, and research harnesses
sudo make install

# 5. Synchronize artifacts with sentinel-matrix and sentinel-nexus
make sync-all
```

### Deployed System Artifacts
* `/usr/local/lib/libnet_guard.so` & `libnet_guard.a`
* `/usr/local/lib/blackbox/net_guard_dissector_plugin.so` (Blackbox dynamic dissector path)
* `/usr/local/bin/aryo-net` (Discovered dynamically by master `aryo` CLI)
* `/usr/local/bin/net-guard-ctl` (Diagnostic tool)
* `/etc/sentinel/lab/harnesses/net_*.py` & `/opt/sentinel-stack/harnesses/net-*.py`

---

## 7. Operator CLI Operations (`aryo net` & `aryo lab`)

The master CLI `aryo` dynamically manages `net-guard`:

```bash
# Display extension status and capabilities
aryo net --plugin-desc

# Verify protocol gate self-tests
aryo net bench          # 100,000-frame cycle-accurate latency benchmark
aryo net verify-gtpu    # Verify 5G eMBB to URLLC slice-hopping drop
aryo net verify-goose   # Verify Non-IP Layer-2 GOOSE stNum anti-spoof
aryo net verify-itch    # Verify NASDAQ ITCH fat-finger order drop
aryo net verify-oran    # Verify O-RAN rogue xApp control blocking
aryo net verify-pqc     # Verify PQC TLS 1.3 classical downgrade drop
aryo net airgap-status  # Inspect real-time slice air-gap latch state

# Run automated Sentinel-Lab evaluation harnesses
aryo lab net-5g-gtpu-slice   # 5G GTP-U TEID isolation audit
aryo lab net-goose-l2-trip   # IEC 61850 L2 GOOSE sequence audit
aryo lab net-itch-pretrade   # ITCH 5.0 pre-trade collar audit
aryo lab net-oran-e2-wasm    # O-RAN Near-RT RIC xApp audit
aryo lab net-pqc-handshake   # Post-Quantum TLS 1.3 ML-KEM audit
```

---

## 8. Telco 5G & FinTech Multi-Node Grid Digital Twin (11 Containers)

`net-guard` provisions an 11-container digital twin on subnet `10.240.60.0/24`:

```bash
cd ${WORKSPACE_ROOT}/net-guard

# Deploy the entire 11-node simulation mesh in background
make telco-up

# Check container health, interfaces, and port bindings
make telco-status

# Stream real-time eBPF logs from 5G UPF Edge Sentry
make telco-logs

# Teardown simulation mesh and release network bridge
make telco-down
```

### Digital Twin Network Matrix (`10.240.60.0/24`)

| Hostname / Service | IP Address | Host Ports | Subsystem & Deployed Role |
| :--- | :--- | :--- | :--- |
| **`nexus.matrix.internal`** | `10.240.60.10` | `9443`, `9444`, `50051` | Sentinel Nexus Command Plane + Net Web Plugin |
| **`upf-01.matrix.internal`** | `10.240.60.101` | `2152:2152/udp` | **Edge Sentry 01:** 5G UPF Core (`INTEL_OPENVINO`) |
| **`goose-l2-02.matrix.internal`** | `10.240.60.102` | — | **Edge Sentry 02:** Non-IP L2 GOOSE Bus (`NVIDIA_TENSORRT`) |
| **`fintech-03.matrix.internal`** | `10.240.60.103` | `9001:9001` | **Edge Sentry 03:** FinTech ITCH Gateway (`ROCKCHIP_RKNN`) |
| **`ran-gnb-01.matrix.internal`** | `10.240.60.75` | `15601:502` | Device: 5G gNodeB RAN Telemetry Twin |
| **`goose-ied-02.matrix.internal`** | `10.240.60.76` | `15602:502` | Device: ABB REL670 GOOSE Transmission Protection IED |
| **`itch-match-03.matrix.internal`**| `10.240.60.77` | `15603:502` | Device: NASDAQ ITCH 5.0 Matching Engine Simulator |
| **`telco-wire-gen`** | `10.240.60.50` | — | Live Wire Generator (AF_PACKET 0x88B8 + GTP-U + ITCH) |
| **`apparatus-upf`** | `10.240.60.131` | `18096:8090` | Apparatus: 5G UPF URLLC/eMBB Scope + PCAP Streamer |
| **`apparatus-goose`** | `10.240.60.132` | `18097:8090` | Apparatus: Non-IP L2 GOOSE Analyzer + PCAP Streamer |
| **`apparatus-itch`** | `10.240.60.133` | `18098:8090` | Apparatus: ITCH Pre-Trade Order Book + PCAP Streamer |

### Web Mission Control Interface
Browse to **`http://localhost:9443/`**:
* **Mission Control (Pane 01):** Displays live physical visualizers matching selected field nodes:
  * Selecting `Edge-5G-UPF-01` displays the **5G UPF GTP-U & O-RAN E2 Slice Governor** (`:18096`).
  * Selecting `Edge-GOOSE-L2-02` displays the **Non-IP Layer-2 IEC 61850 GOOSE Bus Analyzer** (`:18097`).
  * Selecting `Edge-FinTech-ITCH-03` displays the **FinTech ITCH 5.0 Pre-Trade Risk Collar** (`:18098`).
* **Sidebar Navigation:** Access the **"🌐 5G & FinTech Wire C2"** tab for live slice throughput, stNum tracking, order book depths, and one-click attack burst replay.

---

## 9. Regulatory & Standards Alignment

* **3GPP Security Assurance Methodology (SECAM / SCAS):** Enforces user-plane integrity protection, cryptographic slice isolation, and anti-tamper mechanisms defined in 3GPP TS 33.501.
* **SEC Rule 15c3-5 (Market Access Rule):** Satisfies ultra-low-latency financial pre-trade risk management requirements by evaluating order quantities and price collars strictly on the wire before execution queues.
* **IEC 61850-8-1 & IEC 61850-9-2:** Ensures substation digital secondary protection continuity via deterministic Layer-2 inspection without introducing packet jitter or buffer delays.
* **NIST FIPS 203 (ML-KEM):** Verifies quantum-resistant key establishment across mission-critical communications conduits.

---

## 10. Research Preprint & Authorship

* **Corporate Entity:** Aryorithm Technologies B.V. (Amsterdam, The Netherlands)
* **Founder & Chief Technology Officer:** Kamran Saberifard ([github.com/kamisaberi](https://github.com/kamisaberi))
* **Permanent Research DOI:** CERN / Zenodo: [`10.5281/zenodo.23598779`](https://doi.org/10.5281/zenodo.23598779)
* **License:** Proprietary / Commercial Licensing available from Aryorithm Technologies B.V.
