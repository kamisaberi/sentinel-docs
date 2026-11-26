!!! info "Archival Engineering Record — Historical Context"
    This document preserves a historical design artifact from earlier development iterations. For active production specifications, verified APIs, and deployment runbooks, consult **Section 02 (System Architecture)** and **Section 03 (Developer & SDK)**.

---

# 1. Create build directory
mkdir build && cd build

# 2. Configure CMake
cmake ..

# 3. Build libblackbox.so
make -j$(nproc)

# 4. Install libblackbox.so to /usr/local/lib
sudo make install
sudo ldconfig

# 5. Check exported shared library in system
ls -la /usr/local/lib/libblackbox.so*