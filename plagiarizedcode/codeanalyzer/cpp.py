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
        text = re.sub(r"[ \t]+", " ", text)

        return text

    def _get_blocks(self) -> list[str]:
        result = [""]
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
                for char in line:
                    match += char
                    if char == "{":
                        level += 1
                    if char == "}":
                        level -= 1
                    if level == 0 and char == ";":
                        break
                content.append(match.lstrip())
                line = line[len(match) :]

                if old_line == line:
                    log.error("unparsed text: >>>%s", line)
                    break

        log.warning("\n\n".join(content))

        # TODO
        # for line in self.normalized_text.splitlines():
        #     if line.endswith("{"):
        #         result.append("{\n")
        #     result[-1] += line.lstrip() + "\n"
        return result
