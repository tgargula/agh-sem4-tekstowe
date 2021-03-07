from pathlib import Path

from algorithms.pattern_matching import fa, kmp, naive

if __name__ == '__main__':
    text = Path('data', 'act.txt').open('r').read()
    pattern = 'art'
    
    for f in (naive, fa, kmp):
        print(f'{f.__name__}:')
        print(f(text, pattern))
        print()
