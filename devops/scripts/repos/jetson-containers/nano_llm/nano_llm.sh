#!/bin/bash

# https://dusty-nv.github.io/NanoLLM/index.html
# https://github.com/dusty-nv/jetson-containers/tree/master/packages/llm/nano_llm
# https://www.jetson-ai-lab.com/tutorial_slm.html
# https://huggingface.co/models?pipeline_tag=text-generation&sort=trending

jetson-containers run dustynv/nano_llm:r36.2.0

docker run --runtime nvidia -it --rm --network host --shm-size=8g --volume /tmp/argus_socket:/tmp/argus_socket --volume /etc/enctune.conf:/etc/enctune.conf --volume /etc/nv_tegra_release:/etc/nv_tegra_release --volume /tmp/nv_jetson_model:/tmp/nv_jetson_model --volume /var/run/dbus:/var/run/dbus --volume /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket --volume /var/run/docker.sock:/var/run/docker.sock --volume /home/aic/jetson-containers/data:/data --device /dev/snd --device /dev/bus/usb --device /dev/i2c-0 --device /dev/i2c-1 --device /dev/i2c-2 --device /dev/i2c-3 --device /dev/i2c-4 --device /dev/i2c-5 --device /dev/i2c-6 --device /dev/i2c-7 --device /dev/i2c-8 --device /dev/i2c-9 -v /run/jtop.sock:/run/jtop.sock --name my_jetson_container dustynv/nano_llm:r36.2.0
Unable to find image 'dustynv/nano_llm:r36.2.0' locally