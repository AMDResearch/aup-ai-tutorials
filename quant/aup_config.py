# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: MIT

import logging
import subprocess
import os
import requests


def message_string(proc: subprocess.CompletedProcess) -> str:
    """Return a message string based on the return code."""
    if proc.returncode == 0:
        return "successfully"

    return f"failed with return code {proc.returncode}."


def run_capture(cmd, check: bool = False, **kwargs) -> subprocess.CompletedProcess:
    """Run subprocess while capturing stdout/stderr."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check, **kwargs)


def aup_setup() -> None:
    """ Setup Environment by installing required packages"""

    workspace_dir = os.getcwd()
    amd_dev_cloud = False
    for env in os.environ:
        if 'AI_ACADEMY' in env:
            amd_dev_cloud = True
            break
    logging.info("AMD Developer Cloud detected: %s.", amd_dev_cloud)

    proc = run_capture(["python3", "-m", "pip", "install", "--upgrade", "pip"],
                       check=True)
    logging.info("Pip upgraded installed %s.", message_string(proc))

    proc = run_capture(["pip", "install", "matplotlib", "ml_dtypes", "tabulate",
                        "amd-quark==0.11", "onnxruntime", "onnx>=1.16.2",
                        "onnxscript", "pygit2"],
                       check=True)

    logging.info("Pip packages installed %s.", message_string(proc))

    file = 'resnet_trained_for_cifar10.onnx'
    base_url = "https://github.com/AMDResearch/aup-ai-tutorials/raw/refs/heads/main/quant/onnx/resnet_trained_for_cifar10.onnx"
    onnx_dir = os.path.join(workspace_dir, "onnx")
    file_path = os.path.join(onnx_dir, file)
    if not os.path.isfile(file_path):
        os.makedirs(onnx_dir, exist_ok=True)
        response = requests.get(base_url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file_handle:
                file_handle.write(response.content)
        logging.info("Pretrained Resnet model downloaded %s.", message_string(file))

    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aup_setup()
