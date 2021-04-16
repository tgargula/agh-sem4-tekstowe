import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

if __name__ == '__main__':

    data = ([], [], [])

    for filename in sorted(os.listdir("data")):

        original = os.path.getsize(f"data/{filename}")

        encoded = ''.join(filename.split('.')[:-1] + [".bin"])

        static = os.path.getsize(f"encoded/StaticHuffmanTree/{encoded}")

        dynamic = os.path.getsize(f"encoded/DynamicHuffmanTree/{encoded}")

        data[0].append(filename)
        data[1].append(static / original * 100)
        data[2].append(dynamic / original * 100)

    x = np.arange(len(data[0]))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, data[1], width, label='static')
    rects2 = ax.bar(x + width / 2, data[2], width, label='dynamic')
    ax.set_title('Static and dynamic huffman encoding comparison')
    ax.set_ylabel('Compression ratio')
    ax.set_xticks(x)
    ax.set_xticklabels(data[0], rotation="vertical", fontsize="x-small")
    ax.legend()

    for rect, label in zip(rects1, data[1]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                height, round(label,1), ha='center', va='bottom', fontsize="x-small")
    
    for rect, label in zip(rects2, data[2]):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                height, round(label,1), ha='center', va='bottom', fontsize="x-small")

    fig.tight_layout()

    plt.show()
