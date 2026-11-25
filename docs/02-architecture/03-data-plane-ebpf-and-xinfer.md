# Data Plane: In-Kernel eBPF/XDP & Hardware AI (`libxinfer.so`)

The Data Plane operates at the physical network and memory boundary, processing frames within strict sub-microsecond deadlines before userspace context switches occur.

---

## 1. In-Kernel eBPF/XDP Filtering (`blackbox-essential`)

`blackbox-essential` compiles in-kernel eBPF bytecode using Clang/LLVM CO-RE (Compile Once – Run Everywhere) and attaches to the physical network interface using XDP:

```text
Incoming Wire Frame ──► NIC RX Queue ──► XDP Driver Hook (< 0.84 µs)
                                                 │
                        ┌────────────────────────┴────────────────────────┐
                        ▼                                                 ▼
             Hostile (In eBPF Map)                              Nominal / Unknown
                        │                                                 │
                        ▼                                                 ▼
                 XDP_DROP (< 0.84 µs)                           AF_XDP UMEM Zero-Copy
                (Hardware NIC Drop)                                       │
                                                                          ▼
                                                              Userspace IngressManager
```

* **XDP Driver Hook:** Evaluates the frame at the earliest possible software processing point. If an IP or TEID is registered inside `/sys/fs/bpf/blackbox_blocked_ips`, the driver returns `XDP_DROP` immediately.
* **Kernel W^X Protection (`live_sbom.o`):** Attaches a tracepoint to the kernel `sys_enter_mprotect` system call. Any unauthorized attempt to transition process memory pages to `PROT_READ | PROT_WRITE | PROT_EXEC` (fileless shellcode injection) triggers an immediate `SIGKILL` in `< 1.0 µs`.

---

## 2. Multi-Backend Zero-Copy AI (`xinfer-essential`)

When frames pass initial reflex gates, `ModelRouter` dispatches them to **`libxinfer.so`**, which provides a hardware-agnostic C++20 interface across 16 silicon backends:

* **Dynamic Tensor Discovery:** Introspects input and output tensor names automatically (`engine->input_names()`, `engine->output_names()`), executing models regardless of whether inputs are labeled `"input"`, `"data"`, or `"images"`.
* **Stable Softmax Entropy Scoring:** For public multi-class classification models (such as ImageNet 1000-class models), `ModelRouter` calculates normalized Shannon entropy:

$$H(p) = -\sum_{i=1}^{N} \frac{p_i \ln p_i}{\ln N}$$

This prevents false-positive logit clamping and guarantees that model outputs map deterministically into an anomaly score between `0.0` and `1.0`.
