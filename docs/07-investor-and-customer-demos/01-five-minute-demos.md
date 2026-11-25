# Turnkey 5-Minute Digital Twin Demonstration Playbooks

These structured playbooks allow founders, sales engineers, and partners to demonstrate Blackbox Sentinel's sub-microsecond defense capabilities live before investors, enterprise CISOs, and pilot partners.

---

## Demo Playbook 1: Drinking Water Chemical Dosing Attack (`ics-guard`)

**Objective:** Prove that Sentinel intercepts a sophisticated Modbus setpoint injection attack that bypasses traditional IT firewalls, without causing plant downtime.

### Step-by-Step Execution:
1. **Launch the Digital Twin Mesh (60 Seconds):**
   ```bash
   aryo scenario provision 05_drinking_water_dosing_guard --up
   ```
2. **Open the Mission Control Command Center:**
   Navigate to `http://localhost:9443` in the browser. Show the 9 running nodes on the `10.240.105.0/24` subnet, live telemetry streams, and the active Modbus pipeline.
3. **Trigger Hostile Chemical Over-Dosing:**
   In another terminal, simulate an unauthorized setpoint write attempt:
   ```bash
   aryo ics verify-modbus
   ```
4. **Observe Sub-Microsecond Interception:**
   Point to the Mission Control dashboard:
   * The anomalous command is rejected by the **Tier 1 Reflex Gate in 11.96 ns**.
   * The hostile IP is automatically committed to the **eBPF XDP Drop Map** (`0.84 µs`).
   * The nominal water dosing flow continues uninterrupted with zero packet jitter.
5. **Clean Teardown:**
   ```bash
   aryo scenario down 05_drinking_water_dosing_guard
   ```

---

## Demo Playbook 2: Tactical UAV Swarm Telecommand Hijacking (`ccsds-guard`)

**Objective:** Demonstrate sub-50 ns kinematic telecommand verification during a live drone swarm waypoint spoofing attack.

### Step-by-Step Execution:
1. **Launch the Tactical Swarm Mesh:**
   ```bash
   aryo aerospace sim-combat-grid
   ```
2. **Inspect the 3D Tactical Combat Canvas:**
   Open `http://localhost:9443` and view the 3-node autonomous UAV swarm mesh communicating over NATO STANAG 4586 and CCSDS 132/133.
3. **Execute Telecommand Spoofing Test:**
   ```bash
   aryo aerospace verify-stanag
   aryo aerospace verify-ccsds
   ```
4. **Highlight the Key Metrics to Stakeholders:**
   * **Kinematic Teleport Rejection:** Waypoint changes with impossible acceleration profiles (> 50 m/s²) are rejected in **23.77 ns**.
   * **Hardware Air-Gap Tripping:** The actuator latch disconnects the physical control line before the flight controller processes the frame.
5. **Teardown Mesh:**
   ```bash
   aryo aerospace sim-combat-grid-down
   ```
