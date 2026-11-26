!!! info "Archival Engineering Record — Historical Context"
    This document preserves a historical design artifact from earlier development iterations. For active production specifications, verified APIs, and deployment runbooks, consult **Section 02 (System Architecture)** and **Section 03 (Developer & SDK)**.

---

### Binary Preparation & Permissions

Make all scripts and entrypoints executable:

```bash
chmod +x ${WORKSPACE_ROOT}/sentinel-matrix/docker/entrypoints/*.sh
chmod +x ${WORKSPACE_ROOT}/sentinel-matrix/src/traffic/*.py
chmod +x ${WORKSPACE_ROOT}/sentinel-matrix/src/loop/*.py
chmod +x ${WORKSPACE_ROOT}/sentinel-matrix/src/orchestrator/*.py
chmod +x ${WORKSPACE_ROOT}/sentinel-matrix/src/monitor/*.py
chmod +x ${WORKSPACE_ROOT}/sentinel-matrix/tools/*.py
```

Copy the compiled binaries into `shared/bin/` so the Docker build stages can package them:

```bash
mkdir -p ${WORKSPACE_ROOT}/sentinel-matrix/shared/bin
cp ${WORKSPACE_ROOT}/sentinel-nexus/build/sentinel-nexus ${WORKSPACE_ROOT}/sentinel-matrix/shared/bin/
cp ${WORKSPACE_ROOT}/sentinel-nexus/build/nexus-ctl ${WORKSPACE_ROOT}/sentinel-matrix/shared/bin/
cp ${WORKSPACE_ROOT}/blackbox-sentinel/build/sentinel ${WORKSPACE_ROOT}/sentinel-matrix/shared/bin/

# Copy web dashboard assets into sentinel-matrix
cp -r ${WORKSPACE_ROOT}/sentinel-nexus/web ${WORKSPACE_ROOT}/sentinel-matrix/

# Copy proto definitions for python stub compilation in Docker
mkdir -p ${WORKSPACE_ROOT}/sentinel-matrix/shared/proto
cp ${WORKSPACE_ROOT}/sentinel-nexus/proto/*.proto ${WORKSPACE_ROOT}/sentinel-matrix/shared/proto/
```

---

### Verification: Launching the Simulation Inside VMware

```bash
cd ${WORKSPACE_ROOT}/sentinel-matrix

# 1. Build all 5 container images
make build

# 2. Start the autonomous simulation mesh
make up
```

Once running:
* **Web UI:** Open your browser to `http://localhost:9443` (or the VMware guest IP).
* **Live Terminal TUI:** Run `make tui` to launch the live dashboard inside your terminal.
* **Test Attacks & Chaos:**
  * Run `make attack-modbus` to trigger an in-kernel SCADA drop and collective defense fan-out.
  * Run `make chaos-latency` to verify the automated SLA rollback.
  * Run `make chaos-sever` to verify the instant 0ms disconnect.