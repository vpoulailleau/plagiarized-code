"""Ignored code file."""

import simplelogging

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeFile

log = simplelogging.get_logger()


class IgnoredFile(CodeFile):
    """Ignored code file."""

    supported_extensions = ("txt", "md", "")

    def __init__(self, path):
        log.info("ignored file: %s", path)
        super().__init__(path)
