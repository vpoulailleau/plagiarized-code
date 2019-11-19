"""Python code file."""

import re

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeFile


class PythonFile(CodeFile):
    """Python code file."""

    supported_extensions = ("py",)

    def _get_text(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def _get_normalized_text(self):
        # TODO parenthesis content on one line
        # TODO dict literal on one line
        # TODO list literal on one line
        # TODO set literal on one line
        lines = []
        # remove docstrings and other multiline strings
        text = re.sub(
            r'""".*?"""', "", self.text, flags=re.DOTALL | re.MULTILINE
        )
        for line in text.splitlines():
            # remove comments
            line = re.sub(r"#.*$", "", line)
            line = line.rstrip()
            if line:
                lines.append(line)
        return "\n".join(lines)
