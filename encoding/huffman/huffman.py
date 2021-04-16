import pydot

from collections import deque
from bitarray import bitarray

BITS_PER_LETTER = 8


def extract_min(leafs, nodes):
    if not leafs:
        return nodes.pop()
    if not nodes:
        return leafs.pop()
    return nodes.pop() if nodes[-1].weight < leafs[-1].weight else leafs.pop()


def count_letters(text):
    dictionary = {}
    for letter in text:
        dictionary[letter] = dictionary.get(letter, 0) + 1
    return dictionary


def utf8(letter):
    return bin(ord(letter))[2:].zfill(BITS_PER_LETTER)


class Node:
    def __init__(self, weight, left=None, right=None):
        self.left = left
        self.right = right
        self.weight = weight
        self.parent = None
        self.visited = False
        if left:
            left.parent = self
        if right:
            right.parent = self

    def postorder(self):
        return self.left.postorder() + self.right.postorder() + [self]

    def _save(self, G, parent=None, i=None):
        node = pydot.Node(str(self), label=str(self.weight), shape="circle")

        G.add_node(node)
        if parent:
            edge = pydot.Edge(parent, node, label=str(i))
            G.add_edge(edge)
        for i, child in enumerate((self.left, self.right)):
            child._save(G, node, i)


class Leaf(Node):
    def __init__(self, weight, letter):
        super().__init__(weight)
        self.letter = letter

    def postorder(self):
        return [self]

    def code(self):
        pointer = self
        code = []
        while pointer.parent is not None:
            parent = pointer.parent
            if parent.left == pointer:
                code.append("0")
            if parent.right == pointer:
                code.append("1")
            pointer = parent
        return ''.join(reversed(code))

    def _save(self, G, parent, i):
        node = pydot.Node(
            str(self), label=f'{self.letter}: {self.weight}', shape="square")
        G.add_node(node)
        edge = pydot.Edge(parent, node, label=str(i))
        G.add_edge(edge)


class HuffmanTree:
    def __init__(self, root):
        self.root = root
        self.codes, self.letters = self._get_encodings()

    def encode(self, text):
        return ''.join([self.codes[letter] for letter in text])

    def decode(self, code, size=None):
        i, j = 0, 1
        result = []
        while i < len(code) and (size is None or len(result) < size):
            while code[i:j] not in self.letters:
                j += 1
            result += self.letters[code[i:j]]
            i = j
        return ''.join(result)

    def save(self, filename='out.png'):
        G = pydot.Dot(graph_type="graph")
        self.root._save(G)
        G.write_png(filename)

    def _get_encodings(self):
        codes, letters = {}, {}
        pointer = self.root
        code = []
        while pointer:
            if pointer.left is None or pointer is None:
                encoded = ''.join(code)
                codes[pointer.letter] = encoded
                letters[encoded] = pointer.letter
                pointer.visited = True
                code.pop()
                pointer = pointer.parent
            else:
                if not pointer.left.visited:
                    code.append('0')
                    pointer = pointer.left
                elif not pointer.right.visited:
                    code.append('1')
                    pointer = pointer.right
                else:
                    pointer.visited = True
                    code = code[:-1]
                    pointer = pointer.parent
        return codes, letters


class StaticHuffmanTree(HuffmanTree):
    def __init__(self, text):
        super().__init__(self._build(count_letters(text)))

    def _build(self, dictionary):
        leafs = [Leaf(weight, letter) for letter, weight in
                 sorted([item for item in dictionary.items()], key=lambda item: -item[1])]
        nodes = deque()
        if len(leafs) == 1:
            nodes.append(leafs.pop())
        while len(leafs) + len(nodes) > 1:
            node1 = extract_min(leafs, nodes)
            node2 = extract_min(leafs, nodes)
            nodes.appendleft(Node(node1.weight + node2.weight, node1, node2))
        return nodes.pop()


class DynamicHuffmanTree(HuffmanTree):
    def __init__(self, stream=[]):
        self.root = Leaf(0, None)
        self.NYT = self.root
        self.pointers = {}
        self.encoded = bitarray()
        self.nodes = [self.NYT]
        self.root.index = 0
        for letter in stream:
            self.add(letter)

    def decode(self, binary):
        pointer = self.root
        decoded = []
        skipping = 0
        for i, bit in enumerate(binary):
            skipping = skipping - 1 if skipping > 0 else 0
            if not skipping:
                if isinstance(pointer, Leaf):
                    if pointer is self.NYT:
                        letter = chr(int(binary[i:i+BITS_PER_LETTER].to01(), 2))
                        print(binary[i:i+BITS_PER_LETTER])
                        skipping = BITS_PER_LETTER
                        self.add(letter)
                        decoded.append(letter)
                        pointer = self.root
                        continue
                    else:
                        decoded.append(pointer.letter)
                        print(pointer.letter)
                        self.add(pointer.letter)
                        pointer = self.root
                
                pointer = pointer.right if bit else pointer.left
        
        skipping = skipping - 1 if skipping > 0 else 0
        if not skipping:
            if isinstance(pointer, Leaf):
                if pointer is self.NYT:
                    letter = chr(int(binary[i:i+BITS_PER_LETTER].to01(), 2))
                    print(binary[i:i+BITS_PER_LETTER])
                    skipping = BITS_PER_LETTER
                    self.add(letter)
                    decoded.append(letter)
                    pointer = self.root
                else:
                    decoded.append(pointer.letter)
                    print(pointer.letter)
                    self.add(pointer.letter)
                    pointer = self.root
        
        return ''.join(decoded)
        
    def next(self, node):
        return self.nodes[node.index - 1] if node.index > 0 else None

    def add(self, letter):
        pointer = self.root
        if letter in self.pointers:  # has been transferred
            leaf = self.pointers[letter]
            self.encoded.extend(leaf.code())
            p = leaf
            next = self.next(p)
            while next is not None and p.weight == next.weight:
                self.swap(p, next)
                next = self.next(p)
            if p.parent.left is self.NYT:
                leaf = p
                p = p.parent
            else:
                leaf = None

        else:  # not yet transferred (NYT)
            self.encoded.extend(self.NYT.code() + utf8(letter))
            parent = self.NYT.parent
            self.nodes.pop()
            leaf = Leaf(0, letter)
            node = Node(0, self.NYT, leaf)
            self.nodes.append(node)
            node.index = len(self.nodes) - 1
            self.nodes.append(leaf)
            leaf.index = len(self.nodes) - 1
            self.nodes.append(self.NYT)
            self.NYT.index = len(self.nodes) - 1
            if self.NYT is self.root:
                self.root = node
            if parent is not None:
                parent.left = node
            node.parent = parent
            self.pointers[letter] = leaf
            p = node

        self._update(p, leaf)

    def swap(self, node1, node2):
        index1 = node1.index
        index2 = node2.index
        self.nodes[index1], self.nodes[index2] = self.nodes[index2], self.nodes[index1]
        node1.index, node2.index = node2.index, node1.index
        parent1 = node1.parent
        parent2 = node2.parent
        if parent1.left is node1 and parent2.left is node2:
            parent1.left, parent2.left = parent2.left, parent1.left
        elif parent1.left is node1:
            parent1.left, parent2.right = parent2.right, parent1.left
        elif parent2.left is node2:
            parent1.right, parent2.left = parent2.left, parent1.right
        else:
            parent1.right, parent2.right = parent2.right, parent1.right
        node1.parent = parent2
        node2.parent = parent1

    def _update(self, node, leaf):
        parent = node.parent
        while node is not None:

            next = self.next(node)
            while next is not None and isinstance(next, Leaf) and next.weight == node.weight + 1:
                self.swap(node, next)
                next = self.next(node)
            node.weight += 1
            node = parent
            if node is not None:
                parent = node.parent

        if leaf is not None:
            next = self.next(leaf)
            while next is not None and not isinstance(next, Leaf) and next.weight == leaf.weight:
                self.swap(leaf, next)
                next = self.next(leaf)
            leaf.weight += 1


if __name__ == '__main__':

    string = "avadakedavra"

    d = count_letters(string)
    HT = StaticHuffmanTree(string)
    HT.save()
    print(f'Encoded: {HT.encode(string)}')
    print(f'Decoded: {HT.decode(HT.encode(string))}')

    pointer = HT.root
    while not isinstance(pointer, Leaf):
        pointer = pointer.right

    print(pointer.letter)
    # print(pointer.code())

    DHT = DynamicHuffmanTree()

    for i, letter in enumerate(string):
        DHT.add(letter)
        print(DHT.encoded)
    DHT.save(f"DHT{i}.png")

    print(DynamicHuffmanTree().decode(DHT.encoded))

    # pointer = DHT.root.right.left.right.right
    # # while not isinstance(pointer, Leaf):
    # #     print(pointer.weight)
    # #     pointer = pointer.right

    # print(pointer.letter)
    # print(pointer.next().letter)

    # print(bitarray("01010") + bitarray("1111"))
