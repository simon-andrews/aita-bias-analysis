import json
import os
from pprint import pprint
from typing import List

import textstat
from demographic_inference import get_gender_and_age
from judgements import extractJudgment
from tqdm import tqdm

DATA_DIR = "data"
EMPTY_FILES = {"rtl39s", "rykxva", "s7b9m7"}


def load_post(id: str) -> dict:
    file_path = os.path.join(DATA_DIR, f"{id}.json")
    with open(file_path, "r") as f:
        file_contents = f.read()
    post = json.loads(file_contents)
    post["text"] = post["text"].replace("\n", "")
    post["flesch_reading_ease"] = textstat.flesch_reading_ease(post["text"])
    age, gender = get_gender_and_age(post["text"])
    post["op_age"] = age
    post["op_gender"] = gender
    for comment in post["comments"]:
        comment["flesch_reading_ease"] = textstat.flesch_reading_ease(comment["body"])
        comment["judgement"] = extractJudgment(comment["body"])
    return post


def load_posts() -> List[dict]:
    posts = []
    pbar = tqdm(os.listdir("data"))
    for x in pbar:
        x = x[:-5]
        pbar.set_description(x)
        if x in EMPTY_FILES:
            continue
        posts.append(load_post(x))
    return posts


if __name__ == "__main__":
    load_posts()
