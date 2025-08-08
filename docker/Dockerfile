#Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
#SPDX-License-Identifier: MIT

FROM rocm/pytorch:rocm6.4.2_ubuntu24.04_py3.12_pytorch_release_2.6.0

RUN apt-get -y update
RUN apt-get install -y python3-opencv psmisc less vim git
RUN apt-get install -y htop iputils-ping google-perftools python3-venv adduser perl
RUN apt-get install -y build-essential cmake

ARG USER_ID
ARG GROUP_ID
ARG GROUP_NAME
ARG RENDER_GID

LABEL maintainer="AMD University Program"

# Link to Python in conda env where ROCm enabled PyTorch is installed
RUN unlink /usr/bin/python3
RUN ln -s /opt/conda/envs/py_3.12/bin/python3 /usr/bin/python3

# Create render group
RUN if [ -z "${RENDER_GID}" ]; then \
      groupadd -g ${RENDER_GID} render || echo "Ignoring error, if group already exists"; \
    else \
      groupadd render || echo "Ignoring error, if group already exists"; \
    fi

# Add root to render
RUN usermod -a -G render root

# Set non interactive terminal mode
RUN chmod a+rwx /root
ARG DEBIAN_FRONTEND=noninteractive

# set to true to install bits and bytes
ENV INSTALL_BNB=true

# set to true to install flash attention 2, this can take a lot of resources
ENV INSTALL_FA2=false

# set to true to AITER
ENV INSTALL_AITER=true

#-DBNB_ROCM_ARCH="gfx940,gfx941,gfx942,gfx90a,gfx908,gfx1100,gfx1103,gfx1150"

RUN if [ "$INSTALL_BNB" = "true" ]; then \
    git clone --recurse https://github.com/ROCm/bitsandbytes.git && \
    cd  bitsandbytes && git checkout rocm_enabled_multi_backend && \
    pip install -r requirements-dev.txt && \
    cmake -DCOMPUTE_BACKEND=hip -S . && \
    make && pip install .; \
    fi

RUN if [ "$INSTALL_FA2" = "true" ]; then \
    git clone https://github.com/ROCm/flash-attention.git flash-attention-v2 && \
    cd flash-attention-v2 && git submodule update --init --recursive && \
    GPU_ARCHS="gfx90a;gfx942" PYTORCH_ROCM_ARCH="gfx90a;gfx942" python setup.py install && \
    cd .. && \
    rm -rf flash-attention; \
    fi

RUN if [ "$INSTALL_AITER" = "true" ]; then \
    git clone --recursive https://github.com/ROCm/aiter.git && \
    cd aiter && python3 setup.py develop; \
    fi

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Kaggle empty Token
RUN mkdir -p ~/.kaggle/
RUN chmod 600 -R ~/.kaggle/

ENV OLLAMA_MODELS=/ROCM_APP/models/ollama
ENV HF_HOME=/ROCM_APP/models/hf
ENV TORCH_HOME=/ROCM_APP/models/torch
ENV HF_HUB_DISABLE_IMPLICIT_TOKEN=1
ENV ROBOFLOW_API_KEY=""
ENV SHELL=/bin/bash

EXPOSE 8080 8888

RUN echo "sudo chown root:${GROUP_NAME} -R /dev/dri/ /dev/kfd" >> ~/.bashrc
RUN echo "alias launch_jupyter=\"jupyter lab --ip='0.0.0.0' --allow-root --NotebookApp.token='' --NotebookApp.password=''\"" >> ~/.bashrc
RUN echo 'alias check_gpu="python -c \"import torch; print(f'\''GPU detected: {torch.cuda.is_available()}'\'')\""' >> ~/.bashrc

WORKDIR /ROCM_APP