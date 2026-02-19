# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: MIT

import logging
import subprocess
import time


def message_string(proc: subprocess.CompletedProcess) -> str:
    """Return a message string based on the return code."""
    if proc.returncode == 0:
        return "successfully"

    return f"failed with return code {proc.returncode}."


def aup_setup(pgk_update: bool=False) -> None:
    """ Setup Environment by installing required packages"""
    if pgk_update:
        proc = subprocess.run(["sudo", "apt", "update"], check=True)
        proc = subprocess.run(["sudo", "apt", "install", "-y", "vim"],
                              check=True)
        logging.info("System packages updated %s.", message_string(proc))

    proc = subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "pip"], check=True)
    logging.info("Pip upgraded installed %s.", message_string(proc))

    proc = subprocess.run(["pip", "install", "langchain", "langchain-community",
                          "langchain-experimental", "langchain-text-splitters",
                          "pypdf", "fastembed", "ollama", "langchain-ollama",
                          "faiss-cpu", "langchain-chroma", "chromadb", "bs4",
                          "openai", "langchain-openai"],
                          check=True)

    logging.info("Pip packages installed %s.", message_string(proc))

    cmd = "which ollama"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0]
    if output == b'':
        cmd = "curl -fsSL https://ollama.com/install.sh | sh"
        proc = subprocess.run(cmd, check=True, shell=True)
        logging.info("Ollama installed %s.", message_string(proc))

    cmd = "ollama serve &"
    proc = subprocess.run(cmd, check=True, shell=True)
    logging.info("Ollama running in the background %s.", message_string(proc))
    time.sleep(3)

    ollama_model_list = ["llama3.1:8b", "nomic-embed-text:v1.5"]
    for model in ollama_model_list:
        proc = subprocess.run(["ollama", "pull", model], check=True)
        if proc.returncode != 0:
            logging.error("Ollama model %s pull %s.",
                          model, message_string(proc))

    logging.info("Ollama models %s pulled successfully.",
                 ", ".join(ollama_model_list))

    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aup_setup(pgk_update=True)
