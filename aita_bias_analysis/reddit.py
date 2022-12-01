import os
from pprint import pprint
from typing import List

import praw

EXCLUDED_USERS = {"AutoModerator", "Judgement_Bot_AITA"}

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent="AITA bias project for COMPSCI 690F",
)

r_aita = reddit.subreddit("amitheasshole")


class Comment:
    def __init__(self, praw_comment: praw.models.Comment):
        self.author = praw_comment.author.name
        self.body = praw_comment.body
        self.created = praw_comment.created_utc
        self.edited = praw_comment.edited
        self.id = praw_comment.id
        self.permalink = praw_comment.permalink
        self.score = praw_comment.score

    def __eq__(self, other) -> bool:
        if not isinstance(other, Comment):
            raise NotImplementedError(
                f"comparing Comments to objects of type {type(other)} is not supported"
            )
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self):
        return f"{self.author} on {self.permalink}"


def get_comments(id: str) -> List[Comment]:
    submission = reddit.submission(id=id)
    comments = list()
    for comment in submission.comments:
        if type(comment) is not praw.models.Comment:
            continue
        if comment.author is None or comment.author.name in EXCLUDED_USERS:
            continue
        comments.append(Comment(comment))
    return comments


if __name__ == "__main__":
    comments = get_comments("z9me1u")
    pprint(comments[0].__dict__)
