#!/bin/bash

# Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

source jbook/bin/activate || { echo "Error: No venv, create venv"; exit 1; }
cd ../ && jupyter-book build . --builder pdfhtml --all
deactivate