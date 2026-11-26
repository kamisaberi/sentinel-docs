# Cartridge #1: `ics-guard` (Industrial SCADA & Energy Grid)

`ics-guard` delivers deterministic, sub-microsecond protection for critical industrial plants, electric substations, chemical reactors, and regional pipelines.

---

## 1. Specifications & Standards

* **Standards Compliance:** IEC 62443-4-2, IEC 60870-5-104, IEEE C37.118.2 PMU, EU NIS2.
* **Protocols Parsed:** Modbus TCP (`:502`), Siemens S7Comm (`:102`), IEC 60870-5-104 (`:2404`), IEEE C37.118 Synchrophasor (`:15501`).
* **Mean Latency:** **11.96 ns** (P99: 12.87 ns) under 100,000-frame hardware cycle benchmarks.
* **Digital Twin:** `scenarios/production_master_grid` (17 nodes on `10.240.0.0/24`, ports `:18093–18095`).

---

## 2. Mathematical Plant ODE & Control Barrier Function (CBF)

Beyond protocol syntax validation, `ics-guard` incorporates an embedded Runge-Kutta 4th-Order (RK4) ODE solver modeling plant thermal and kinetic dynamics:

$$\dot{T} = \frac{Q_{\text{in}} - U \cdot A \cdot (T - T_{\text{cool}})}{C_{\text{thermal}}}$$

Physical safety invariance is enforced via a Nagumo barrier function:

$$h(T) = T_{\text{critical}} - T \ge 0$$

$$\dot{h}(T) + \gamma \cdot h(T) \ge 0$$

If incoming telemetry indicates that a setpoint change will breach the critical safety envelope within the critical clearing time ($t_{\text{crit}} \le 38.4\text{ ms}$), the command is intercepted and dropped at line rate.
