Cartridge #2: ccsds-guard (Aerospace & Autonomous UAV Swarms)
ccsds-guard protects autonomous drone swarms, defense datalinks, satellite downlinks, and planetary exploration rovers against telecommand hijacking and spoofing.
1. Specifications & Standards
Standards Compliance: NATO STANAG 4586 (DLI), CCSDS 133.0-B-2 (Space Data Link Security), CCSDS 132.0-B-3.
Protocols Parsed: STANAG 4586 DLI over UDP, CCSDS TC Frame, CCSDS Space Packet Protocol.
Mean Latency: 23.77 ns (P99: 26.60 ns) under 100,000-frame hardware cycle benchmarks.
Digital Twin: scenarios/tactical_uav_swarm_combat_grid (6 nodes on 10.240.52.0/24, ports :18091–18092).
2. Planetary Rover Regolith Slip & Rollover CBF (rover_slip_cbf.hpp)
ccsds-guard implements the Burckhardt granular regolith friction model 
μ
(
λ
)
μ(λ)
:
μ
(
λ
)
=
c
1
⋅
(
1
−
e
−
c
2
λ
)
−
c
3
λ
μ(λ)=c 
1
​
 ⋅(1−e 
−c 
2
​
 λ
 )−c 
3
​
 λ
It models continuous pitch and roll slope dynamics via Runge-Kutta 4th-order integration and clamps hostile drive telecommands using a Nagumo critical rollover barrier:
h
tip
(
θ
)
=
θ
critical
−
∥
θ
∥
≥
0
h 
tip
​
 (θ)=θ 
critical
​
 −∥θ∥≥0
Telecommands that would cause rover wheel spinout on granular regolith or vehicle rollover on steep inclines are rejected in under 25 nanoseconds.
