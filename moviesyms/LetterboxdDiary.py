from typing import TypedDict
import datetime as dt


class LetterboxdDiary(TypedDict):
    date: dt.datetime
    name: str
    year: int
    letterboxd_uri: str
    rating: float
    rewatch: bool
    tags: str
    watched_date: dt.datetime
