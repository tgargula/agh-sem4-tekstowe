from pathlib import Path
from pprint import pprint

from algorithms.pattern_matching import fa, kmp, naive
from algorithms.time_test import test

if __name__ == '__main__':
    text = Path('data', 'act.txt').open('r').read()
    pattern = 'art'
    result = {}

    for f in (naive, fa, kmp):
        result[f.__name__] = test(f, text, pattern)
    
    pprint(result)
