# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: MIT

import logging
import subprocess
import time
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


def aup_setup(pgk_update: bool=False, zstd_install: bool=True,
              vllm: bool=False, graphviz_install: bool=True) -> None:
    """ Setup Environment by installing required packages"""

    amd_dev_cloud = False
    for env in os.environ:
        if 'AI_ACADEMY' in env:
            amd_dev_cloud = True
            break

    if pgk_update:
        proc = run_capture(["sudo", "apt", "update"], check=True)
        logging.info("System packages updated %s.", message_string(proc))
        proc = run_capture(["sudo", "apt", "install", "-y", "htop",
                            "python3-dev", "graphviz", "libgraphviz-dev",
                            "pkg-config"],
                           check=True)
        logging.info("System packages installed %s.", message_string(proc))

    logging.info("AMD Developer Cloud detected: %s.", amd_dev_cloud)
    if amd_dev_cloud and vllm:
        large_model = False
        model_name = "Qwen3-30B-A3B" if large_model else "Qwen3-8B"
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

    if zstd_install and not os.path.exists("/workspace/zstd") and amd_dev_cloud:
        proc = run_capture(["git", "clone", "https://github.com/facebook/zstd"], check=True)
        os.chdir("/workspace/zstd")
        proc = run_capture(["git", "checkout", "6e1e545"], check=True)
        proc = run_capture(["cmake", "-S", ".", "-B", "build-cmake-debug", "-G", "Ninja", "-DCMAKE_OSX_ARCHITECTURES='x86_64'"], check=True)
        os.chdir("/workspace/zstd/build-cmake-debug")
        proc = run_capture(["ninja"], check=True)
        proc = run_capture(["sudo", "ninja", "install"], check=True)
        logging.info("Zstd installed %s.", message_string(proc))
        os.chdir("/workspace/")

    filename = "graphviz-14.1.2.tar.gz"
    graphviz_path = filename.split(".tar.gz")[0]
    graphviz_version = graphviz_path.split("-")[-1]
    if graphviz_install and not os.path.exists(f"/workspace/{graphviz_path}") and amd_dev_cloud:
        response = requests.get(f"https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/{graphviz_version}/{filename}", stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)

        proc = run_capture(["tar", "-xvzf", filename], check=True)
        os.chdir(f"/workspace/{graphviz_path}")
        proc = run_capture(["./configure"], check=True)
        proc = run_capture(["make", "-j16"], check=True)
        proc = run_capture(["make", "install"], check=True)
        logging.info("graphviz installed %s.", message_string(proc))
        os.chdir("/workspace/")

    proc = run_capture(["python3", "-m", "pip", "install", "--upgrade", "pip"], check=True)
    logging.info("Pip upgraded installed %s.", message_string(proc))


    proc = run_capture(["pip", "install", "--force-reinstall", "openai==2.21"],
                       check=True)

    proc = run_capture(["pip", "install", "langgraph", "langchain", "langchain-ollama",
                        "pygraphviz", "langchain-openai", "langchain_mcp_adapters",
                        "pydantic_ai", "mcp_server_time", "openmeteo_requests",
                        "requests_cache", "retry_requests", "grandalf"],
                       check=True)

    logging.info("Pip packages installed %s.", message_string(proc))

    files = ["open_weather.py", "math_server.py"]
    for file in files:
        base_url = f"https://raw.githubusercontent.com/AMDResearch/aup-ai-tutorials/refs/heads/ai-agents/ai-agents/{file}"
        if not os.path.isfile(file):
            response = requests.get(base_url, stream=True)
            if response.status_code == 200:
                with open(file, 'wb') as file_handle:
                    file_handle.write(response.content)

    logging.info("Files %s downloaded successfully.", ", ".join(files))

    cmd = "which ollama"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0]
    if output == b"":
        cmd = "curl -fsSL https://ollama.com/install.sh | sh"
        proc = run_capture(cmd, check=True, shell=True)
        logging.info("Ollama installed %s.", message_string(proc))

    os.environ["OLLAMA_FLASH_ATTENTION"] = "1"
    os.environ["OLLAMA_NO_CLOUD"] = "1"
    os.environ["OLLAMA_CONTEXT_LENGTH"] = "16000"

    proc = run_capture(["ollama", "list"], check=False)
    if proc.returncode != 0:
        subprocess.Popen(
            ["ollama", "serve"],
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
    ollama_model_list = ["qwen3:8b", "qwen3.5:4b"]
    for model in ollama_model_list:
        proc = run_capture(["ollama", "pull", model], check=True)
        if proc.returncode != 0:
            logging.error("Ollama model %s pull %s.",
                        model, message_string(proc))

    logging.info("Ollama models %s pulled successfully.",
                ", ".join(ollama_model_list))


    return ollama_model_list


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aup_setup(pgk_update=False, zstd_install=True)
