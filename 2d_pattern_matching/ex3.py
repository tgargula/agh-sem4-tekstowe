from letters.image import Haystack
from ahocorasick import Automaton2d

if __name__ == '__main__':
    haystack = Haystack()
    e = haystack.get('e')
    n = haystack.get('n')
    o = haystack.get('o')
    
    A = Automaton2d.images(patterns=[o, n, e])
    results = A.search2d(haystack.image)
    for line, pos, z in results:
        print(f"{line}:{pos} \t{A.stats.get_repr(z)}")
        