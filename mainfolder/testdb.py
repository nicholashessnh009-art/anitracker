from database import db
import sqlite3

conn = db.get_connection("anitracker.db")
db.init_db(conn)
tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
print(f"1. - tables: {tables}")
print(f"{db.DEFAULT_DB_PATH}")
conn.close()

conn = db.get_connection(":memory:")
db.init_db(conn)

conn.execute("INSERT INTO lists (name) VALUES (?)", ("Favorites",))
try:
    conn.execute("INSERT INTO list_items (list_id, anime_id) VALUES (?, ?)", (1, 999))
    print("Error: foreign key constraint not enforced")
except sqlite3.IntegrityError as e:
    print(f" 2. Foreign key constraint enforced: {e}")

conn.execute("INSERT INTO anime (title) VALUES (?)", ("Solo Leveling",))
conn.execute("INSERT INTO list_items (list_id, anime_id) VALUES (?, ?)", (1, 1))
conn.commit()
everything = conn.execute("SELECT * FROM list_items").fetchall()
print(f"3. ok" if everything == [] else f"3. not ok: {everything}")
conn.close()