#!/bin/bash

#!/bin/bash
# Clean up Docker system

# Remove unused Docker images and build cache
docker builder prune -a
docker network prune -f

# Remove any dangling images that are not associated with a container
docker rmi $(docker images -f "dangling=true" -q)