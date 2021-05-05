import pytest

from metrics.metrics import dice, cosine, euclidean

@pytest.mark.parametrize(
    'expected,x,y',
    [
        (1, {'al': 1, 'lg': 1, 'go': 1}, {'og': 1, 'gl': 1, 'la': 1}),
        (0.4, {'al': 1, 'lg': 1, 'go': 1}, {'al': 1, 'lg': 1, 'go': 1, 'or': 1, 'ry': 1, 'yt': 1, 'tm': 1})
    ]
)
def test_dice(expected, x, y):
    assert expected == dice(x, y)


@pytest.mark.parametrize(
    'expected,x,y',
    [
        (1, {'al': 1, 'lg': 1, 'go': 1}, {'og': 1, 'gl': 1, 'la': 1}),
        (0.7, {'al': 1, 'lg': 1, 'go': 1}, {'al': 1, 'lg': 1, 'go': 1, 'or': 1, 'ry': 1, 'yt': 1, 'tm': 1})
    ]
)
def test_cosine(expected, x, y):
    assert expected == cosine(x, y)


@pytest.mark.parametrize(
    'expected,x,y',
    [
        (0.816496580927726, {'al': 1, 'lg': 1, 'go': 1}, {'og': 1, 'gl': 1, 'la': 1}),
        (0.4364357804719847, {'al': 1, 'lg': 1, 'go': 1}, {'al': 1, 'lg': 1, 'go': 1, 'or': 1, 'ry': 1, 'yt': 1, 'tm': 1}),
    ]
)
def test_euclidean(expected, x, y):
    assert expected == euclidean(x, y)


if __name__ == '__main__':
    euclidean({'al': 1, 'lg': 1, 'go': 1}, {'al': 1, 'lg': 1, 'go': 1, 'or': 1, 'ry': 1, 'yt': 1, 'tm': 1})