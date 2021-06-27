from lcs import diff

if __name__ == "__main__":

    d = diff("data/romeo-i-julia-700.txt", "data/out1.txt")

    for line, difference in d.items():
        print(f"{line} :")
        for pointer, words in difference.items():
            print("\t", pointer, end=" ")
            print(*words, sep=" ")
