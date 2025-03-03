#!/bin/bash

# Ref
# https://github.com/dscripka/openWakeWord

#*------------------------------------------------------------------------------
source "$(dirname "$0")/../../../scripts/utils.sh"

ROOT_DIR=$(find_root_path)

check_and_activate_conda_env
#*------------------------------------------------------------------------------

# git clone https://github.com/dscripka/openWakeWord others/repos/openWakeWord

# pip install openwakeword
# https://github.com/dscripka/openWakeWord/releases/tag/v0.1.1
# pip install https://github.com/dscripka/openWakeWord/releases/download/v0.1.1/speexdsp_ns-0.1.2-cp310-cp310-linux_aarch64.whl