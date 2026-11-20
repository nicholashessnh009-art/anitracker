import requests
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "covers"

def load_cover(url):
    if not url:
        return None
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    file = CACHE_DIR / url.rsplit("/", 1)[-1]
    if file.exists():
        return file.read_bytes()
    try:
        data = requests.get(url, timeout=5).content
    except requests.exceptions.RequestException:
        return None
    file.write_bytes(data)
    return data