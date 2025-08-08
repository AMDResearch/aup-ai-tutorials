#!/bin/bash

#Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
#SPDX-License-Identifier: MIT

sudo docker run \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add video \
    --group-add render \
    --shm-size 16G \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --network=host \
    --ipc=host \
    -it \
    -p 8888:8888 \
    -v $(pwd)/../:/ROCM_APP aupai bash