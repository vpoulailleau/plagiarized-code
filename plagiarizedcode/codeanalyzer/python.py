"""Python code file."""

import re

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeFile
from plagiarizedcode.codeanalyzer.utils import parenthesis_in_one_line


class PythonFile(CodeFile):
    """Python code file."""

    supported_extensions = ("py",)

    def _get_text(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def _get_normalized_text(self):
        text = self.text
        lines = []
        # remove docstrings and other multiline strings
        text = re.sub(r'""".*?"""', "", text, flags=re.DOTALL | re.MULTILINE)
        for line in text.splitlines():
            # remove comments
            line = re.sub(r"#.*$", "", line)
            line = line.rstrip()
            if line:
                lines.append(line)
        text = "\n".join(lines)
        text = parenthesis_in_one_line(text)
        return text
