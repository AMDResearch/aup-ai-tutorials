# Jupyter Book build

## Install Dependencies

For ease of use, the dependencies will be installed in a Python virtual environment.

```sh
set_book_venv.sh
```

The `jbook` directory is created with the `venv` on it.

## Build HTML

The script `build.sh` will activate the `venv` and build the Book HTML on the directory `../_build/html/`.

```sh
./build.sh
```

## Publish

The script `publish.sh` will push the html content to the `gh-pages` branch of the remote repository.

```sh
./publish.sh
```

## Build PDF

Make sure the system-wide dependencies are installed

```sh
sudo apt install -y libnss3-dev libnss3 libnspr4 libgbm-dev libasound
```

Build the PDF file with the `pdf_build.sh` script

```sh
pdf_build.sh
```

----------
Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.

SPDX-License-Identifier: MIT