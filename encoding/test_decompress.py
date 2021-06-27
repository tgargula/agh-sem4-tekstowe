import pytest
from os import listdir
from bitarray import bitarray

from huffman.huffman import StaticHuffmanTree, DynamicHuffmanTree


def test_decompress():
    for filename in listdir("data"):
        encodedfile = ''.join(filename.split('.')[:-1] + [".bin"])
        with open(f"data/{filename}", "r") as f:
            text = f.read()

        for HuffmanTree in (StaticHuffmanTree, DynamicHuffmanTree,):

            with open(f"encoded/{HuffmanTree.__name__}/{encodedfile}", "rb") as f:
                array = bitarray()
                array.fromfile(f)
                decoded = HuffmanTree().decode(array)

            assert text == decoded

if __name__ == '__main__':
    test_decompress()
