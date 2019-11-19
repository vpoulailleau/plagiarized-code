"""Python code file."""

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeFile


class PythonFile(CodeFile):
    """Python code file."""

    supported_extensions = ("py",)

    def _get_text(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def _get_normalized_text(self):
        return self.text