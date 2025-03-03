# Nginx Setup Guide

## 1. Install Nginx

```bash
# For MacOS
brew install nginx

# For Ubuntu/Debian
sudo apt update
sudo apt install nginx

# For Windows
# Download from nginx.org
```

## 2. Setup Project Structure

```bash
# From project root
mkdir -p devops/setup/nginx
cd devops/setup/nginx
mkdir logs conf
```

## 3. Configure Nginx

Create `devops/setup/nginx/conf/nginx.conf` with proxy settings:

```nginx
server {
    listen 80;
    server_name localhost;

    # Backend API (FastAPI on 8000)
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Frontend (Nuxt.js on 3000)
    location /ui/ {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 4. Control Commands

From project root:

```bash
# Start Nginx
nginx -c devops/setup/nginx/conf/nginx.conf -p devops/setup/nginx

# Test configuration
nginx -t -c devops/setup/nginx/conf/nginx.conf -p devops/setup/nginx

# Stop Nginx
nginx -s stop -c devops/setup/nginx/conf/nginx.conf -p devops/setup/nginx

# Reload configuration
nginx -s reload -c devops/setup/nginx/conf/nginx.conf -p devops/setup/nginx
```

## 5. Optional: Setup Control Script

```bash
# From project root
chmod +x devops/setup/nginx/nginx-control.sh

# Usage
./devops/setup/nginx/nginx-control.sh start
./devops/setup/nginx/nginx-control.sh stop
./devops/setup/nginx/nginx-control.sh reload
./devops/setup/nginx/nginx-control.sh test
```

## 6. Frontend Deployment

From project root:

```bash
npm run build
docker buildx prune -f
docker-compose -f devops/docker/ui.docker-compose.yaml up -d --build
```

## 7. Test Access

```bash
# Test backend
curl http://localhost

# Start ngrok
ngrok http 80
```

## Access Points

`ngrok http --url=positive-viper-presently.ngrok-free.app 80`

After starting ngrok, your services will be available at:

- Backend (FastAPI): `https://[ngrok-url]/`
- Frontend (Nuxt.js): `https://[ngrok-url]/ui/`

## Monitoring

```bash
# Check nginx logs from project root
tail -f devops/setup/nginx/logs/error.log
tail -f devops/setup/nginx/logs/access.log
```
