from models import Anime

class Library:
    def __init__(self):
        self._anime: dict[int, Anime] = {}
        self._lists: dict[str, set[int]] = {}
        self._next_id = 1

    def add(self, anime: Anime):
        anime.id = self._next_id
        self._anime[anime.id] = anime
        self._next_id += 1
        return anime
    
    def get(self, anime_id: int): #anime or none
        return self._anime.get(anime_id)

    
    def all(self):
        return list(self._anime.values())
    
    def rate(self, anime_id: int, rating: int):
        if not 1 <= rating <= 10:
            raise ValueError("Rating error: rating must be between 1 and 10")
        anime = self.get(anime_id)
        if anime is None:
            raise ValueError(f"Anime with id {anime_id} not found")
        anime.rating = rating

    def remove(self, anime_id: int):
        if anime_id in self._anime:
            del self._anime[anime_id]
        for i in self._lists.values():
            i.discard(anime_id)

    def create_list(self, list_name: str):
        if list_name in self._lists:
            raise KeyError(f"AddListError: List {list_name} already exists")
        self._lists[list_name] = set()

    def addToList(self, list_name: str, anime_id: int):
        if list_name not in self._lists:
            raise KeyError(f"AddToListError: List {list_name} does not exist")
        if anime_id not in self._anime:
            raise KeyError(f"AddToListError: Anime with id {anime_id} does not exist")
        self._lists[list_name].add(anime_id)

    def getList(self, list_name: str):
        if list_name not in self._lists:
            raise KeyError(f"GetListError: List {list_name} does not exist")
        result = []
        for anime_id in self._lists[list_name]:
            anime = self.get(anime_id)
            if anime is not None:
                result.append(anime)
        return result
    
    def ranked(self, genre: str | None = None, list_name: str | None = None):
        if list_name is not None:
            cList = self.getList(list_name)
        else:
            cList = self.all()
        if genre is not None:
            filtered = []
            for anime in cList:
                if genre in anime.genres:
                    filtered.append(anime)
            cList = filtered
        else:
            filtered = cList
        rated = []

        for anime in cList:
            if anime.rating is not None:
                rated.append(anime)
        
        cList = rated
        return sorted(cList, key=lambda anime: anime.rating, reverse=True)
    
            
