"""C/C++ code file."""

import re

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeFile
from plagiarizedcode.codeanalyzer.utils import parenthesis_in_one_line


class CppFile(CodeFile):
    """C/C++ code file."""

    supported_extensions = ("c", "h", "cpp", "hpp")

    def _get_normalized_text(self):
        text = self.text
        lines = []
        # remove multiline comments
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL | re.MULTILINE)
        for line in text.splitlines():
            # remove monoline comments
            line = re.sub(r"//.*$", "", line)
            line = line.rstrip()
            if line:
                lines.append(line)
        text = "\n".join(lines)
        text = parenthesis_in_one_line(text)
        # TODO normalize {}
        return text

    def _get_blocks(self) -> list[str]:
        result = [""]
        # TODO
        # for line in self.normalized_text.splitlines():
        #     if line.endswith("{"):
        #         result.append("{\n")
        #     result[-1] += line.lstrip() + "\n"
        return result
