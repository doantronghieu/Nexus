#!/bin/bash

# Get the absolute path of the project root (one level up from the script location)
NGINX_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$NGINX_PATH/../../../" && pwd)"
NGINX_CONF="$NGINX_PATH/conf/nginx.conf"

echo "Project Root: $PROJECT_ROOT"
echo "Nginx Path: $NGINX_PATH"
echo "Nginx Config: $NGINX_CONF"

case "$1" in
    start)
        nginx -c "$NGINX_CONF" -p "$NGINX_PATH/"
        ;;
    stop)
        nginx -s stop -c "$NGINX_CONF" -p "$NGINX_PATH/"
        ;;
    reload)
        nginx -s reload -c "$NGINX_CONF" -p "$NGINX_PATH/"
        ;;
    test)
        nginx -t -c "$NGINX_CONF" -p "$NGINX_PATH/"
        ;;
    *)
        echo "Usage: $0 {start|stop|reload|test}"
        exit 1
        ;;
esac

# ./devops/setup/nginx/nginx-control.sh test
# ./devops/setup/nginx/nginx-control.sh start
# ./devops/setup/nginx/nginx-control.sh reload
# ./devops/setup/nginx/nginx-control.sh stop