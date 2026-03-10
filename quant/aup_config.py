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


def _patch_pytorch_utils() -> None:
    """Add the removed is_torch_less_than_1_11 flag to transformers.pytorch_utils."""
    utils_path = "/usr/local/lib/python3.12/dist-packages/transformers/pytorch_utils.py"
    if not os.path.isfile(utils_path):
        logging.warning("pytorch_utils.py not found at %s, skipping patch.", utils_path)
        return

    with open(utils_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    if "is_torch_less_than_1_11" in content:
        logging.info("pytorch_utils.py already contains is_torch_less_than_1_11.")
        return

    patch = "\n# Patched by aup_config\nis_torch_less_than_1_11 = False\n"
    with open(utils_path, "a", encoding="utf-8") as fh:
        fh.write(patch)
    logging.info("Patched %s: added is_torch_less_than_1_11.", utils_path)


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
                        "onnxruntime", "onnx>=1.16.2", "onnxscript",
                        "pygit2", "lm_eval==0.4.9.2", "optimum[amd]",
                        "onnxruntime_genai"], check=True)

    proc = run_capture(["pip", "install",
                        "git+https://github.com/amd/Quark/@release/0.11"],
                       check=True)

    if amd_dev_cloud:
        _patch_pytorch_utils()

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
