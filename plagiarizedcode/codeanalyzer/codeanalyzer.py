"""Base class of code analyzer."""

from pathlib import Path
from typing import Union, Tuple, List, Sequence

import simplelogging

log = simplelogging.get_logger()

_code_file_classes = set()


class _RegisteringMeta(type):
    def __new__(cls, name, bases, class_dict):
        cls = type.__new__(cls, name, bases, class_dict)
        _code_file_classes.add(cls)
        return cls


class CodeFile(metaclass=_RegisteringMeta):
    """Base class of code file."""

    supported_extensions: Tuple[str] = ()  # ("cpp", "cxx", "hpp", "h")

    def __init__(self, path: Path):
        """Initializer."""
        self.path = path
        self._text = None
        self._normalized_text = None

    @property
    def text(self):
        """Return textual representation of the code."""
        if self._text is None:
            self._text = self._get_text()
        return self._text

    @property
    def normalized_text(self):
        """
        Return normalized textual representation of the code.

        Comments are ignored, code is indented in a strict fashion.
        """
        if self._normalized_text is None:
            self._normalized_text = self._get_normalized_text()
        return self._normalized_text

    def _get_text(self) -> str:
        """Return textual representation of the code."""
        raise NotImplementedError("To be implemented by a subclass")

    def _get_normalized_text(self) -> str:
        """
        Return normalized textual representation of the code.

        Comments are ignored, code is indented in a strict fashion.
        """
        raise NotImplementedError("To be implemented by a subclass")


_ignored_dirs = ("venv", "env", ".git", "__pycache__")


class CodeAnalyzer:
    """Code analyzer."""

    def __init__(self, name: str, path=None):
        """Initializer."""
        self.files: List[CodeFile] = []
        self.name = name
        if path:
            self.add_path(path)

    def add_path(self, path: Union[str, Path]) -> None:
        """
        Add to the list of source files the files in path.

        If path is a directory, add every files in it.

        If path is a file, add the file.
        """
        path = Path(path)
        if path.is_dir():
            if path.name in _ignored_dirs:
                log.debug("ignoring directory %s", path)
                return
            for filepath in path.rglob("*"):
                self.add_path(filepath)
        elif path.is_file():
            for dir_ in path.parents:
                if dir_.name in _ignored_dirs:
                    log.debug("ignoring file because of a directory: %s", path)
                    return
            extension = path.suffix
            for cls in _code_file_classes:
                if extension[1:] in cls.supported_extensions:
                    self.files.append(cls(path=path))
                    self.files.sort(key=lambda f: f.path)
                    break
            else:
                log.warning("Unknown extension: %s (%s)", extension, path)

    @property
    def text(self):
        """Return textual representation of the code."""
        return "\n".join(code.text for code in self.files)

    @property
    def normalized_text(self):
        """
        Return normalized textual representation of the code.

        Comments are ignored, code is indented in a strict fashion.
        """
        return "\n".join(code.normalized_text for code in self.files)

    @staticmethod
    def _convolution_item(text1: str, text2: str) -> int:
        return 2

    def _convolution(self, text1: str, text2: str) -> int:
        convolution_range = min(len(text1), len(text2))
        result = 0
        for offset in range(convolution_range + 1):
            result += self._convolution_item(offset * " " + text1, text2)
            result += self._convolution_item(offset * " " + text2, text1)
        return result

    def compare(self, other: "CodeAnalyzer") -> Sequence[int]:
        return (
            self._convolution(self.text, other.text),
            self._convolution(self.normalized_text, other.normalized_text),
        )
