import pytest

from metrics.ngrams import ngrams, ngrams_text


@pytest.mark.parametrize(
    'expected,string,length',
    [
        ({'al': 1, 'lg': 1, 'go': 1, 'or': 1, 'ry': 1, 'yt': 1, 'tm': 1}, "algorytm", 2),
        ({'alg': 1, 'lgo': 1, 'gor': 1, 'ory': 1, 'ryt': 1, 'ytm': 1}, "algorytm", 3),
        ({'la': 3, 'al': 2}, "lalala", 2),
    ]
)
def test_ngrams(expected, string, length):
    assert expected == ngrams(string, length=length)


@pytest.mark.parametrize(
    'expected,text,length,delimiter',
    [
        (
            {'Mężny bądź,': 1, 'bądź, chroń': 1, 'chroń pułk': 1, 'pułk twój': 1, 'twój i': 1,
             'i sześć': 1, 'sześć flag': 1},
            'Mężny bądź, chroń pułk twój i sześć flag',
            2,
            ' '
        ),
        (
            {'Hello there! General': 1, 'there! General Kenobi!': 1},
            'Hello there! General Kenobi!',
            3,
            ' '
        ),
        (
            {'Ich': 1, 'heiße': 2, 'Tomek': 2, 'ich': 1},
            'Ich heiße Tomek Tomek heiße ich',
            1,
            ' '
        )
    ]
)
def test_ngrams_text(expected, text, length, delimiter):
    assert expected == ngrams_text(text, length=length, delimiter=delimiter)
