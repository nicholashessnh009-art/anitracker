import requests
API_URL = "https://graphql.anilist.co"
## hmmmm puta merda como vou fazer isso daquii
QUERY = """
query($search: String) {
    Page(perPage: 5) {
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
try:
    response = requests.post(API_URL, json = {"query": QUERY, "variables": {"search": "Code Geass"}}, timeout=10,)
    checker = response.raise_for_status()
    if checker is not None:
        print(response.text)
    data = response.json()
    for media in data["data"]["Page"]["media"]:
        title = media["title"]["english"] or media["title"]["romaji"]
        print(media['id'], " ", title, " ", media['episodes'], " ", media['genres'], " ", media['averageScore'])
except requests.exceptions.ConnectionError:
    print("Connection error: No Internet")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"API error occurred: {e.response.status_code} - {e.response.reason}")
