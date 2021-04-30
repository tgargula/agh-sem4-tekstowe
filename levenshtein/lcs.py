from sys import argv
from lcs import lcs, tokenize_from_file, decompose
from itertools import combinations

if __name__ == "__main__":

    files = argv[1:] if argv[1:] else ['data/out1.txt', 'data/out2.txt', 'data/romeo-i-julia-700.txt']

    for f1, f2 in combinations(files, 2):
        t1, t2 = tokenize_from_file(f1), tokenize_from_file(f2)
        d, _ = lcs(decompose(t1), decompose(t2))
        print(f"LCS of {f1} and {f2}: {d}")
