import json
import os
from pprint import pprint
from typing import List, Optional

import numpy as np
import pandas as pd
import sklearn
import textstat
from demographic_inference import get_age_and_gender
from judgements import ah_judgement_ratio, extractJudgment
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
    post["word_count"] = len(post["text"].split(" "))
    post["op_age"], post["op_gender"] = get_age_and_gender(post["text"])
    post["sentiment"] = SENTIMENT_ANALYZER.polarity_scores(post["text"])["compound"]
    for comment in post["comments"]:
        comment["body"] = clean_text(comment["body"])
        comment["word_count"] = len(clean_text(comment["body"]).split(" "))
        comment["flesch_reading_ease"] = textstat.flesch_reading_ease(comment["body"])
        comment["judgement"] = extractJudgment(comment["body"])
        comment["sentiment"] = SENTIMENT_ANALYZER.polarity_scores(comment["body"])[
            "compound"
        ]
    post["ah_judgement_ratio"] = ah_judgement_ratio(post)
    return post


def load_posts(start: Optional[int] = None, end: Optional[int] = None) -> List[dict]:
    posts = []
    files = os.listdir("data")[start:end]
    pbar = tqdm(files)
    for x in pbar:
        x = x[:-5]
        pbar.set_description(f"loading post: {x}")
        if x in EMPTY_FILES:
            continue
        posts.append(load_post(x))
    return posts


def flatten_post(post: dict) -> pd.DataFrame:
    records = []
    op_data = {
        "op_ah_judgement_ratio": post["ah_judgement_ratio"],
        "op_created": post["created"],
        "op_flair": post["flair"],
        "op_flesch_reading_ease": post["flesch_reading_ease"],
        "op_age": post["op_age"],
        "op_gender": post["op_gender"],
        "op_permalink": post["permalink"],
        "op_score": post["score"],
        "op_sentiment": post["sentiment"],
        "op_upvote_ratio": post["upvote_ratio"],
        "op_word_count": post["word_count"]
    }
    for comment in post["comments"]:
        record = op_data.copy()
        record["comment_created"] = int(comment["created"])
        record["comment_flesch_reading_ease"] = comment["flesch_reading_ease"]
        record["comment_judgement"] = comment["judgement"]
        record["comment_permalink"] = comment["permalink"]
        record["comment_score"] = comment["score"]
        record["comment_sentiment"] = comment["sentiment"]
        record["comment_word_count"] = comment["word_count"]
        record["comment_tree_depth"] = comment["tree_depth"]
        records.append(record)
    df = pd.DataFrame.from_records(records)
    return df


def flatten_posts(posts: List[dict]) -> pd.DataFrame:
    pbar = tqdm(posts)
    fs = []
    for post in pbar:
        pbar.set_description(f"flattening post: {post['id']}")
        fs.append(flatten_post(post))
    return pd.concat(fs)


if __name__ == "__main__":
    posts = load_posts()
    df = flatten_posts(posts)
    print(df.describe())
    df.to_csv("data.csv")
