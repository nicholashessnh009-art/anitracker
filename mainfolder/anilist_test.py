
from database.db import get_connection, init_db
from nucleo.library import Library
from services.anilist import searchForAnime, AniListError

results = searchForAnime("code geass", limit=3)
for a in results:
    print(a.anilist_id, a.title, a.episodes, a.genres, a.cover_url)

assert searchForAnime("   ") == []                  # empty search → no request

conn = get_connection(":memory:")
init_db(conn)
lib = Library(conn)

saved = lib.add(results[0])
loaded = lib.get(saved.id)
assert loaded.anilist_id == results[0].anilist_id
assert loaded.cover_url == results[0].cover_url   # the new column works

try:
    lib.add(results[0])
    assert False, "duplicate should fail"
except ValueError as e:
    print("Blocked duplicate:", e)

print("AniList → Library works")

# movi para services/anilist.py
