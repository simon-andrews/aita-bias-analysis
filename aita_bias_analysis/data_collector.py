import json
import os
import sys
from datetime import date, datetime, timedelta
from pprint import pprint
from typing import Any, Dict, Generator, List

from pushshift import AITAPost, get_submissions_on_day
from tqdm import tqdm

CACHE_DIR = "cache_test"
DATA_DIR = "data_test"


def date_range(start: date, end: date, step: timedelta) -> List[date]:
    dates = []
    current = start
    while current < end:
        dates.append(current)
        current += step
    return dates


def post_to_dict(post: AITAPost) -> Dict[str, Any]:
    post.get_comments()
    d = post.__dict__
    d["comments"] = [comment.__dict__ for comment in d["comments"]]
    return d


def ensure_data_dir() -> None:
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)


def write_post_data(post: AITAPost) -> None:
    ensure_data_dir()
    id = post.id
    path = os.path.join(DATA_DIR, f"{id}.json")
    if os.path.exists(path):
        return
    with open(path, "w") as f:
        dict_representation = post_to_dict(post)
        json_representation = json.dumps(dict_representation)
        f.write(json_representation)


if __name__ == "__main__":
    d1 = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    d2 = datetime.strptime(sys.argv[2], "%Y-%m-%d")

    dates = date_range(d1, d2, timedelta(days=1))
    date_pbar = tqdm(dates, position=0, desc="date", colour="green")
    for d in date_pbar:
        date_pbar.set_description(str(d))
        try:
            submissions = get_submissions_on_day(d, max_results=500)
        except Exception:
            print(f"failed to get submissions for {d}")
            continue
        try:
            for submission in tqdm(
                submissions, position=1, colour="green", leave=False
            ):
                write_post_data(submission)
        except Exception:
            print(f"failed to get comments for {submission.id}")
