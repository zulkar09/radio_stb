FROM python:3.11-slim

# Instalasi library sistem untuk ARM64
RUN apt-get update && apt-get install -y \
    libshout3-dev \
    gcc \
    pkg-config \
    libogg-dev \
    libvorbis-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalasi library python dari requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file ke folder app
COPY . .

# Default menjalankan pemutar radio
CMD ["python", "pemutar_radio.py"]
