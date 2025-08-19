FROM python:3.11-slim

# benötigte Tools installieren
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Script ins Image kopieren
COPY updater.py /app/updater.py

# YAML- und HTTP-Support für Python
RUN pip install pyyaml requests

# Volumes für ISOs & Config
VOLUME ["/isos", "/config"]

# Startbefehl
CMD ["python", "/app/updater.py"]

