(direct-ml-windows)=
# Setting PyTorch Environment for GPU

This page describes the procedure to setup a DirectML-enabled PyTorch environment on Windows for a supported AMD GPU.

## Pre-requisites

```{card}
GPUs: {bdg-primary}`AMD Radeon™ RX Graphics Cards` or {bdg-primary}`AMD Radeon™ PRO Graphics Cards`

See [Enable PyTorch with DirectML on Windows](https://learn.microsoft.com/en-us/windows/ai/directml/pytorch-windows)
```

## Install Python Virtual Environment

1. Follow the steps to install [Python on Windows](env-cpu.md#cpu-windows)
1. Then continue by [creating a Python virtual environment](env-cpu.md#cpu-venv)

Once these steps are completed, install [Pytorch with DirectML](#pytorch-directml).

(pytorch-directml)=
## Install Pytorch with DirectML

Inside of the `venv` run:

```sh
python -m pip install torch-directml
```

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT