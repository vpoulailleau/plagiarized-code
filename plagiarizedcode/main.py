"""CLI for plagiarizedcode."""

import argparse
from pathlib import Path

import simplelogging

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeAnalyzer
from plagiarizedcode.codeanalyzer.python import PythonFile  # noqa
from plagiarizedcode.codeanalyzer.ignoredfile import IgnoredFile  # noqa

log = None
analyzers = []


def load_analyzers(path: Path) -> None:
    if not path.is_dir():
        log.error("%s is not a directory", path)

    for subpaths in path.iterdir():
        log.info("Loading code for: %s", subpaths)
        analyzers.append(CodeAnalyzer(subpaths))


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

