from pathlib import Path

from algorithms.parse import parse
from algorithms.pattern_matching import fa, kmp, naive

if __name__ == '__main__':
    text = parse(Path('data', 'act.txt'))
    pattern = 'art'
    
    for f in (naive, fa, kmp):
        print(f'{f.__name__}:')
        print(f(text, pattern))
        print()
