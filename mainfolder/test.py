from nucleo.library import Library
from models import Anime
lib = Library()
a = lib.add(Anime(title="FMA", genres=["Action"]))
b = lib.add(Anime(title="Toradora", genres=["Romance"]))
c = lib.add(Anime(title="Naruto", genres=["Action"]))   # never rated
lib.rate(a.id, 10)
lib.rate(b.id, 8)

assert [x.title for x in lib.ranked()] == ["FMA", "Toradora"]
assert [x.title for x in lib.ranked(genre="Romance")] == ["Toradora"]

lib.create_list("Favorites")
lib.addToList("Favorites", b.id)
assert [x.title for x in lib.ranked(list_name="Favorites")] == ["Toradora"]
print("ranked() works")