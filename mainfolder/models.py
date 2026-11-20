from dataclasses import dataclass, field
@dataclass
class Anime:
    title: str
    id: int | None = None
    anilist_id : int | None = None
    genres: list[str] = field(default_factory=list)
    episodes: int | None = None
    rating: int | None = None
    media_type: str = "anime"
    cover_url: str | None = None
    anilist_score: int | None = None
    def __post_init__(self):
        if self.rating is not None and not (1 <= self.rating <= 10):
            raise ValueError("Rating error: rating must be between 1 and 10")
    


