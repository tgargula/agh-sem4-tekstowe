import pytest

from metrics.metrics import dice, cosine, lcs, levenshtein

@pytest.mark.parametrize(
    'expected,x',
    [
        (1, ['algo', 'ogla']),
        (0.4, ['algo', 'algorytm'])
    ]
)
def test_dice(expected, x):
    assert expected == dice([0], [1], x, length=2)


@pytest.mark.parametrize(
    'expected,x',
    [
        (1, ['algo', 'ogla']),
        (0.7, ['algo', 'algorytm'])
    ]
)
def test_cosine(expected, x):
    assert expected == cosine([0], [1], x, 2)

    
@pytest.mark.parametrize(
    'expected,x',
    [
        (0.75, ['algo', 'ogla']),
        (0.5, ['algo', 'algorytm']),
        (0.75, ['alor', 'algorytm'])
    ]
)
def test_lcs(expected, x):
    assert expected == lcs([0], [1], x)
    
@pytest.mark.parametrize(
    'expected,x',
    [
        (1, ['algo', 'ogla']),
        (0.5, ['algo', 'algorytm']),
        (0.5, ['alor', 'algorytm'])
    ]
)
def test_levenshtein(expected, x):
    assert expected == levenshtein([0], [1], x)