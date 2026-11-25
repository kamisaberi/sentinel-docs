# The 5-Tier Dependency DAG (How All 14 Repositories Connect)

To eliminate circular dependencies and support independent compilation, the Aryorithm ecosystem enforces a strict **unidirectional Directed Acyclic Graph (DAG)** from Tier 0 (Foundations) up to Tier 4 (Orchestration & C2):

| Tier | Repository | Primary Binary / Library | Depends On | Role in Ecosystem |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 0** | `sentinel-fs` | `libsentinelfs.so`, `sfs`, `sentinel_fs` | OS / OpenSSL | Sovereign storage hierarchy (`SENTINEL_ROOT`), `PathResolver`, SHA-256 `CasStore` |
| **Tier 0** | `blackbox-essential` | `libblackbox.so` | Linux eBPF / XDP | Line-rate packet drop engine (`< 0.84 µs`), AF_XDP multi-queue UMEM |
| **Tier 0** | `xinfer-essential` | `libxinfer.so` | OpenVINO / TRT / etc. | Universal zero-copy C++20 neural inference engine across 16 silicon targets |
| **Tier 1** | `blackbox-sentinel` | `sentinel`, `sentinel-ctl`, `sentinel-artifact` | Tier 0 | 4-Bus ingress (`AF_PACKET`, `AF_CAN`, `ShmRing`, `V4L2`), `PluginSupervisor`, `ModelRouter` |
| **Tier 1** | `xinfer-forge` | `forge-cli` | `xinfer-essential`, `sentinel-fs` | Continual self-supervised learning (Tabular MAE + InfoNCE), INT8 PTQ export |
| **Tier 2** | `ics-guard` | `libics_guard.so`, `aryo-ics`, `*_plugin.so` | Tier 0, Tier 1 ABI | Industrial SCADA (Modbus, S7, IEC-104, PMU) + RK4 ODE & Nagumo CBF |
| **Tier 2** | `ccsds-guard` | `libccsds_guard.so`, `aryo-aerospace`, `*_plugin.so` | Tier 0, Tier 1 ABI | UAV Swarms & Space (STANAG 4586, CCSDS 132/133, Rover Slip CBF) |
| **Tier 2** | `net-guard` | `libnet_guard.so`, `aryo-net`, `*_plugin.so` | Tier 0, Tier 1 ABI | Telco & FinTech (5G GTP-U, L2 GOOSE/SV, ITCH 5.0, O-RAN, PQC ML-KEM) |
| **Tier 2** | `motion-guard` | `libmotion_guard.so`, `aryo-motion`, `*_plugin.so` | Tier 0, Tier 1 ABI | Robotics (ISO 13849, EtherCAT L2, CAN-FD, ShmRing, Surgical TSN 802.1Qbv) |
| **Tier 2** | `vision-guard` | `libvision_guard.so`, `aryo-vision`, `*_plugin.so` | Tier 0, Tier 1 ABI | Edge Vision (4K RTSP, GigE GVCP, HIPAA ShmRing, DMS Gaze) |
| **Tier 3** | `sentinel-matrix` | `scenario_engine.py`, `apparatus-runtime` | `sentinel-fs` | Cyber-physical Docker digital twin orchestrator (reads SSFS Catalog, writes Workspaces) |
| **Tier 3** | `sentinel-lab` | Research Harnesses | Tier 0, Tier 2 | 14-D scientific ODE & Ames/Nagumo CBF verification harnesses |
| **Tier 4** | `sentinel-nexus` | `sentinel-nexus`, `nexus-ctl` | Tier 0 (`sentinel-fs`) | Sovereign Fleet C2 (gRPC `:50051`, HTTP `:9443`, SSE `:9444`, Web UI) |
| **Tier 4** | `sentinel-stack` | `aryo` CLI, 50 Scenario Scripts | Tier 0–3 | Master CLI router, PKI provisioning, 50 recipes, `.aryopack` exporter |
