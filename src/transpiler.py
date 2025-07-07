import re

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
        words = re.findall(r"\w+|[^\w\s]|\s+", pyhton_code)

        result = []
        for word in words:
            if word.isalpha():
                original = self.typo_engine.find_original_word(word)
                if original:
                    result.append(original)
                else:
                    result.append(word)
            else:
                result.append(word)

        return "".join(result)
