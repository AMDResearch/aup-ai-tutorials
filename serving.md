# Model Serving

This section guides you through serving Large Language Models (LLMs) locally using three powerful and freely available tools:

- [Ollama](https://ollama.com) – A lightweight, user-friendly framework for running LLMs with minimal setup.
- [Llamafile](https://llamafile.ai/) – A self-contained, portable LLM server that simplifies deployment.
- [OpenLLM](https://github.com/bentoml/OpenLLM) – A flexible and scalable solution for serving LLMs in production environments.

Each of these tools has advantages depending on your use case:

- Ollama is ideal for quick experimentation and interactive chat, supporting various models from Hugging Face and other sources.
- Llamafile is designed for simplicity, bundling an entire LLM into a single executable for easy deployment across different platforms and operating systems.
- OpenLLM provides a more scalable, API-driven approach, making it well-suited for enterprise and cloud-based applications.

In the following sections, we’ll walk you through setting up and using Ollama, Llamafile, and OpenLLM to serve LLMs on AMD hardware.

## Serve LLMs with Ollama

Install Ollama inside the Docker container:

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

By default, models are not automatically served, so you will need to start the service and redirect the output:

```sh
ollama serve > /tmp/ollama.log 2>&1 &
```

Launch the 8 billion Llama3.1. You can explore more available models from the [Ollama library](https://ollama.com/library).

```sh
ollama run llama3.1:8b
```

Once the model is running, you can start interacting with it.

```{note}
Models are stored in `/ROCM_APP/models/ollama`, this ensures that the model will be only downloaded once, even after stopping the Docker container.
```

To stop **Ollama** run:

```sh
killall ollama
```

## Serve LLM(s) with Llamafile

Inside the Docker container, download LlaVa and give executable permissions.

```sh
wget https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/resolve/main/llava-v1.5-7b-q4.llamafile?download=true -O llava-v1.5-7b-q4.llamafile
chmod +x llava-v1.5-7b-q4.llamafile
```

Launch the Llamafile server.

```sh
./llava-v1.5-7b-q4.llamafile --port 8888 --nobrowser -ngl 999 --host '0.0.0.0'
```

In the host machine (outside Docker), open a web browser and navigate to `localhost:8888`. This will load the Llamafile web app, where you can experiment with *Chat* and *Completion* modes.

```{note}
We suggest you click on `More options` and increase the `Show Probabilities`, this will show the output tokens color coded.
If you click in the token, it shows the most likely tokens and the likelihood of being placed after the previous token.
By increasing the `Temperature`, you can get more 'creative' answers.
```

## Serve with OpenLLM

[Step-by-Step Guide to Use OpenLLM on AMD GPUs](https://rocm.blogs.amd.com/artificial-intelligence/openllm/README.html)

## Serve with SGLang

[Step-by-Step Guide to Use SGLang on AMD GPUs](https://rocm.blogs.amd.com/artificial-intelligence/sglang/README.html)

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT