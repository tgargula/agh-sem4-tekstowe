import pytest
from . import lcs
import numpy as np


@pytest.mark.parametrize(
    'expected,a,b',
    [
        (0, '', ''),
        (5, 'Hello', 'Hello'),
        (3, 'lasso', 'las'),
        (2, 'zbcy', 'vbyu'),
        (5, 'abTcHEdeRfghEi', 'zyxTHwutEsRrpE'),
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
        ('THERE', 'abTcHEdeRfghEi', 'zyxTHwutEsRrpE')
    ]
)
def test_lcs_string(expected, a, b):
    assert expected == lcs(a, b)[1]
