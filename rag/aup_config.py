# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: MIT

import logging
import subprocess
import time
import os
import glob
import shutil


def message_string(proc: subprocess.CompletedProcess) -> str:
    """Return a message string based on the return code."""
    if proc.returncode == 0:
        return "successfully"

    return f"failed with return code {proc.returncode}."


def run_capture(cmd, check: bool = False, **kwargs) -> subprocess.CompletedProcess:
    """Run subprocess while capturing stdout/stderr."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check, **kwargs)


def aup_setup(zstd_install: bool=True, vllm: bool=False) -> list[str]:
    """ Setup Environment by installing required packages"""

    logging.basicConfig(level=logging.INFO)
    workspace_dir = os.getcwd()
    aup_learning_cloud = False

    baseurl = os.environ.get("BASE_URL")
    amd_dev_cloud = True if baseurl=="notebooks.amd.com" else False

    for env in os.environ:
        if 'AUP_LEARNING' in env:
            aup_learning_cloud = True
            break

    logging.info("AMD Developer Cloud detected: %s.", amd_dev_cloud)
    logging.info("AUP Learning Cloud detected: %s.", aup_learning_cloud)
    if aup_learning_cloud:
        return

    logging.info("AMD Developer Cloud detected: %s.", amd_dev_cloud)

    if amd_dev_cloud and vllm:
        large_model = False
        model_name = "Qwen3.5-35B-A3B" if large_model else "Qwen3.5-9B"
        vllm_file = f"""#!/bin/bash

        VLLM_USE_TRITON_FLASH_ATTN=0 \\
        vllm serve Qwen/{model_name} \\
            --served-model-name {model_name} \\
            --api-key abc-123 \\
            --port 8000 \\
            --enable-auto-tool-choice \\
            --tool-call-parser hermes \\
            --trust-remote-code 2>&1 | tee vllm_serve.log
        """

        with open('vllm_serve.sh', 'w', encoding='utf-8') as f:
            f.write(vllm_file)
        logging.info("Wrote vLLM script: %s.", amd_dev_cloud)

    zstd_path = os.path.join(workspace_dir, "zstd")
    if zstd_install and not os.path.exists(zstd_path) and amd_dev_cloud:
        proc = run_capture(["git", "clone", "https://github.com/facebook/zstd"], check=True)
        os.chdir(zstd_path)
        proc = run_capture(["cmake", "-S", ".", "-B", "build-cmake-debug", "-G", "Ninja", "-DCMAKE_OSX_ARCHITECTURES='x86_64'"], check=True)
        os.chdir(os.path.join(zstd_path, "build-cmake-debug"))
        proc = run_capture(["ninja"], check=True)
        proc = run_capture(["sudo", "ninja", "install"], check=True)
        logging.info("Zstd installed %s.", message_string(proc))
        os.chdir(workspace_dir)

    proc = run_capture(["python3", "-m", "pip", "install", "--upgrade", "pip"], check=True)
    logging.info("Pip upgraded installed %s.", message_string(proc))


    proc = run_capture(["pip", "install", "--force-reinstall", "openai==2.21"],
                       check=True)

    proc = run_capture(["pip", "install", "langchain", "langchain-community==0.4.1",
                        "langchain-experimental==0.4.1", "langchain-text-splitters",
                        "pypdf", "fastembed", "ollama", "langchain-ollama",
                        "faiss-cpu", "langchain-chroma", "chromadb", "bs4",
                        "langchain-openai"],
                       check=True)

    logging.info("Pip packages installed %s.", message_string(proc))

    cmd = "which ollama"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0]
    if output == b"":
        cmd = "curl -fsSL https://ollama.com/install.sh | sh"
        proc = run_capture(cmd, check=True, shell=True)
        logging.info("Ollama installed %s.", message_string(proc))

    # The installer finds AMD GPUs only with lspci or lshw, which containers
    # often lack, and then installs the CPU-only build: every answer takes
    # minutes. When the GPU is visible (/dev/kfd), add the ROCm build it skipped.
    ollama_lib = os.path.join(os.path.dirname(os.path.dirname(
        shutil.which("ollama") or "/usr/local/bin/ollama")), "lib", "ollama")
    if os.path.exists("/dev/kfd") and not glob.glob(os.path.join(ollama_lib, "rocm*")):
        cmd = ("curl -fsSL https://ollama.com/download/ollama-linux-amd64-rocm.tar.zst"
               f" | zstd -d | tar -x -C {os.path.dirname(os.path.dirname(ollama_lib))}")
        proc = run_capture(cmd, check=True, shell=True)
        logging.info("Ollama ROCm support installed %s.", message_string(proc))

    os.environ["OLLAMA_FLASH_ATTENTION"] = "1"
    os.environ["OLLAMA_NO_CLOUD"] = "1"
    # LLM chunking sends ~8k tokens of the user guide in one prompt; a shorter
    # context makes Ollama refuse it with "400 Bad Request".
    os.environ["OLLAMA_CONTEXT_LENGTH"] = "32768"

    proc = run_capture(["ollama", "list"], check=False)
    if proc.returncode != 0:
        # Ollama ships its own ROCm. HIP_DEVICE_LIB_PATH from a ROCm image points
        # it at that image's device libraries, which it cannot link against, and
        # every model load segfaults. The code-object cache keeps such a failed
        # build, so it is off too: otherwise a crash once means a crash always.
        ollama_env = {k: v for k, v in os.environ.items() if k != "HIP_DEVICE_LIB_PATH"}
        ollama_env["AMD_COMGR_CACHE"] = "0"
        subprocess.Popen(
            ["ollama", "serve"],
            env=ollama_env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        logging.info("Ollama started in the background")
        time.sleep(3)
    else:
        logging.info("Ollama is already running")

    logging.info("Ollama is pulling models, this may take a while...")
    ollama_model_list = ["qwen3:8b", "qwen3.5:9b", "nomic-embed-text:v1.5"]
    for model in ollama_model_list:
        proc = run_capture(["ollama", "pull", model], check=True)
        if proc.returncode != 0:
            logging.error("Ollama model %s pull %s.",
                        model, message_string(proc))

    logging.info("Ollama models %s pulled successfully.",
                ", ".join(ollama_model_list))

    logging.getLogger().setLevel(logging.WARNING)
    return ollama_model_list


if __name__ == "__main__":
    aup_setup(zstd_install=True)
