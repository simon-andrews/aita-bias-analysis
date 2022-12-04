import re
from typing import Literal, Optional, Tuple

Gender = Literal["m", "f", "nb"]

age_regex = r"(?P<age>\d+)"
gender_regex = r"(?P<gender>m|f|nb)"
first_person_pronoun_regex = r"(i|me|my|mine|i'd|i'll|i'm|i've)"
age_gender_regex = re.compile(
    f"{first_person_pronoun_regex}\s*{age_regex}\s*{gender_regex}"
)


def get_age_and_gender(text: str) -> Tuple[Optional[int], Optional[Gender]]:
    # Remove all characters but letters, numbers, spaces, and apostrophes.
    text = "".join([c for c in text if c.isalnum() or c in {" ", "'"}])

    # Convert string to lowercase
    text = text.lower()

    # Find all matches
    matches = re.findall(age_gender_regex, text)

    # Get the first one and hope it's right:
    if matches:
        _, age, gender = matches[0]
        return int(age), gender

    # No match found, give up
    return None, None


if __name__ == "__main__":
    import json
    import sys

    with open(f"data/{sys.argv[1]}.json", "r") as f:
        post = json.loads(f.read())
    m = get_age_and_gender(post["text"])
    print(m)
