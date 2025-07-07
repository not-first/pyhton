from src.typo_engine import TypoEngine


def test_doubled_letter_typos():
    engine = TypoEngine()

    assert engine.find_original_word("deff") == "def"
    assert engine.find_original_word("prrint") == "print"
    assert engine.find_original_word("iff") == "if"
    assert engine.find_original_word("retuurn") == "return"

    assert engine.is_valid_typo("deff", "def")
    assert engine.is_valid_typo("prrint", "print")


def test_missing_letter_typos():
    engine = TypoEngine()

    assert engine.find_original_word("prnt") == "print"
    assert engine.find_original_word("retur") == "return"
    assert engine.find_original_word("inpu") == "input"
    assert engine.find_original_word("de") == "def"

    assert engine.is_valid_typo("prnt", "print")
    assert engine.is_valid_typo("retur", "return")


def test_swapped_letter_typos():
    engine = TypoEngine()

    assert engine.find_original_word("pritn") == "print"
    assert engine.find_original_word("esle") == "else"
    assert engine.find_original_word("Fasle") == "False"
    assert engine.find_original_word("Treu") == "True"

    assert engine.is_valid_typo("pritn", "print")
    assert engine.is_valid_typo("esle", "else")


def test_invalid_typos():
    engine = TypoEngine()

    # non python words
    assert engine.find_original_word("hello") is None
    assert engine.find_original_word("world") is None
    assert engine.find_original_word("xyz") is None

    # too many changes
    assert engine.find_original_word("defff") is None
    assert engine.find_original_word("pr") is None

    # same word (not a typo)
    assert engine.find_original_word("print") is None
    assert engine.find_original_word("def") is None


def test_edge_cases():
    engine = TypoEngine()

    # empty strings
    assert engine.find_original_word("") is None

    # single character scenarios (testing the logic)
    assert engine.is_valid_typo("aa", "a")  # doubled
    assert engine.is_valid_typo("", "a")  # missing
