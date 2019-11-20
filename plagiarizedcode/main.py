"""CLI for plagiarizedcode."""

import argparse
from pathlib import Path
from statistics import median, stdev
from typing import List

import simplelogging

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeAnalyzer
from plagiarizedcode.codeanalyzer.python import PythonFile  # noqa
from plagiarizedcode.codeanalyzer.ignoredfile import IgnoredFile  # noqa

log = None
analyzers: List[CodeAnalyzer] = []
result_text = {}
result_normalized_text = {}


def load_analyzers(path: Path) -> None:
    """Load a code analyzer for each child of path."""
    if not path.is_dir():
        log.error("%s is not a directory", path)

    for subpath in path.iterdir():
        log.info("Loading code for: %s", subpath)
        analyzers.append(CodeAnalyzer(name=subpath.name, path=subpath))


def check_for_similarities() -> None:
    def _add_in_result(name):
        if name not in result_text:
            result_text[name] = {}
        if name not in result_normalized_text:
            result_normalized_text[name] = {}

    for index, code in enumerate(analyzers):
        _add_in_result(code.name)
        print(f"{code.name:30}", end=" ", flush=True)
        for other_code in analyzers[index + 1 :]:
            print("#", end="", flush=True)
            _add_in_result(other_code.name)
            text_similarity, normalized_text_similarity = code.compare(
                other_code
            )
            result_text[code.name][other_code.name] = text_similarity
            result_text[other_code.name][code.name] = text_similarity
            result_normalized_text[code.name][
                other_code.name
            ] = normalized_text_similarity
            result_normalized_text[other_code.name][
                code.name
            ] = normalized_text_similarity
        print()


def display_result_dict(result_dict: dict) -> None:
    """Display results of copy analysis dictionary."""
    similarities = []
    for one in result_dict:
        for other in result_dict:
            if one == other:
                continue
            similarities.append(result_dict[one][other])
    xbar = median(similarities)
    dev = stdev(similarities, xbar=xbar)
    for one in result_dict:
        print("-", one)
        for other in result_dict:
            if one == other:
                continue
            value = result_dict[one][other]
            value = value - xbar
            value /= dev
            if value > 1:
                print("    -", other, "######## copy factor", value)
            else:
                # print("    -", other)
                pass  # no display if ok


def display_result() -> None:
    """Display results of copy analysis."""
    print()
    print("#" * 80)
    print("textual comparison")
    print("#" * 80)
    display_result_dict(result_text)
    print()
    print("#" * 80)
    print("normalized textual comparison")
    print("#" * 80)
    display_result_dict(result_normalized_text)


def main():
    """Entry point."""
    global log
    log = simplelogging.get_logger("__main__")

    parser = argparse.ArgumentParser(description="Linter for *.po files.")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "-i",
        "--input-path",
        metavar="PATH",
        type=str,
        help="path of the directory to check",
        default=".",
    )
    args = parser.parse_args()
    if args.verbose < 1:
        log.reduced_logging()
    elif args.verbose < 2:
        log.normal_logging()
    else:
        log.full_logging()

    log.info("Starting analysis of %s", str(args.input_path))
    load_analyzers(Path(args.input_path))
    check_for_similarities()
    display_result()


if __name__ == "__main__":
    main()