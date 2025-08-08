# Generative AI on AMD platforms

In this section, we refer to popular generative AI applications that can be run on your local machine.

## Text Generation Webui

```sh
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui/

./start_linux.sh --listen-port 8888
```

In your browser, open `localhost:8888`. Head over to the Model tab, in the Download window on the right, get your model of choice from Hugging Face. For instance, let us use `lmsys/vicuna-7b-v1.5`, click download. Once the download is done, you load the model and go back to the `Chat` tab.

If you would like to get more information on this tool, please visit the repository https://github.com/oobabooga/text-generation-webui.

## ComfyUI

```sh
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt -O models/checkpoints/v1-5-pruned-emaonly.ckpt # download checkpoint
python main.py
```

Open the web browser in your host machine and start playing with it. You can find a getting started here https://docs.comfy.org/get_started/gettingstarted

## InvokeAI

```sh
cd /tmp
wget https://github.com/invoke-ai/InvokeAI/releases/download/v4.2.7post1/InvokeAI-installer-v4.2.7post1.zip -O invokeai.zip
unzip invokeai.zip
./InvokeAI-Installer/install.sh -r /ROCM_APP/invokeai
/ROCM_APP/invokeai/invoke.sh
```

<!--
## AUTOMATIC1111/stable-diffusion-webui

Lots of problems

https://github.com/lshqqytiger/stable-diffusion-webui-amdgpu.git

```sh
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui

# activate venv

REQS_FILE='requirements.txt' python launch.py --precision full --no-half
```

https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs#running-inside-docker

https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs#setup-venv-environment

https://stackoverflow.com/questions/74289972/cannot-import-name-rank-zero-only-from-pytorch-lightning-utilities-distribute
-->

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT