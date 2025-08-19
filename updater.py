import os
import requests
import shutil
import yaml
from datetime import datetime
from pathlib import Path
import time

CONFIG_FILE = Path("/config/isos.yaml")
DOWNLOAD_DIR = Path("/isos")

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f)
    else:
        print("⚠️ Keine isos.yaml gefunden!")
        return {}

def download_iso(name, url):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_file = DOWNLOAD_DIR / f"{name}-{timestamp}-{filename}"

    print(f"🔽 Lade {name} von {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(new_file, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    print(f"✅ Gespeichert: {new_file}")
    clean_old(name)

def clean_old(name):
    files = sorted(DOWNLOAD_DIR.glob(f"{name}-*.iso")) \
          + sorted(DOWNLOAD_DIR.glob(f"{name}-*.zip")) \
          + sorted(DOWNLOAD_DIR.glob(f"{name}-*.qcow2*"))
    if len(files) > 1:
        for old_file in files[:-1]:
            print(f"🗑️ Lösche alte {name}-ISO: {old_file}")
            old_file.unlink()

if __name__ == "__main__":
    while True:
        config = load_config()
        for name, url in config.items():
            try:
                download_iso(name, url)
            except Exception as e:
                print(f"⚠️ Fehler beim Laden von {name}: {e}")
        print("⏳ Warte 24h bis zum nächsten Lauf...")
        time.sleep(24*60*60)

