from pyhton.language.python_words import ALL_WORDS


class TypoEngine:
    def __init__(self):
        self.valid_words = ALL_WORDS

    # check if if a word is a valid typo of another word
    def is_valid_typo(self, typo_word: str, original_word: str) -> bool:
        if typo_word == original_word:
            return False

        return (
            self._is_doubled_letter(typo_word, original_word)
            or self._is_missing_letter(typo_word, original_word)
            or self._is_swapped_letters(typo_word, original_word)
        )

    # check if a word is a doubled letter typo
    def _is_doubled_letter(self, typo: str, original: str) -> bool:
        # verify that the typo is 1 character longer
        if len(typo) != len(original) + 1:
            return False

        # double each letter in the original words and check against the typo
        for i in range(len(original)):
            before_double = original[:i]
            char_to_double = original[i]
            after_double = original[i + 1 :]

            doubled_version = before_double + char_to_double + char_to_double + after_double

            if doubled_version == typo:
                return True

        return False

    # check if a word is a missing letter typo
    def _is_missing_letter(self, typo: str, original: str) -> bool:
        # verify that the typo is 1 character shorter
        if len(typo) != len(original) - 1:
            return False

        # remove each letter in the original word and check against the typo
        for i in range(len(original)):
            before_missing = original[:i]
            after_missing = original[i + 1 :]

            missing_version = before_missing + after_missing

            if missing_version == typo:
                return True

        return False

    # check if a word is a swapped letters typo
    def _is_swapped_letters(self, typo: str, original: str) -> bool:
        # verify that the typo is the same length
        if len(typo) != len(original):
            return False

        # swap each pair of adjacent letters and check against the typo.
        for i in range(len(original) - 1):  # len() - 1 as the last letter can't be swapped with anything
            before_swap = original[:i]
            first_char = original[i]
            second_char = original[i + 1]
            after_swap = original[i + 2 :]

            swapped_version = before_swap + second_char + first_char + after_swap

            if swapped_version == typo:
                return True

        return False

    # find the original word from a typo
    def find_original_word(self, typo_word) -> str | None:
        # only consider typos that are longer than 1 character
        if len(typo_word) <= 1:
            return None

        for word in self.valid_words:
            if self.is_valid_typo(typo_word, word):
                return word
        return None

    # check if a word is a valid word in the language
    def is_correct_word(self, word: str) -> bool:
        # only flag correctly spelled words that are longer than 1 character
        if len(word) <= 1:
            return False
        return word in self.valid_words
