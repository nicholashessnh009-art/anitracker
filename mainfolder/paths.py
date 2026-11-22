import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Se o aplicativo estiver empacotado com PyInstaller
    APP_DIR = Path(sys.executable).parent
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    APP_DIR = Path(__file__).resolve().parent
    BUNDLE_DIR = APP_DIR

DATA_DIR = APP_DIR / "data"
