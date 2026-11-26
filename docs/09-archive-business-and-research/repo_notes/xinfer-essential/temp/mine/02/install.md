!!! info "Archival Engineering Record — Historical Context"
    This document preserves a historical design artifact from earlier development iterations. For active production specifications, verified APIs, and deployment runbooks, consult **Section 02 (System Architecture)** and **Section 03 (Developer & SDK)**.

---

### How Developers Use This:

#### Option A: One-Command Installation via `install.sh`
```bash
./install.sh --all
```

#### Option B: Build via CMake (Automatic Header Fetching)
```bash
mkdir build && cd build
cmake .. -DXINFER_ENABLE_RKNN=ON
make -j$(nproc)
```
If RKNN headers are missing on their machine, CMake will clone them automatically during compilation!