#!/bin/bash

sudo killall -9 docker
sudo killall -9 dockerd
sudo killall -9 containerd
sudo killall -9 containerd-shim

sudo systemctl restart docker