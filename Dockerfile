# ==============================================================================
# QMOOSA BOT - PRODUCTION CONTAINER DOCKERFILE
# Autonomous Agentic OS with Virtual Desktop, Screen Controller & PQC
# ==============================================================================

FROM python:3.11-slim

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV SCREEN_WIDTH=1920
ENV SCREEN_HEIGHT=1080
ENV SCREEN_DEPTH=24

# Install Linux X11, Xvfb virtual display, fluxbox WM, noVNC, and Chromium browser
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    fluxbox \
    novnc \
    websockify \
    net-tools \
    curl \
    git \
    chromium \
    chromium-driver \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Qmoosa Bot codebase
COPY . .

# Expose ports:
# 8000: FastAPI Gateway / REST API
# 6080: noVNC WebRTC Screen Stream
# 8080: Serverpod WebSocket Gateway
EXPOSE 8000 6080 8080

# Production startup entrypoint script
RUN chmod +x run_qmoosa_bot.bat

CMD ["python", "qmoosa_bot_launcher.py"]
