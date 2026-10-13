from database.db import get_connection, init_db
from nucleo.library import Library
from models import Anime
conn = get_connection(":memory:")
init_db(conn)
lib = Library(conn)
ani_title = input("Enter anime title: ")
text = input("Enter anime genres (comma-separated): ")
ani_genres = [g.strip() for g in text.split(",") if g.strip()]
idk = lib.add(Anime(title=ani_title, genres=ani_genres))
assert idk.id == 1
loaded = lib.get(idk.id)
assert loaded.title == ani_title
assert loaded.genres == ani_genres
assert loaded == idk
assert lib.get(67) is None
lib.rate(idk.id, 9)
assert lib.get(idk.id).rating == 9
assert len(lib.all()) == 1
lib.remove(idk.id)
assert lib.get(idk.id) is None
assert lib.all() == []
print("FUNCIONADNDODODOOD")