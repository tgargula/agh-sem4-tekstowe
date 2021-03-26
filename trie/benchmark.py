from pathlib import Path
from time import time

from trees import Trie, SuffixTree


def benchmark(Class, *args):
    start = time()
    Class(*args)
    return time() - start


if __name__ == '__main__':
    with open(Path('data', 'act.txt'), 'r') as f:
        x = f.read()
    x = ''.join(x) + '$'

    data = ('bbbd', 'aabbabd', 'ababcd', 'abcbccd')

    for text in data:
        print(f'Trie ({text}):\t\t{benchmark(Trie, text)}')
        print(f'SuffixTree ({text}):\t{benchmark(SuffixTree, text)}')

    print(f'Trie (act.txt):\t\t{benchmark(Trie, x)}')
    print(f'SuffixTree (act.txt):\t{benchmark(SuffixTree, x)}')
