# Control Plane: Fleet C2 (`sentinel-nexus`), Continual Learning (`xinfer-forge`) & Lab

The Control Plane supervises deployed nodes, coordinates collective defense threat intelligence, and continually adapts neural detection baselines without cloud egress.

---

## 1. Sovereign Fleet C2 (`sentinel-nexus`)

`sentinel-nexus` acts as the fleet command-and-control server, providing three distinct interfaces:
* **gRPC Fleet Service (`:50051`):** High-throughput bidirectional gRPC channel receiving periodic node heartbeats, streaming threat alerts, and distributing Over-The-Air (OTA) candidate models.
* **REST Management API (`:9443`):** Endpoints serving topology metadata, node routing profiles, and the dynamic vault inventory.
* **Server-Sent Events Telemetry (`:9444`):** Real-time event stream broadcasting latency metrics and threat vectors to the web console.

---

## 2. Continual Learning Flywheel (`xinfer-forge`)

When edge nodes observe ambiguous or high-entropy traffic, uncertainty samples are buffered locally and forwarded to `xinfer-forge`:

1. **Self-Supervised Pretraining:** Trains a Tabular Masked Autoencoder (MAE) with InfoNCE contrastive loss over nominal traffic baselines without requiring manual labeling.
2. **Safety Regression Gate:** Validates newly trained candidate models against a historical corpus of "golden attacks" (`golden_attacks.yaml`). If the new model fails to detect any known exploit, it is automatically purged.
3. **Zero-Downtime Rollout:** Approved models are exported to INT8 ONNX, staged into SSFS `models/calibrated/`, and rolled out to edge nodes via Canary stages (`Shadow Mode` $\to$ `Canary 5%` $\to$ `Fleet-Wide`).

---

## 3. Scientific Verification Testbed (`sentinel-lab`)

`sentinel-lab` provides a 14-dimensional scientific validation environment. It executes physical ODE simulations (Runge-Kutta 4th-order) in lockstep with network traffic to verify that physical plants (such as chemical reactors or power grids) remain within Lyapunov stability margins under active cyber-attack.
