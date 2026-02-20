# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: MIT

import logging
import subprocess
import time
import os


def message_string(proc: subprocess.CompletedProcess) -> str:
    """Return a message string based on the return code."""
    if proc.returncode == 0:
        return "successfully"

    return f"failed with return code {proc.returncode}."


def run_capture(cmd, check: bool = False, **kwargs) -> subprocess.CompletedProcess:
    """Run subprocess while capturing stdout/stderr."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check, **kwargs)


def aup_setup(pgk_update: bool=False, zstd_install: bool=True) -> None:
    """ Setup Environment by installing required packages"""
    if pgk_update:
        proc = run_capture(["sudo", "apt", "update"], check=True)
        proc = run_capture(["sudo", "apt", "install", "-y", "vim"],
                           check=True)
        logging.info("System packages updated %s.", message_string(proc))

    if zstd_install:
        proc = run_capture(["git", "clone", "https://github.com/facebook/zstd"], check=True)
        os.chdir("/workspace/zstd")
        proc = run_capture(["cmake", "-S", ".", "-B", "build-cmake-debug", "-G", "Ninja", "-DCMAKE_OSX_ARCHITECTURES='x86_64'"], check=True)
        os.chdir("/workspace/zstd/build-cmake-debug")
        proc = run_capture(["ninja"], check=True)
        proc = run_capture(["sudo", "ninja", "install"], check=True)
        logging.info("Zstd installed %s.", message_string(proc))
        os.chdir("/workspace/")

    proc = run_capture(["python3", "-m", "pip", "install", "--upgrade", "pip"], check=True)
    logging.info("Pip upgraded installed %s.", message_string(proc))

    proc = run_capture(["pip", "install", "langchain", "langchain-community",
                        "langchain-experimental", "langchain-text-splitters",
                        "pypdf", "fastembed", "ollama", "langchain-ollama",
                        "faiss-cpu", "langchain-chroma", "chromadb", "bs4",
                        "openai", "langchain-openai"],
                       check=True)

    logging.info("Pip packages installed %s.", message_string(proc))

    cmd = "which ollama"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0]
    if output == b"":
        cmd = "curl -fsSL https://ollama.com/install.sh | sh"
        proc = run_capture(cmd, check=True, shell=True)
        logging.info("Ollama installed %s.", message_string(proc))

    cmd = "ollama serve &"
    proc = run_capture(cmd, check=True, shell=True)
    logging.info("Ollama running in the background %s.", message_string(proc))
    time.sleep(3)

    ollama_model_list = ["llama3.1:8b", "nomic-embed-text:v1.5"]
    for model in ollama_model_list:
        proc = run_capture(["ollama", "pull", model], check=True)
        if proc.returncode != 0:
            logging.error("Ollama model %s pull %s.",
                          model, message_string(proc))

    logging.info("Ollama models %s pulled successfully.",
                 ", ".join(ollama_model_list))

    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aup_setup(pgk_update=False, zstd_install=True)
