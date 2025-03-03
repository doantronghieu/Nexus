from enum import Enum

class QConfig(Enum):
    # X86: Quantization backend for x86 architecture
    # Can run on Intel-based Macs and some other x86 systems
    X86 = "x86"

    # FBGEMM: Facebook's GEMM library for server-side inference
    # Primarily designed for x86 processors, not typically used on macOS
    # Especially not suitable for Apple Silicon (ARM) Macs
    FBGEMM = "fbgemm"

    # QNNPACK: Quantized Neural Network PACKage
    # Optimized for mobile and ARM architectures
    # Well-suited for Apple Silicon (M1/M2) Macs and iOS devices
    QNNPACK = "qnnpack"

    # ONEDNN: Intel's Deep Neural Network library
    # Supports both x86 and ARM architectures
    # Can run on both Intel and Apple Silicon Macs
    ONEDNN = "onednn"