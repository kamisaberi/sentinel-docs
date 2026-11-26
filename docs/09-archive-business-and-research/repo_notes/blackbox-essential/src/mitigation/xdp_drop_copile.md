!!! info "Archival Engineering Record — Historical Context"
    This document preserves a historical design artifact from earlier development iterations. For active production specifications, verified APIs, and deployment runbooks, consult **Section 02 (System Architecture)** and **Section 03 (Developer & SDK)**.

---

```
clang -O2 -g -target bpf -D__TARGET_ARCH_x86 \
  -I${WORKSPACE_ROOT}/blackbox-essential/src/mitigation \
  -I/usr/include/$(uname -m)-linux-gnu \
  -c ${WORKSPACE_ROOT}/blackbox-essential/src/mitigation/xdp_drop.c \
  -o ${WORKSPACE_ROOT}/blackbox-essential/src/mitigation/xdp_drop.o

  ```