import pytest
from . import levenshtein, show
from .levenshtein import path
import numpy as np


p = np.zeros(shape=(3,3))
p[2,2] = 1
p[2,1] = -1

@pytest.mark.parametrize(
    "expected,parents",
    [
        ([0, 0, 0], np.zeros(shape=(4, 4))),
        ([2, 2], np.full(shape=(3, 3), fill_value=2)),
        ([0, -1, 1], p)
    ]
)
def test_path(expected, parents):
    assert expected == list(path(parents))


@pytest.mark.parametrize(
    "expected,a,b",
    [
        (2, 'los', 'kloc'),
        (3, 'Łódź', 'Lodz'),
        (5, 'quintessence', 'kwintesencja'),
        (7, 'ATGAATCTTACCGCCTCG', 'ATGAGGCTCTGGCCCCTG'),
        (5, '', 'Hello'),
        (6, 'world!', ''),
    ]
)
def test_levenshtein_distance(expected, a, b):
    assert expected == levenshtein(a, b)[0]


@pytest.mark.parametrize(
    "a,b",
    [
        ('los', 'kloc'),
        ('Łódź', 'Lodz'),
        ('quintessence', 'kwintesencja'),
        ('ATGAATCTTACCGCCTCG', 'ATGAGGCTCTGGCCCCTG'),
        ('', 'Hello'),
        ('world!', ''),
    ]
)
def test_levenshtein_reverse(a, b):
    _, path = levenshtein(a, b)
    assert b == show(a, b, path)
