import requests
from models import Anime
API_URL = "https://graphql.anilist.co"
QUERY = """
query($search: String, $perPage: Int) {
    Page(perPage: $perPage) {
        media(search: $search, type: ANIME)  {
        id
        title {romaji english}
        episodes
        genres
        coverImage {large}
        averageScore
        }
    }
}"""

class AniListError(Exception):
    "if an error occurs, this is raised // se um erro ocorre, esse erro é levantado"

def _media_2_anime(media: dict):
    title = media["title"]["english"] or media["title"]["romaji"]
    return Anime(
        anilist_id=media["id"],
        title=title,
        episodes=media["episodes"],
        genres=media["genres"],
        media_type="anime",
        cover_url=media["coverImage"]["large"],
        anilist_score = media["averageScore"]
    )

def searchForAnime(text: str, limit: int = 20):
    if not text.strip():
        return []
    try:
        response = requests.post(API_URL, json = {"query": QUERY, "variables": {"search": text, "perPage": limit}}, timeout=10,)
        response.raise_for_status()
        
    except requests.exceptions.ConnectionError:
        raise AniListError("Connection error: No Internet")
    except requests.exceptions.Timeout:
        raise AniListError(f"Request timed out")
    except requests.exceptions.HTTPError as e:
        raise AniListError(f"API error occurred: {e.response.status_code} - {e.response.text}")
    data = response.json()
    media_array = data["data"]["Page"]["media"]
    return [_media_2_anime(media) for media in media_array]


