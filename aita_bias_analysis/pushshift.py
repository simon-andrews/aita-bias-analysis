"""
Code for interacting with PushShift's API.
"""

import json
from datetime import date, timedelta
from pprint import pprint
from time import mktime
from typing import List, Optional

import requests
from reddit import Comment, get_comments

BASE_API_URL = "https://api.pushshift.io"
SUBMISSION_API_URL = BASE_API_URL + "/reddit/search/submission"


class AITAPost:
    """
    Represents a single post on AITA.
    """

    def __init__(self, data: dict):
        """
        Initialize an AITAPost instance from data about a submission from the PushShift API. This can be either from
        a normal AITA post, or a post on AITAFiltered.
        """

        # If we are given an AITAFiltered post (which is a crosspost to an AITA thread), initialize using the AITA post
        # instead.
        if "crosspost_parent" in data:
            data = data["crosspost_parent_list"][0]

        # Otherwise, initialize normally
        self.author: str = data["author"]
        self.created: int = int(data["created_utc"])
        self.id: str = data["id"]
        self.flair: str = data["link_flair_text"]
        self.permalink: str = data["permalink"]
        self.score: int = data["score"]
        self.text: str = data["selftext"]
        self.title: str = data["title"]
        self.upvote_ratio: float = data["upvote_ratio"]
        self.comments: Optional[List[Comment]] = None

    def get_comments(self) -> List[Comment]:
        if self.comments is None:
            self.comments = get_comments(self.id)
        return self.comments

    def __repr__(self):
        return f"{self.title} ({self.flair})"


def get_submissions_on_day(
    day: date,
    max_results: int = 500,
) -> List[AITAPost]:
    """
    Query the PushShift API for posts on /r/AITAFiltered for a given day.
    """

    # PushShift API expects date ranges to be given as UNIX timestamps.
    unix_timestamp: int = int(mktime(day.timetuple()))
    tomorrow_timestamp: int = unix_timestamp + int(timedelta(days=1).total_seconds())

    # Perform the request, and complain if anything goes wrong
    url = f"{SUBMISSION_API_URL}/?size={max_results}&subreddit=aitafiltered&after={unix_timestamp}&before={tomorrow_timestamp}&sort_type=score"
    r = requests.get(url)
    if r.status_code != 200:
        raise RuntimeError(
            f"got status code {r.status_code} when getting {url} but expected 200"
        )

    # Check that _some_ data was returned, which should pretty much always be the case.
    data = r.json()["data"]
    if not data:
        raise RuntimeWarning(
            f"received no data from PushShift API, so your query ({url}) is probably wrong"
        )

    # All is well, build and return posts.
    return [AITAPost(p) for p in data]


if __name__ == "__main__":
    d = date(2022, 9, 1)
    results = get_submissions_on_day(d, max_results=10)
    results[0].get_comments()
    pprint(json.dumps(results[0]))
