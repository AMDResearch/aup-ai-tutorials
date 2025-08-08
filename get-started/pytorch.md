# Using PyTorch Hub Models

This section shows you how to run pre-trained PyTorch models from the Torch Hub.

PyTorch models will be stored in:

``````{tab-set}
`````{tab-item} Linux
```console
$USER/.cache/huggingface
```
`````

`````{tab-item} Windows
```console
%USERPROFILE%\.cache\huggingface\hub
```
`````
``````

```{note}
In Docker, the models will be stored in `/ROCM_APP/models/torch`, this ensures that the model will be only downloaded once, even after stopping the Docker container.
```

## Examples

Make sure the [environment is setup](../env/env.md).

This guide provides a number of examples you can run out of the box. Navigate to `get-started/pytorch/` and lunch `jupyter lab`. Some of them can only run if you have an AMD GPU in your system.

```{tableofcontents}
```

## More Pre-trained Models

If you would like to run a different model, PyTorch Hub hosts several models.
Explore what PyTorch Hub has to offer https://pytorch.org/hub/.

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT