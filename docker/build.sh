#!/bin/bash

#Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
#SPDX-License-Identifier: MIT

USER_NAME="$USER"

if [ $# -eq 1 ]; then
    USER_NAME="$1"
fi

USER_ID=`id -u $USER_NAME`
GROUP_ID=`id -g $USER_NAME`
GROUP_NAME=`id -g -n $USER_NAME`
RENDER_GID=`getent group render | cut -d: -f3`

docker build \
    --build-arg USER_ID=${USER_ID} \
    --build-arg GROUP_ID=${GROUP_ID} \
    --build-arg GROUP_NAME=${GROUP_NAME} \
    --build-arg RENDER_GID=${RENDER_GID} \
    --tag aupai .