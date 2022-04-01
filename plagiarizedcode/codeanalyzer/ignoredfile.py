"""Ignored code file."""

import simplelogging

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeFile

log = simplelogging.get_logger()


class IgnoredFile(CodeFile):
    """Ignored code file."""

    supported_extensions = (
        "",
        "cbp",
        "csv",
        "depend",
        "iml",
        "jpeg",
        "jpg",
        "json",
        "layout",
        "md",
        "o",
        "odp",
        "ods",
        "out",
        "pdf",
        "rar",
        "sh",
        "text",
        "txt",
        "xml",
        "zip",
        "7z",
    )

    def __init__(self, path):
        log.info("ignored file: %s", path)
        super().__init__(path)

    def _get_text(self):
        return ""

    def _get_normalized_text(self):
        return ""

    def _get_blocks(self) -> list[str]:
        return []
