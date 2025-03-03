#!/bin/bash

# Stop and remove all containers
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Remove ALL volumes (not just dangling ones)
docker volume rm $(docker volume ls -q)

# General cleanup
docker system prune -a -f 
docker container prune -f 
docker buildx prune -f
docker network prune -f 
docker volume prune -f
