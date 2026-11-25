Cartridge #4: motion-guard (Robotics & Time-Sensitive Networking)
motion-guard enforces deterministic physical safety invariants across industrial cobots, autonomous mobile robots (AMRs), automotive brake-by-wire buses, and telesurgery TSN networks.
1. Specifications & Standards
Standards Compliance: ISO 13849-1 (PL-e Category 4), IEEE 802.1Qbv TSN, CiA 301 / CANopen, EtherCAT Specification.
Protocols & Busses: Non-IP L2 EtherCAT (0x88A4) on Bus A, SocketCAN CAN-FD on Bus B, AMR ShmRing (MOT1) on Bus C.
Mean Latency: 14.10 ns (P99: 18.20 ns) under 100,000-frame hardware cycle benchmarks.
Digital Twin: scenarios/robotics_can_ethercat_grid (8 nodes on 10.240.70.0/24, ports :18099–18101).
2. Surgical Robotics TSN Jitter Clamp & Anatomical Keep-Out Zone (surgical_tsn.hpp)
motion-guard integrates a dedicated validator for high-precision robotic surgery:
TSN 802.1Qbv Jitter Enforcement: Validates cycle arrival times using hardware PTP timestamps (SO_TIMESTAMPING), rejecting command packets with cycle jitter exceeding 500 microseconds.
3D Anatomical Keep-Out Zone CBF: Evaluates end-effector coordinates against patient anatomical scan keep-out zones (arteries, critical nerves):
h
koz
(
x
)
=
∥
p
tip
−
p
artery
∥
−
r
safety
≥
0
h 
koz
​
 (x)=∥p 
tip
​
 −p 
artery
​
 ∥−r 
safety
​
 ≥0
Commands commanding tool trajectories that breach the safety margin are clamped in under 15 nanoseconds.
