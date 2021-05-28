from ahocorasick import Automaton2d
from ahocorasick.stats import TextStats

if __name__ == "__main__":
    with open("haystack.txt", "r") as f:
        lines = f.readlines()

    A = Automaton2d.text(["th", "t h"])

    mapper = {"th": (1, 1), "t h": (2, 2), (1, 1): "'th'", (2, 2): "'t h'"}

    results = A.search2d(lines, [mapper["th"], mapper["t h"]])

    for line, pos, pattern in results:
        mapped = mapper[pattern]
        print(f"{line}-{line+1}:{pos-len(mapped)+3}-{pos}\t{mapped}")
