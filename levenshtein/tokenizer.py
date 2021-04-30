from sys import argv
from lcs import lcs, tokenize_from_file, decompose, punch


if __name__ == "__main__":
    file = argv[1] if len(argv) > 1 else "data/romeo-i-julia-700.txt"
    n = argv[2] if len(argv) > 2 else 2

    dir = "/".join(file.split("/")[:-1])

    for i in range(n):
        tokens = tokenize_from_file(file)
        punched = punch(tokens)
        print(1 - len(punched) / len(tokens))

        outfile = f"{dir}/out{i + 1}.txt"
        with open(outfile, "w") as f:
            for token in punched:
                f.write(token.text_with_ws)
