!!! info "Archival Engineering Record — Historical Context"
    This document preserves a historical design artifact from earlier development iterations. For active production specifications, verified APIs, and deployment runbooks, consult **Section 02 (System Architecture)** and **Section 03 (Developer & SDK)**.

---

# 1. Stop any stopped or hanging matrix simulation containers holding the network
docker stop $(docker ps -aq --filter "name=matrix-") 2>/dev/null || true
docker rm $(docker ps -aq --filter "name=matrix-") 2>/dev/null || true

# 2. Prune unused Docker networks to release the 10.240.0.0/24 pool
docker network prune -f

# 3. Verify that 10.240.0.0 is completely freed
docker network inspect $(docker network ls -q) --format '{{.Name}}: {{range .IPAM.Config}}{{.Subnet}}{{end}}' | grep "10.240.0" || echo "[+] Address pool 10.240.0.0/24 is 100% FREE"

# 4. Re-launch your generic sentinel-matrix scenario
cd ${WORKSPACE_ROOT}/sentinel-matrix
# Run your standard generic scenario command (e.g. docker compose up -d or make up)