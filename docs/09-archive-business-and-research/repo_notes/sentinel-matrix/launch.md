!!! info "Archival Engineering Record — Historical Context"
    This document preserves a historical design artifact from earlier development iterations. For active production specifications, verified APIs, and deployment runbooks, consult **Section 02 (System Architecture)** and **Section 03 (Developer & SDK)**.

---

cd ${WORKSPACE_ROOT}/sentinel-matrix

# 1. Reset AppArmor shims, restart docker, and clear stuck containers with 1 command
make fix-docker

# 2. Launch the entire mesh cleanly
make up

# 3. Check live running status
make status