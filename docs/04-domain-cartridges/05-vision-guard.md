Cartridge #5: vision-guard (Air-Gapped Optical Ingress & Privacy)
vision-guard protects air-gapped camera feeds, factory automation vision cameras, automotive driver monitoring sensors, and hospital surgical imaging streams.
1. Specifications & Standards
Standards Compliance: HIPAA Security Rule (Zero Cloud Retention), ONVIF Profile S/T, GigE Vision 2.0 (GVCP/GVSP), Euro NCAP DMS 2026.
Protocols & Busses: 4K RTSP (:8554) on Bus A, GVCP (:3956) on Bus A, HIPAA ShmRing (VIS1) on Bus C, V4L2 / MIPI-CSI2 on Bus D.
Mean Latency: 16.30 ns (P99: 20.80 ns) under 100,000-frame hardware cycle benchmarks.
Digital Twin: scenarios/vision_edge_grid (8 nodes on 10.240.80.0/24, ports :18102–18104).
2. Automotive In-Cabin DMS Gaze & Drowsiness Validator (dms_gaze.hpp)
vision-guard validates driver state directly from raw V4L2 camera buffers without requiring high-power external neural accelerators (< 5W envelope):
PERCLOS Metric: Monitors percentage of eyelid closure over time.
Constant-Time 
O
(
64
)
O(64)
 Strided Luma Inspection: Evaluates illumination saturation directly on Bus D memory frames to detect optical blinding lasers or infrared dazzle attacks in real time.
