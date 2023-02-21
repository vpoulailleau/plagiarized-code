"""CLI for plagiarizedcode."""

import argparse
import re
from pathlib import Path

import simplelogging
import textdistance

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeAnalyzer
from plagiarizedcode.codeanalyzer.python import PythonFile  # noqa
from plagiarizedcode.codeanalyzer.ignoredfile import IgnoredFile  # noqa
from plagiarizedcode.codeanalyzer.cpp import CppFile  # noqa

log = None
analyzers: list[CodeAnalyzer] = []
code_blocks = {}
code_blocks_owners = {}
_code_len_cache = {}


def _load_analyzers(path: Path, ignore: list[str]) -> None:
    """Load a code analyzer for each child of path."""
    if not path.is_dir():
        log.error("%s is not a directory", path)

    for subpath in path.iterdir():
        log.info("Loading code for: %s", subpath)
        analyzer = CodeAnalyzer(name=subpath.name, path=subpath, ignore=ignore)
        if len(analyzer):
            analyzers.append(analyzer)


def code_len(code: str) -> int:
    """Return length of normalized code."""
    if code not in _code_len_cache:
        normalized_code = " ".join(code.splitlines())
        normalized_code = re.sub(r"\s+", " ", normalized_code)
        _code_len_cache[code] = len(normalized_code)
    return _code_len_cache[code]


def code_is_similar(code1, code2):
    len_code1 = code_len(code1)
    len_code2 = code_len(code2)
    tolerance = max(len_code1, len_code2) * 0.3
    return textdistance.damerau_levenshtein.distance(code1, code2) < tolerance


def _check_for_similarities() -> None:
    for code in analyzers:
        for block in code.blocks:

            if block not in code_blocks_owners:
                code_blocks_owners[block] = []
            code_blocks_owners[block].append(code.name)

            if block not in code_blocks:
                code_blocks[block] = 0
            for existing_block in code_blocks:
                if code_is_similar(block, existing_block):
                    code_blocks[block] += 1
                    code_blocks[existing_block] += 1

    for block, nb_versions in code_blocks.items():
        code_blocks[block] = nb_versions - 1


def _display_result() -> None:
    """Display results of copy analysis."""
    nb_analyzers = len(analyzers)
    for code in sorted(analyzers):
        print("\n\n")
        print("#" * 80)
        print(code.name)
        for block in code.blocks:
            if (
                # if not only one version
                code_blocks[block] > 1
                # exclude too common parts (statement of the exercice?)
                and code_blocks[block] < 0.8 * nb_analyzers
                # ignore too small blocks
                and len(block.splitlines()) > 2
            ):
                print()
                print("-" * 80)
                print(
                    f"found {code_blocks[block] - 1} " "similar versions of this code"
                )
                print(block[:200] + "…")
                for other_block, owners in code_blocks_owners.items():
                    if code_is_similar(block, other_block):
                        print("\n\n")
                        for owner in owners:
                            print("    - code in", owner)
                        for line in other_block.splitlines()[:20]:
                            print("        ", line)


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
    parser.add_argument(
        "--ignore",
        metavar="PATH",
        type=str,
        nargs="+",
        help="paths to ignore",
        default=[""],
    )
    args = parser.parse_args()
    if args.verbose < 1:
        log.reduced_logging()
    elif args.verbose < 2:
        log.normal_logging()
    else:
        log.full_logging()

    log.info("Starting analysis of %s", str(args.input_path))
    _load_analyzers(Path(args.input_path), args.ignore)
    _check_for_similarities()
    _display_result()


if __name__ == "__main__":
    main()
