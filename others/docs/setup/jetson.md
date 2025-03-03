# Setup environment for Linux server

## Initial

## Conda

```bash
conda deacivate
conda activate dev
```

## Python

```bash
pip install --upgrade -r apps/requirements/dev.requirements.txt

# (python 3.10/3.11 only)
conda install xformers -c xformers
```

### PyTorch for Jetson

Ref:

- https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html#overview__section_orin
- https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-base

```bash
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH

sudo apt-cache show nvidia-jetpack
```

```bash
wget https://raw.githubusercontent.com/pytorch/pytorch/5c6af2b583709f6176898c017424dc9981023c28/.ci/docker/common/install_cusparselt.sh
export CUDA_VERSION=12.2  # This matches your CUDA version
sudo bash ./install_cusparselt.sh


export TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v60/pytorch/torch-2.5.0a0+872d972e41-cp38-cp38-linux_aarch64.whl

```

## Start services

```
make start
```

## Poppler

```bash
sudo apt-get install poppler-utils

# Verify if Poppler is in your system PATH
# This command checks for the pdftoppm utility, which is part of Poppler
which pdftoppm

# Restart your shell to reload the PATH
# This is useful if you've just installed Poppler or modified your PATH
exec $SHELL

# # Activate an existing virtual environment
# # Replace '/path/to/your/venv' with the actual path to your virtual environment
# source /path/to/your/venv/bin/activate

# # Create a new virtual environment named 'myenv'
# python3 -m venv myenv

# # Activate the newly created virtual environment
# source myenv/bin/activate

# # Install required packages in the activated virtual environment
# # Replace 'your-required-packages' with actual package names, e.g., PyPDF2, pdf2image
# pip install your-required-packages

# # Run your Python script
# # Replace 'your_script.py' with the name of your actual Python file
# python your_script.py
```

## Services

- Run services using the Makefile as described in the [README](../../../README.md).

```bash
jetson-containers run -d --name ollama dustynv/ollama:r35.4.1
```

###
