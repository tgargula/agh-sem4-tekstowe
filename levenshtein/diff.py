from lcs import diff
from lcs.diff import diff_text

if __name__ == "__main__":

    d = diff("data/romeo-i-julia-700.txt", "data/out1.txt")
    # d = diff("data/data1.txt", "data/data2.txt")

    for line, diffrence in d.items():
        print(f"{line} :")
        for pointer, words in diffrence.items():
            print("\t", pointer, end=" ")
            print(*words, sep=" ")
