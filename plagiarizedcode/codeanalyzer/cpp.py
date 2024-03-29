"""C/C++ code file."""

import re

import simplelogging

from plagiarizedcode.codeanalyzer.codeanalyzer import CodeFile
from plagiarizedcode.codeanalyzer.utils import parenthesis_in_one_line

log = simplelogging.get_logger()


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
                if line.startswith("#") and not line.endswith("\\"):
                    lines.append(line + "\n")
                else:
                    lines.append(line)
        text = " ".join(lines)

        # spaces around parenthesis
        text = re.sub(r" *([{}()[\]]) *", r" \1 ", text)
        # spaces around operators
        text = re.sub(r" *([+-/*<>=&^|~!?:%]+) *", r" \1 ", text)
        # spaces around others
        text = re.sub(r" *([;,]) *", r"\1 ", text)

        text = re.sub(r"[ \t]+", " ", text)

        return text

    def _get_blocks(self) -> list[str]:
        content = [""]
        text = self._get_normalized_text()
        for line in text.splitlines():
            line = line.lstrip()
            if not line:
                continue

            while line:
                old_line = line

                # preprocessor
                if line.startswith("#"):
                    if content[-1].startswith("#"):
                        content[-1] += "\n" + line
                    else:
                        content.append(line)
                    break

                match = ""
                level = 0
                for index, char in enumerate(line):
                    match += char
                    if char == "{":
                        level += 1
                    if char == "}":
                        level -= 1
                    if level == 0:
                        if char == "}":
                            m = re.match(r"[^{};]*;", line[index + 1 :])
                            if m is not None:
                                match += m[0]
                            break
                        elif char == ";":
                            break
                content.append(match.lstrip())
                line = line[len(match) :]

                if old_line == line:
                    log.error("unparsed text: >>>%s", line)
                    break

        return [line for line in content if line.strip()]
