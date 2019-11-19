"""CLI for plagiarizedcode."""

import argparse

import simplelogging

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeAnalyzer
from plagiarizedcode.codeanalyzer.python import PythonFile  # noqa
from plagiarizedcode.codeanalyzer.ignoredfile import IgnoredFile  # noqa


def main():
    """Entry point."""
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
    analyzer = CodeAnalyzer()
    analyzer.add_path(args.input_path)
    with open("log_text.txt", "w", encoding="utf8") as f:
        f.write(analyzer.text)
    with open("log_normalized_text.txt", "w", encoding="utf8") as f:
        f.write(analyzer.normalized_text)

