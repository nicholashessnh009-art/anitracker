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
                    cover_url=row["cover_url"],
                )
    def _list_id(self, list_name: str):
        row = self._conn.execute("SELECT id FROM lists WHERE name = ?", (list_name,)).fetchone()
        if row is None:
            raise KeyError(f"List {list_name} does not exist")
        return row["id"]
    
    def add(self, anime: Anime):
        try:
            cursor = self._conn.execute(
                "INSERT INTO anime (anilist_id, title, episodes, genres, rating, media_type, cover) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (anime.anilist_id, anime.title, anime.episodes, json.dumps(anime.genres), anime.rating, anime.media_type, anime.cover_url)
            )
        except sqlite3.IntegrityError:
            raise ValueError(f"Anime already in library: {anime.title}")
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
    
        
        cursor = self._conn.execute("UPDATE anime SET rating = ? WHERE id = ?", (rating, anime_id))
        if cursor.rowcount == 0:
            raise KeyError(f"Anime with id {anime_id} not found")
        else:
            self._conn.commit()


    def remove(self, anime_id: int):
        cursor = self._conn.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
        if cursor.rowcount == 0:
            raise KeyError(f"Anime with id {anime_id} not found")
        else:
            self._conn.commit()

    def create_list(self, list_name: str):
        try: 
            self._conn.execute("INSERT INTO lists (name) VALUES (?)", (list_name,))
        except sqlite3.IntegrityError:
            raise ValueError(f"CreateListError: List {list_name} already exists")
        self._conn.commit()

    def addToList(self, list_name: str, anime_id: int):
        list_id = self._list_id(list_name)
        if self.get(anime_id) is None:
            raise KeyError(f"AddToListError: Anime with id {anime_id} does not exist")
        self._conn.execute("INSERT OR IGNORE INTO list_items (list_id, anime_id) VALUES (?, ?)", (list_id, anime_id),)
        self._conn.commit()

    def getList(self, list_name: str):
        list_id = self._list_id(list_name)
    
        rows = self._conn.execute("SELECT anime.* FROM anime JOIN list_items ON list_items.anime_id = anime.id WHERE list_items.list_id = ? ", (list_id,),).fetchall()
        return [self._row_conversion(row) for row in rows]
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
        list_id = self._list_id(list_name)
        self._conn.execute("DELETE FROM lists WHERE id = ?", (list_id,))
        self._conn.commit()
    
            
