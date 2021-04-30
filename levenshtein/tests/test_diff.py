import pytest

from lcs.diff import diff_


@pytest.mark.parametrize(
    'expected,a,b',
    [
        (
            [('there','>'), ('general', '>'), ('Kenobi', '>'), ('world', '<')], 
            ['Hello', 'there', 'general', 'Kenobi'], 
            ['Hello', 'world']
        ),
        (
            [],
            ['Romeo', 'i', 'Julia'],
            ['Romeo', 'i', 'Julia']
        ),
        (
            [('Hamlet', '>'), ('William', '<'), ('Szekspir', '<')],
            ['Hamlet'],
            ['William', 'Szekspir']
        )
    ]
)
def test_diff(expected, a, b):
    assert sorted(expected) == sorted(diff_(a, b))
