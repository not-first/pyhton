import ast

from src.typo_engine import TypoEngine


class PyhtonTranspiler:
    def __init__(self):
        self.typo_engine = TypoEngine()

    def transpile_file(self, input_file: str, output_file: str = None) -> str:
        with open(input_file, "r") as f:
            pyhton_code = f.read()

        python_code = self.transpile_code(pyhton_code)

        if output_file:
            with open(output_file, "w") as f:
                f.write(python_code)

        return python_code

    def transpile_code(self, pyhton_code: str) -> str:
        try:
            # parse the code into an AST
            tree = ast.parse(pyhton_code)

            # find all keyword positions that need conversion
            keyword_positions = self._find_keyword_positions(tree, pyhton_code)

            # convert the code by replacing the keywords needing conversion
            return self._replace_keywords_at_positions(pyhton_code, keyword_positions)

        except SyntaxError:
            return "SYNTAX_ERROR"

    def _find_keyword_positions(self, tree, code):
        positions = []
        lines = code.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 'def' keyword
                self._add_keyword_at_position(node, lines, positions, "def")

            elif isinstance(node, ast.Call):
                # function calls - check if it's a builtin
                if isinstance(node.func, ast.Name):
                    self._add_exact_word_at_position(node.func, lines, positions)

            elif isinstance(node, ast.Return):
                # 'return' keyword
                self._add_keyword_at_position(node, lines, positions, "return")

            elif isinstance(node, ast.If):
                # 'if' keyword and handle elif/else
                self._add_keyword_at_position(node, lines, positions, "if")
                # Handle elif and else clauses
                self._handle_if_elif_else(node, lines, positions)

            elif isinstance(node, ast.For):
                # 'for' keyword
                self._add_keyword_at_position(node, lines, positions, "for")

            elif isinstance(node, ast.While):
                # 'while' keyword
                self._add_keyword_at_position(node, lines, positions, "while")

            elif isinstance(node, ast.Import):
                # 'import' keyword
                self._add_keyword_at_position(node, lines, positions, "import")

            elif isinstance(node, ast.ImportFrom):
                # 'from' keyword
                self._add_keyword_at_position(node, lines, positions, "from")

        return positions

    def _handle_if_elif_else(self, if_node, lines, positions):
        current_line = if_node.lineno

        # look for elif and else keywords in subsequent lines
        for i, line in enumerate(lines[current_line:], start=current_line + 1):
            stripped = line.strip()
            if stripped.startswith("elif "):
                # found elif
                elif_pos = line.find("elif")
                if elif_pos != -1:
                    positions.append({"line": i, "start": elif_pos, "end": elif_pos + 4, "word": "elif"})
            elif stripped.startswith("else:"):
                # found else
                else_pos = line.find("else")
                if else_pos != -1:
                    positions.append({"line": i, "start": else_pos, "end": else_pos + 4, "word": "else"})
                break  # else is the last clause
            elif stripped and not stripped.startswith(" ") and not stripped.startswith("\t") and stripped != "else:":
                # Hit a new statement at the same indentation level, stop looking
                break

    def _add_keyword_at_position(self, node, lines, positions, keyword):
        if hasattr(node, "lineno") and hasattr(node, "col_offset"):
            line_idx = node.lineno - 1
            if 0 <= line_idx < len(lines):
                line = lines[line_idx]
                # find the keyword in the line starting from col_offset
                start_pos = line.find(keyword, node.col_offset)
                if start_pos != -1:
                    positions.append(
                        {
                            "line": node.lineno,
                            "start": start_pos,
                            "end": start_pos + len(keyword),
                            "word": line[start_pos : start_pos + len(keyword)],
                        }
                    )

    def _add_exact_word_at_position(self, node, lines, positions):
        if hasattr(node, "lineno") and hasattr(node, "col_offset") and hasattr(node, "id"):
            line_idx = node.lineno - 1
            if 0 <= line_idx < len(lines):
                line = lines[line_idx]
                word = node.id
                start_pos = node.col_offset
                if start_pos + len(word) <= len(line):
                    actual_word = line[start_pos : start_pos + len(word)]
                    if actual_word == word:  # make sure it matches
                        positions.append(
                            {"line": node.lineno, "start": start_pos, "end": start_pos + len(word), "word": word}
                        )

    def _replace_keywords_at_positions(self, code, positions):
        lines = code.split("\n")

        # group positions by line number
        positions_by_line = {}
        for pos in positions:
            line_num = pos["line"]
            if line_num not in positions_by_line:
                positions_by_line[line_num] = []
            positions_by_line[line_num].append(pos)

        # sort positions by start position (right to left) to avoid offset issues
        for line_num in positions_by_line:
            positions_by_line[line_num].sort(key=lambda x: x["start"], reverse=True)

        # replace keywords line by line
        for line_num, line_positions in positions_by_line.items():
            line_idx = line_num - 1
            if 0 <= line_idx < len(lines):
                line = lines[line_idx]

                for pos in line_positions:
                    word = pos["word"]
                    correct_word = self.typo_engine.find_correct_word(word)

                    if correct_word and correct_word != word:
                        # replace the word at the exact position
                        line = line[: pos["start"]] + correct_word + line[pos["end"] :]

                lines[line_idx] = line

        return "\n".join(lines)
