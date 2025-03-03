#!bin/bash

# https://github.com/confluentinc/cp-all-in-one
# https://docs.confluent.io/platform/current/get-started/platform-quickstart.html

# sudo systemctl restart docker
# docker system prune -y

wget -O devops/docker/kafka.docker-compose.yaml https://raw.githubusercontent.com/confluentinc/cp-all-in-one/7.7.1-post/cp-all-in-one-kraft/docker-compose.yml

docker compose -p kafka -f devops/docker/kafka.docker-compose.yaml up -d
docker compose -p kafka -f devops/docker/kafka.docker-compose.yaml down
