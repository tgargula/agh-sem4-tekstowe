import pytest

from metrics.lcs import lcs

@pytest.mark.parametrize(
    'expected,x,y',
    [
        (0, ['al', 'lg', 'go'], ['og', 'gl', 'la']),
        (3, ['al', 'lg', 'go'], ['al', 'lg', 'go', 'or', 'ry', 'yt', 'tm']),
        (1, ['al', 'lo', 'or'], ['al', 'lg', 'go', 'or', 'ry', 'yt', 'tm'])
    ]
)
def test_lcs(expected, x, y):
    assert expected == lcs(x, y)
    