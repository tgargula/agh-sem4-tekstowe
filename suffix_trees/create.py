from pathlib import Path

from trees import Trie, SuffixTree

if __name__ == '__main__':

    dir = {
        Trie: 'trie',
        SuffixTree: 'suffix_tree'
    }

    data = ('bbbd', 'aabbabd', 'ababcd', 'abcbccd')

    for text in data:
        filename = f'{text}.png'
        T = Trie(text)
        T.save(Path('out', dir[Trie], filename))
        ST = SuffixTree(text)
        ST.save(Path('out', dir[SuffixTree], filename))
