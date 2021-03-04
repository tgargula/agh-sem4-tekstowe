from pathlib import Path

from algorithms.parse import parse
from algorithms.pattern_matching import fa, kmp, naive
from algorithms.time_test import test

if __name__ == '__main__':
    text = parse(Path('data', 'act.txt'))
    pattern = 'art'
    result = {}

    for f in (naive, fa, kmp):
        result[f.__name__] = test(f, text, pattern)
    
    print(result)
