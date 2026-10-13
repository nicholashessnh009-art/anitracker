from models import Anime
import sqlite3
import json

class Library:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
    
    def _row_conversion(self, row: sqlite3.Row):
        return Anime(
                    id=row["id"],
                    anilist_id=row["anilist_id"],
                    title=row["title"],
                    episodes=row["episodes"],
                    genres=json.loads(row["genres"]),
                    rating=row["rating"],
                    media_type=row["media_type"],
                )

    def add(self, anime: Anime):
        cursor = self._conn.execute(
            "INSERT INTO anime (anilist_id, title, episodes, genres, rating, media_type) VALUES (?, ?, ?, ?, ?, ?)",
            (anime.anilist_id, anime.title, anime.episodes, json.dumps(anime.genres), anime.rating, anime.media_type,)
        )
        self._conn.commit()
        anime.id = cursor.lastrowid
        return anime

    def get(self, anime_id: int): #anime or none
        cursor = self._conn.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return self._row_conversion(row)

    def all(self):
        cursor = self._conn.execute("SELECT * FROM anime").fetchall()
        return [self._row_conversion(row) for row in cursor]
    
    
    def rate(self, anime_id: int, rating: int):
        if not 1 <= rating <= 10:
            raise ValueError("Rating error: rating must be between 1 and 10")
        anime = self.get(anime_id)
        if anime is None:
            raise ValueError(f"Anime with id {anime_id} not found")
        cursor = self._conn.execute("UPDATE anime SET rating = ? WHERE id = ?", (rating, anime_id))
        if cursor.rowcount == 0:
            raise ValueError(f"Anime with id {anime_id} not found")
        else:
            self._conn.commit()


    def remove(self, anime_id: int):
        cursor = self._conn.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
        if cursor.rowcount == 0:
            raise ValueError(f"Anime with id {anime_id} not found")
        else:
            self._conn.commit()

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

    def removeList(self, list_name: str):
        if list_name not in self._lists:
            raise KeyError(f"RemoveListError: List {list_name} does not exist")
        del self._lists[list_name]
    
            
