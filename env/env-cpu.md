(pytorch-cpu)=
# Setting PyTorch Environment for CPU

This page describes the process to setup a PyTorch environment in your machine.

Follow the steps to install Python and virtual environment tools for your OS:
[Windows](#cpu-windows) or [Linux](#cpu-linux), then follow the steps to create a `venv`
where you will run the getting started examples.

Alternative, you can setup [VS Code](#vs-code) in any of the supported OSes.

## Pre-requisites

```{card}
{bdg-primary}`AMD EPYC™ Processors`, {bdg-primary}`AMD Ryzen™ Processors` or {bdg-primary}`AMD Ryzen™ AI Processors`
```

```{raw} html
<!DOCTYPE html>
<html>
<head>
    <script>
        function getPlatform() {
            // Retrieve platform information
            var platform = navigator.platform;
            // Display platform information
            document.getElementById('platform').textContent = platform;
        }

        // Call the function when the window loads
        window.onload = getPlatform;
    </script>
</head>
<body>
    <p>Your platform is: <span id="platform">Loading...</span></p>
</body>
</html>
```

(cpu-windows)=
## Windows

Click [here to download Python 3.12.8](https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe) or
find the latest release of Python [here python.org/downloads/windows/](https://www.python.org/downloads/windows/) select *Windows installer (64-bit)*

```{note}
Python 3.13 has not been verified.
```

Follow the steps in the [Python documentation](https://docs.python.org/3.12/using/windows.html#installation-steps) after executing the installer.

Once you complete the installation, open a [Windows PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/starting-windows-powershell?view=powershell-7.4#from-the-start-menu).

Confirm that Python is installed by checking the version

```sh
python -c "import sys; print(sys.version)"
```

Continue by [creating the venv](#cpu-venv).

(cpu-linux)=
## Linux

We will use a [Python virtual environment](https://docs.python.org/3/library/venv.html) (venv) to install the dependencies.

Open a new terminal and install `python3-venv`.

```sh
sudo apt install python3-pip python3-venv libgl1
```

Confirm that Python is installed by checking the version

```sh
python3 -c "import sys; print(sys.version)"
```

Continue by [creating the venv](#cpu-venv).

(cpu-venv)=
## Create venv

Navigate to a directory where you would like to create the `venv`, then create the `venv`.

``````{tab-set}
`````{tab-item} Linux
```sh
cd /path/to/directory/
mkdir aupai
python3 -m venv aupai
```
`````

`````{tab-item} Windows
```sh
cd /path/to/directory/
mkdir aupai
python -m venv aupai
```
`````
``````

Activate the `venv`.

``````{tab-set}
`````{tab-item} Linux
```sh
source aupai/bin/activate
```
`````

`````{tab-item} Windows PowerShell
```sh
./aupai/Scripts/Activate.ps1
```
`````

`````{tab-item} Windows CMD
```sh
./aupai/Scripts/activate.bat
```
`````
``````

Confirm that you are inside the `venv`.

```sh
python -c "import sys; print(f'Running on venv: {sys.prefix != sys.base_prefix}')"
```

```{note}
You can deactivate the `venv` with `deactivate`.
```

Continue by [installing package dependencies](#cpu-install-dependencies).

(vs-code)=
## Visual Studio Code

If you prefer working from a code editing tool, you can setup VS Studio code.

1. [Install VS Code](https://code.visualstudio.com/download).

1. [Get started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)

1. [Create a virtual environment](https://code.visualstudio.com/docs/python/python-tutorial#_create-a-virtual-environment)

(cpu-install-dependencies)=
## Install Package Dependencies

Inside the `venv` execute the following to install the necessary dependencies.

```sh
python -m pip install "torch>2.3" "numpy<2" torchvision fvcore
python -m pip install av validators matplotlib jupyterlab jupyter transformers SentencePiece accelerate ultralytics==8.0.196 wheel
python -m pip install tiktoken einops pytest Pillow Requests jupyterlab_myst torchinfo "onnx>=1.16.2" netron tqdm shap kaggle roboflow==1.1.47 pickleshare
python -m pip install jupyter-book sphinxcontrib-mermaid sphinx_design
```

```{note}
If you are using VS Code, you can open a new terminal by `` Ctrl+Shift+` `` or `Terminal > New Terminal`. For more information,
checkout [Install and use packages](https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages).
```

This process can take a few minutes to download and install.

You are now all set to get started with pre-trained models in AMD CPUs.

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT