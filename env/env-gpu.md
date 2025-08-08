(docker-gpu)=
# Setting PyTorch Environment for GPU

This page describes the procedure to setup a ROCm-enabled PyTorch environment in your machine with a supported AMD GPU.

## Pre-requisites

```{card}
GPUs: {bdg-primary}`AMD Instinct™ Accelerators`, {bdg-primary}`AMD Radeon™ RX Graphics Cards` or {bdg-primary}`AMD Radeon™ PRO Graphics Cards`

See [Linux-supported GPUs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus)
```

- Linux OS: list of supported operating systems [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems)
- Elevated (root) privileges
- [Docker](https://www.docker.com/)

(gpu-linux)=
## Linux

To simplify the installation process, you will use a pre-built Docker container.
We provide a docker file that builds on top of the official [PyTorch docker container](https://hub.docker.com/r/rocm/pytorch/tags).

The first step is to install Docker in your Linux machine, follow the steps [here](https://docs.docker.com/engine/install/). For instance, [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

Once installed, make sure to check and apply [Linux post-installation steps for Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/).

Clone this repository

```sh
git clone https://github.com/AMDResearch/aup-ai-tutorials.git
```

Navigate to the `docker` folder and build the docker container.

```sh
cd aup-ai-tutorials/docker
./build.sh
```

```{note}
This process can take at least 10 minutes, depending on your Internet connection.
```

Once build, to launch it the docker container run

```sh
./run.sh
```

Once inside the Docker container, check if the GPU is being detected.

```sh
check_gpu
```

```{note}
`check_gpu` is an alias defined in `~/.bashrc` that executes `python -c "import torch; print(f'GPU detected: {torch.cuda.is_available()}')"`
```

Now you can launch Jupyter Lab, navigate to the folder where the repository is and you run (from inside the Docker):

```sh
cd /ROCM_APP/aup-ai-tutorials
launch_jupyter
```

```{note}
`launch_jupyter` is an alias defined in `~/.bashrc` that executes `jupyter lab --ip='0.0.0.0' --allow-root --NotebookApp.token='' --NotebookApp.password=''`
```

On the host machine launch a web browser and open `localhost:8888/lab`

(gpu-windows)=
## Windows

AI Frameworks are not currently supported. See list of [Windows ROCm Component Support](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/component-support.html#rocm-component-support).

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT