import json
import os
from pprint import pprint
from typing import List, Optional

import textstat
from demographic_inference import get_age_and_gender
from judgements import extractJudgment
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

DATA_DIR = "data"
EMPTY_FILES = {"rtl39s", "rykxva", "s7b9m7"}


SENTIMENT_ANALYZER = SentimentIntensityAnalyzer()


def clean_text(text: str) -> str:
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    text = text.replace("\t", " ")
    text = text.strip()
    return text


def load_post(id: str) -> dict:
    file_path = os.path.join(DATA_DIR, f"{id}.json")
    with open(file_path, "r") as f:
        file_contents = f.read()
    post = json.loads(file_contents)
    post["text"] = clean_text(post["text"])
    post["flesch_reading_ease"] = textstat.flesch_reading_ease(post["text"])
    post["op_age"], post["op_gender"] = get_age_and_gender(post["text"])
    post["sentiment"] = SENTIMENT_ANALYZER.polarity_scores(post["text"])["compound"]
    for comment in post["comments"]:
        comment["body"] = clean_text(comment["body"])
        comment["flesch_reading_ease"] = textstat.flesch_reading_ease(comment["body"])
        comment["judgement"] = extractJudgment(comment["body"])
        comment["sentiment"] = SENTIMENT_ANALYZER.polarity_scores(comment["body"])[
            "compound"
        ]
    return post


def load_posts(start: Optional[int] = None, end: Optional[int] = None) -> List[dict]:
    posts = []
    files = os.listdir("data")[start:end]
    pbar = tqdm(files)
    for x in pbar:
        x = x[:-5]
        pbar.set_description(x)
        if x in EMPTY_FILES:
            continue
        posts.append(load_post(x))
    return posts


if __name__ == "__main__":
    posts = load_posts(0, 5)
    one_post = posts[0]
    pprint(one_post["comments"][0])
    del one_post["comments"]
    pprint(one_post)
