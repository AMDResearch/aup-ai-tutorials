# Configuring the Environment

Independent of the path you are taking, if you are planning to do hands-on with
an AMD platform, you will need to setup the environment to be able to run the
examples provided in this guide.


(supported-hw)=
## Supported AMD Platforms

```{card}
- CPUs: {bdg-primary}`AMD EPYC™ Processors` {bdg-primary}`AMD Ryzen™ Processors` {bdg-primary}`AMD Ryzen™ AI Processors`
- GPUs: {bdg-primary}`AMD Instinct™ Accelerators` {bdg-primary}`AMD Radeon™ RX Graphics Cards` {bdg-primary}`AMD Radeon™ PRO Graphics Cards`
```

```{note}
AMD GPUs for AI workloads are only supported on a Linux based system. [Linux-supported GPUs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus)
```

## Setup Environment

To setup the environment we strongly suggest you use one of the officially supported Linux OS.
Check the list of supported operating systems [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems). AI Frameworks are not currently supported on Windows.

- [Setup a CPU only environment](env-cpu.md). No ROCm needed, both Linux and Windows.
- [Setup a GPU environment on Linux](env-gpu.md). Enable GPU acceleration both for training and inference on a Linux.
- [Setup a GPU environment on Windows](env-gpu-windows.md). Enable GPU acceleration both for training and inference on Windows using [DirectML](https://learn.microsoft.com/en-us/windows/ai/directml/dml).

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT