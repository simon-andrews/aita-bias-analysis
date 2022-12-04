import json
import os
import re
import sys
from typing import Optional

DATA_DIR = "data"


def extractJudgment(comment_body: str) -> Optional[str]:
    if re.match("yta", comment_body, re.IGNORECASE):
        return "yta"
    elif re.match("nta", comment_body, re.IGNORECASE):
        return "nta"
    elif re.match("esh", comment_body, re.IGNORECASE):
        return "esh"
    elif re.match("nah", comment_body, re.IGNORECASE):
        return "nah"
    elif re.match("info", comment_body, re.IGNORECASE):
        return "info"
    else:
        return None


if __name__ == "__main__":
    for post in os.listdir(DATA_DIR):
        with open(DATA_DIR + "/" + post) as json_file:
            try:
                json_data = json.load(json_file)
            except json.JSONDecodeError:
                print("Empty response")

        if json_data:
            for comment in json_data["comments"]:
                comment["judgment"] = extractJudgment(comment["body"])
            with open(DATA_DIR + "/" + post, "w") as json_file:
                json.dump(json_data, json_file)
