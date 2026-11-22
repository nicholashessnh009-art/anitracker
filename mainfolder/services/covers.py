import requests
from pathlib import Path
from paths import DATA_DIR
CACHE_DIR = DATA_DIR / "covers"

def load_cover(url):
    if not url:
        return None
    
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    file = CACHE_DIR / url.rsplit("/", 1)[-1]
    if file.exists():
        return file.read_bytes()
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
            return None
    file.write_bytes(response.content)
    return response.content