import pytest

from lcs import punch, decompose
from lcs.tokenizer import tokenize, nlp


@pytest.mark.parametrize(
    "expected,text",
    [
        ([nlp("Przykładowy "), nlp("tekst")], "Przykładowy tekst"),
        ([nlp("Hello "), nlp("there"), nlp("!")], "Hello there!"),
    ],
)
def test_tokenize(expected, text):
    expected = [text.text_with_ws for text in expected]
    got = [text.text_with_ws for text in tokenize(text)]
    assert expected == got


@pytest.mark.parametrize(
    "expected,text,level",
    [
        (8, "1 2 3 4 5 6 7 8 9 0", 0.2),
        (4, "Hello there! General Kenobi!", 1 / 3),
    ],
)
def test_punch(expected, text, level):
    tokens = tokenize(text)
    punched = punch(tokens, level=level)
    assert expected == len(punched)


@pytest.mark.parametrize(
    "expected,text",
    [
        (
            ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0"],
            "1 2 3 4 5 6 7 8 9 0",
        ),
        (
            ["Hello ", "there", "! ", "General ", "Kenobi", "!"],
            "Hello there! General Kenobi!",
        ),
    ],
)
def test_decompose(expected, text):
    tokens = tokenize(text)
    got = decompose(tokens)
    assert expected == got
