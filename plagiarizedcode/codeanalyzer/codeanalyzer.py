"""Base class of code analyzer."""

from pathlib import Path
from typing import Union

# TODO CodeFile


class CodeAnalyzer:
    """Base class of code analyzer."""

    def __init__(self):
        """Initializer."""
        self.files = []

    def add_path(self, path: Union[str, Path]) -> None:
        """
        Add to the list of source files the files in path.

        If path is a directory, add every files in it.

        If path is a file, add the file.
        """
        path = Path(path)
        if path.is_dir():
            for filepath in path.rglob("*"):
                self.add_path(filepath)
        elif path.is_file():
            self.files.append(path)

    @property
    def text(self):
        """Return textual representation of the code."""
        raise NotImplementedError("To be implemented by a subclass")

    @property
    def normalized_text(self):
        """
        Return normalized textual representation of the code.

        Comments are ignored, code is indented in a strict fashion.
        """
        raise NotImplementedError("To be implemented by a subclass")
