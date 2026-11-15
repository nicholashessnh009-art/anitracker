from database.db import get_connection, init_db
from nucleo.library import Library
from models import Anime
conn = get_connection(':memory:')
init_db(conn)
lib = Library(conn)
# ani_title = input("Enter anime title: ")
# text = input("Enter anime genres (comma-separated): ")
# ani_genres = [g.strip() for g in text.split(",") if g.strip()]
# idk = lib.add(Anime(title=ani_title, genres=ani_genres))
# assert idk.id == 1
# loaded = lib.get(idk.id)
# assert loaded.title == ani_title
# assert loaded.genres == ani_genres
# assert loaded == idk
# assert lib.get(67) is None
# lib.rate(idk.id, 9)
# assert lib.get(idk.id).rating == 9
# assert len(lib.all()) == 1
# lib.remove(idk.id)
# assert lib.get(idk.id) is None
# assert lib.all() == []
# print("FUNCIONADNDODODOOD")

a = lib.add(Anime(title="FMA", genres=["Action"]))
b = lib.add(Anime(title="Toradora", genres=["Romance"]))
lib.rate(a.id, 10)
lib.rate(b.id, 8)

lib.create_list("Favorites")
lib.addToList("Favorites", a.id)
lib.addToList("Favorites", a.id)              # twice → no error, no duplicate
assert [x.title for x in lib.getList("Favorites")] == ["FMA"]

try:
    lib.create_list("Favorites")
    assert False, "duplicate list should fail"
except ValueError:
    pass

assert [x.title for x in lib.ranked(list_name="Favorites")] == ["FMA"]
assert [x.title for x in lib.ranked()] == ["FMA", "Toradora"]

lib.remove(a.id)                              # cascade: FMA leaves the list too
assert lib.getList("Favorites") == []

lib.removeList("Favorites")
try:
    lib.getList("Favorites")
    assert False, "deleted list should fail"
except KeyError:
    pass
print("Lists work with SQLite")
lib.create_list("Watchlist")
lib.addToList("Watchlist", b.id)
lib.listNames()
lib.create_list("1")
lib.create_list("2")
print(lib.listNames())
assert lib.listNames() != ["Watchlist"]
lib.removeFromList("Watchlist", b.id)
print(lib.getList("Watchlist"))
