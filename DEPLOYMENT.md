# Qmoosa Bot - Production Deployment Guide 🚀

This document outlines the standard production procedures for deploying **Qmoosa Bot** across cloud infrastructures, Docker clusters, and bare-metal servers.

---

## 1. Quick Deploy with Docker Compose (Recommended)

The fastest and most isolated way to run Qmoosa Bot in production is via Docker Compose.

### Prerequisites
- Docker Engine 24.0+
- Docker Compose v2.20+
- 4GB+ RAM (8GB recommended for concurrent browser sessions)

### Deployment Steps
```bash
# 1. Clone repository
git clone https://github.com/elon00/qmoosa-bot.git
cd qmoosa-bot

# 2. Configure production secrets
cp .env.example .env
nano .env

# 3. Build and launch multi-service cluster
docker compose up -d --build

# 4. Verify running services
docker compose ps
```

### Exposed Endpoints:
- **FastAPI Gateway & Swagger UI:** `http://localhost:8000/docs`
- **noVNC Live Virtual Desktop:** `http://localhost:6080/vnc.html`
- **Prometheus Health & Metrics:** `http://localhost:8000/metrics`
- **PostgreSQL Database:** `localhost:5432`

---

## 2. Bare-Metal Linux Deployment (Ubuntu 22.04 / 24.04 LTS)

For maximum performance and direct GPU/Display acceleration:

### Step 1: Install System Dependencies
```bash
sudo apt update && sudo apt install -y \
  python3.11 python3-pip python3-venv \
  xvfb x11vnc fluxbox novnc websockify \
  chromium-browser libnss3 libgconf-2-4 libfontconfig1 \
  curl git
```

### Step 2: Install Dart SDK & Flutter
```bash
# Install Dart SDK
sudo apt-get update && sudo apt-get install -y apt-transport-https
wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/dart.gpg
echo 'deb [signed-by=/usr/share/keyrings/dart.gpg arch=amd64] https://storage.googleapis.com/download.dartlang.org/linux/debian stable main' | sudo tee /etc/apt/sources.list.d/dart_stable.list
sudo apt-get update && sudo apt-get install -y dart
```

### Step 3: Configure Virtual Display (Xvfb)
Create a systemd unit file `/etc/systemd/system/xvfb.service`:
```ini
[Unit]
Description=X Virtual Frame Buffer Service
After=network.target

[Service]
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```
Enable and start the service:
```bash
sudo systemctl enable --now xvfb
```

### Step 4: Launch Qmoosa Bot Master Machine
```bash
cd /opt/qmoosa-bot
pip install -r requirements.txt
python qmoosa_bot_launcher.py
```

---

## 3. Reverse Proxy & SSL Termination (NGINX)

Set up NGINX to route public domain traffic and secure WebSockets:

```nginx
server {
    listen 80;
    server_name bot.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name bot.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/bot.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bot.yourdomain.com/privkey.pem;

    # FastAPI REST & OpenAPI Gateway
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Real-Time WebSocket Streaming
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }

    # noVNC Remote Screen Stream
    location /vnc/ {
        proxy_pass http://127.0.0.1:6080/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }

    # Static Landing Page
    location / {
        root /opt/qmoosa-bot/web;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 4. Post-Quantum Key Rotation & Security Protocol

1. **Vault Encryption:**
   All API keys and blockchain seeds are encrypted with NIST FIPS 203 (ML-KEM-768).
2. **Key Rotation Routine:**
   To rotate master lattice keys without downtime:
   ```bash
   python -c "from security_pqc.key_vault import PQCKeyVault; v = PQCKeyVault(); print(v.list_keys())"
   ```
3. **Audit Notarization:**
   Every mission log is signed with NIST FIPS 204 (ML-DSA-65) for non-repudiation.
