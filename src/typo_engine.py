"""Typo generation and validation logic."""

from .python_words import ALL_WORDS


class TypoEngine:
    def __init__(self):
        self.valid_words = ALL_WORDS

    def is_valid_typo(self, typo_word: str, original_word: str) -> bool:
        if typo_word == original_word:
            return False

        return (
            self._is_doubled_letter(typo_word, original_word)
            or self._is_missing_letter(typo_word, original_word)
            or self._is_swapped_letters(typo_word, original_word)
        )

    def _is_doubled_letter(self, typo: str, original: str) -> bool:
        # verify that the typo is 1 character longer:
        if len(typo) != len(original) + 1:
            return False

        # double each letter in the original word and check against typo
        for i in range(len(original)):
            doubled_version = original[:i] | original[i] + original[i:]

            if doubled_version == typo:
                return True

        return False

    def _is_missing_letter(self, typo: str, original: str) -> bool:
        # i will add this functionality later
        pass

    def _is_swapped_letters(self, typo: str, original: str) -> bool:
        # I will add this functionality later
        pass

    def find_original_word(self, typo_word) -> str | None:
        for word in self.valid_words:
            if self.is_valid_typo(typo_word, word):
                return word
        return None

    def suggest_valid_typos(self, originalword: str) -> list[str]:
        # to be used to error messages, add this later
        suggestions = []

        return suggestions
