import sqlite3
import json
import os
from pathlib import Path
SCHEMA = """
CREATE TABLE IF NOT EXISTS anime (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    anilist_id  INTEGER UNIQUE,
    title       TEXT NOT NULL,
    episodes    INTEGER,
    genres      TEXT NOT NULL DEFAULT '[]',
    rating      INTEGER CHECK (rating BETWEEN 1 AND 10),
    media_type  TEXT NOT NULL DEFAULT 'anime',
    cover_url TEXT,
    anilist_score INTEGER
);

CREATE TABLE IF NOT EXISTS lists (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS list_items (
    list_id INTEGER NOT NULL REFERENCES lists(id) ON DELETE CASCADE,
    anime_id INTEGER NOT NULL REFERENCES anime(id) ON DELETE CASCADE,
    PRIMARY KEY (list_id, anime_id)
);
"""

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "anitracker.db"

def get_connection(path=DEFAULT_DB_PATH) -> sqlite3.Connection:
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)

    try:  # adiciona a coluna anilist_score se não existir (como eu adicionei mais uma coluna)
        conn.execute("ALTER TABLE anime ADD COLUMN anilist_score INTEGER")
    except sqlite3.OperationalError:
        pass # ja existeeee \>O</