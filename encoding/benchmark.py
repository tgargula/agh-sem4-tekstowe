from os import listdir
from timeit import default_timer as timer
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

from huffman.huffman import DynamicHuffmanTree, StaticHuffmanTree


def benchmark(f, *args):
    start = timer()
    result = f(*args)
    return timer() - start, result


if __name__ == '__main__':

    data = ([], [], [])

    for filename in sorted(listdir("data")):
        
        data[0].append(filename)

        for i, HuffmanTree in enumerate((StaticHuffmanTree, DynamicHuffmanTree)):
            file = filename

            with open(f"data/{file}", "r") as f:
                elapsed, HT = benchmark(HuffmanTree, f.read())


            data[i+1].append(elapsed)

            file = ''.join(file.split('.')[:-1] + [".bin"])

            # since we have built the tree, we can save it to file
            with open(f"encoded/{HuffmanTree.__name__}/{file}", "wb") as f:
                f.write(HT.get_encoded())
    
    
    width = 0.35

    independent = data[0][:-3], data[1][:-3], data[2][:-3]
    dependent = data[0][-3:], data[1][-3:], data[2][-3:]

    x = np.arange(len(independent[0]))

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, independent[1], width, label='static')
    rects2 = ax.bar(x + width / 2, independent[2], width, label='dynamic')
    ax.set_title('Static and dynamic huffman encoding comparison')
    ax.set_ylabel('Time [s]')
    ax.set_xticks(x)
    ax.set_yscale('log')
    ax.set_xticklabels(independent[0], rotation="vertical", fontsize="x-small")
    ax.legend()

    for rect, label in zip(rects1, independent[1]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                height, round(label,3), ha='center', va='bottom', fontsize="x-small")
    
    for rect, label in zip(rects2, independent[2]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                height, round(label,3), ha='center', va='bottom', fontsize="x-small")

    fig.tight_layout()

    plt.show()

    x = np.arange(len(dependent[0]))

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, dependent[1], width, label='static')
    rects2 = ax.bar(x + width / 2, dependent[2], width, label='dynamic')
    ax.set_title('Static and dynamic huffman encoding comparison')
    ax.set_ylabel('Time [s]')
    ax.set_xticks(x)
    ax.set_yscale('log')
    ax.set_xticklabels(dependent[0], rotation="vertical", fontsize="x-small")
    ax.legend()

    for rect, label in zip(rects1, dependent[1]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                height, round(label,3), ha='center', va='bottom', fontsize="x-small")
    
    for rect, label in zip(rects2, dependent[2]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                height, round(label,3), ha='center', va='bottom', fontsize="x-small")

    fig.tight_layout()

    plt.show()