import pytest
from lcs.lcs import lcs_
from lcs.tokenizer import tokenize
from lcs import punch


@pytest.mark.parametrize(
    "expected,text,level",
    [
        (8, "1 2 3 4 5 6 7 8 9 0", 0.2),
        (4, "Hello there! General Kenobi!", 1 / 3),
    ],
)
def test_lcs_of_punched_text(expected, text, level):
    tokens = tokenize(text)
    punched = punch(tokens, level=level)
    lcsv, _ = lcs_(tokens, punched)
    lcsv = lcsv[len(tokens), len(punched)]
    assert expected == lcsv