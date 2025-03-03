#!bin/bash

# Ref

# Python 3.11
# https://llm.mlc.ai/docs/install/mlc_llm.html#install-mlc-packages
# https://huggingface.co/mlc-ai/
# https://llm.mlc.ai/docs/install/tvm.html
# https://platform.openai.com/docs/api-reference/chat/create

#*------------------------------------------------------------------------------
source ../../../utils.sh

check_and_activate_conda_env
#*------------------------------------------------------------------------------

# Install

# conda deactivate && conda activate dev
conda create -n mlc -c conda-forge "cmake>=3.24" rust git python=3.11
conda activate mlc

conda install -y -c conda-forge libgcc-ng
conda install -y -c conda-forge git-lfs

git clone --recursive https://github.com/mlc-ai/mlc-llm.git others/repos/mlc-llm
cd others/repos/mlc-llm
mkdir -p build && cd build
python ../cmake/gen_cmake_config.py
cmake .. && cmake --build . --parallel $(nproc) && cd ..

cd python
pip install -e .
pip install apache-tvm

cd ..
ls -l ./build/ # `libmlc_llm.so`, `libtvm_runtime.so`
mlc_llm chat -h


# source ~/.bashrc
# python -m pip install --pre -U -f https://mlc.ai/wheels mlc-llm-cpu mlc-ai-cpu 
# python -m pip install --pre -U -f https://mlc.ai/wheels mlc-llm-cu122 mlc-ai-cu122


#*------------------------------------------------------------------------------

# Validate
python -c "import mlc_llm; print(mlc_llm)"
# Prints out: <module 'mlc_llm' from '/path-to-env/lib/python3.11/site-packages/mlc_llm/__init__.py'>

python -c "import tvm; print(tvm.__file__)"
# /some-path/lib/python3.11/site-packages/tvm/__init__.py

python -c "import tvm; print(tvm._ffi.base._LIB)"
# <CDLL '/some-path/lib/python3.11/site-packages/tvm/libtvm.dylib', handle 95ada510 at 0x1030e4e50>

python -c "import tvm; print('\n'.join(f'{k}: {v}' for k, v in tvm.support.libinfo().items()))"

python -c "import tvm; print(tvm.metal().exist)"
python -c "import tvm; print(tvm.cuda().exist)"
python -c "import tvm; print(tvm.vulkan().exist)"

#*------------------------------------------------------------------------------

# MODEL: HF://mlc-ai/Llama-3-8B-Instruct-q4f16_1-MLC

mlc_llm serve MODEL --host 127.0.0.1 --port 8000 # --overrides "tensor_parallel_shards=2"

mlc_llm chat MODEL

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "model": "MODEL",
        "messages": [
            {"role": "user", "content": "Hello! Our project is MLC LLM. What is the name of our project?"}
        ]
  }' \
  http://127.0.0.1:8000/v1/chat/completions

