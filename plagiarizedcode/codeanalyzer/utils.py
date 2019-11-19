"""Helper functions."""

import re
from typing import List


def split_at_parenthesis(text: str) -> List[str]:
    """Return a list of strings with parenthesis as separators."""
    result = []
    match = 1
    while match is not None:
        match = re.search(r"[(){}[\]]", text)
        if match:
            result.append(text[: match.start()])
            result.append(match.group(0))
            text = text[match.end() :]
    if text:
        result.append(text)
    return result


def normalize(text: str) -> str:
    """Remove unnecessary spaces around commas."""
    text = re.sub(r"\s*,\s*", ", ", text)
    return text


def parenthesis_in_one_line(text: str) -> str:
    """Return the content of the parenthesis in one line."""
    parts = split_at_parenthesis(text)
    parenthesis_level = 0
    text = ""
    for index, part in enumerate(parts):
        if part in ")}]":
            parenthesis_level -= 1
        if parenthesis_level == 0:
            text += part
        else:
            try:
                next_part = parts[index + 1]
            except IndexError:
                next_part = ""
            try:
                previous_part = parts[index - 1]
            except IndexError:
                previous_part = ""
            new_part = normalize(part)
            if previous_part in "({[":
                new_part = new_part.lstrip()
            if next_part == "({[":
                new_part = new_part.rstrip()
            text += new_part
        if part in "({[":
            parenthesis_level += 1

    return text
