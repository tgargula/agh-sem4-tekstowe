import numpy as np
import pytest

from lcs import lcs


@pytest.mark.parametrize(
    'expected,a,b',
    [
        (0, '', ''),
        (5, 'Hello', 'Hello'),
        (3, 'lasso', 'las'),
        (2, 'zbcy', 'vbyu'),
        (5, 'abTcHEdeRfghEi', 'zyxTHwutEsRrpE'),
        (3, ['a', 'b', 'c'], ['a', 'b', 'c']),
        (1, [''], ['']),
        (2, ['ABC', 'B', 'CAA', 'HI'], ['Hello', 'B', 'HI', 'Ja', 'AGdsa']),
        (0, [], []),
    ]
)
def test_lcs_length(expected, a, b):
    assert expected == lcs(a, b)[0]


@pytest.mark.parametrize(
    'expected,a,b',
    [
        ('', '', ''),
        ('Hello', 'Hello', 'Hello'),
        ('las', 'lasso', 'las'),
        ('by', 'zbcy', 'vbyu'),
        ('THERE', 'abTcHEdeRfghEi', 'zyxTHwutEsRrpE'),
        (['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c']),
        ([''], [''], ['']),
        (['B', 'HI'], ['ABC', 'B', 'CAA', 'HI'], ['Hello', 'B', 'HI', 'Ja', 'AGdsa']),
        ([], [], [])
    ]
)
def test_lcs_string(expected, a, b):
    assert expected == lcs(a, b)[1]
