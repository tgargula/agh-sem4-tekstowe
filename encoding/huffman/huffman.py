import pydot

from collections import deque
from bitarray import bitarray

BITS_PER_LETTER = 16
BITS_PER_SIZE = 64

def extract_min(leaves, nodes):
    if not leaves:
        return nodes.pop()
    if not nodes:
        return leaves.pop()
    return nodes.pop() if nodes[-1].weight < leaves[-1].weight else leaves.pop()


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
        if left: left.parent = self
        if right: right.parent = self

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


'''Decorator class for List that saves info about the index'''
class List:
    def __init__(self, *nodes):
        self.structure = []
        self.extend(*nodes)
    
    def __getitem__(self, index):
        return self.structure[index]
    
    def __setitem__(self, index, node):
        self.structure[index] = node
        node.index = index
    
    def append(self, node):
        self.structure.append(node)
        node.index = len(self.structure) - 1
    
    def extend(self, *nodes):
        for node in nodes:
            self.append(node)
    
    def pop(self):
        node = self.structure.pop()
        node.index = None


class HuffmanTree:
    def __init__(self, root):
        self.root = root
        self.codes, self.letters = self._get_encodings()

    def save(self, filename='out.png'):
        G = pydot.Dot(graph_type="graph")
        self.root._save(G)
        G.write_png(filename)

    def _get_encodings(self):
        codes, letters = {}, {}
        pointer = self.root
        code = []
        while pointer:
            if pointer.left is None:
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
    
    def decode_size(self, binary):
        return int(binary[:BITS_PER_SIZE].to01(), 2)


class StaticHuffmanTree(HuffmanTree):
    def __init__(self, text=None):
        if text is not None:
            super().__init__(self._build(count_letters(text)))
            self.encoded = self.encode(text).tobytes()
        else:
            self.root = None
        
    def get_encoded(self):
        return self.encoded

    def _build(self, dictionary):
        leaves = [Leaf(weight, letter) for letter, weight in
                 sorted([item for item in dictionary.items()], key=lambda item: -item[1])]
        nodes = deque()
        if len(leaves) == 1:
            nodes.append(leaves.pop())
        while len(leaves) + len(nodes) > 1:
            node1 = extract_min(leaves, nodes)
            node2 = extract_min(leaves, nodes)
            nodes.appendleft(Node(node1.weight + node2.weight, node1, node2))
        return nodes.pop()
    
    def _encode_tree(self):
        return bitarray(''.join(
            ['1' + utf8(node.letter) if isinstance(node, Leaf) else '0' for node in self.root.postorder()]
        ) + '0')
    
    def _encode_size(self, text):
        return bitarray(bin(len(text))[2:].zfill(BITS_PER_SIZE))

    def _encode_text(self, text):
        return bitarray(''.join([self.codes[letter] for letter in text]))

    def encode(self, text):
        return self._encode_size(text) + self._encode_tree() + self._encode_text(text)

    def decode_tree(self, binary):
        stack = []
        j = 0
        while j < len(binary):
            j += 1
            if binary[j-1]:
                stack.append(Leaf(None, chr(int(binary[j:j+BITS_PER_LETTER].to01(), 2))))
                j += BITS_PER_LETTER
            else:
                if len(stack) == 1:
                    self.root = stack.pop()
                    self.codes, self.letters = self._get_encodings()
                    return j
                node1, node2 = stack.pop(), stack.pop()
                stack.append(Node(None, node2, node1))

    def decode_text(self, binary, size):
        i, j = 0, 1
        result = []
        while i < len(binary) and (size is None or len(result) < size):
            while binary[i:j].to01() not in self.letters:
                j += 1
            result += self.letters[binary[i:j].to01()]
            i = j
        return ''.join(result)

    def decode(self, binary):
        size = self.decode_size(binary)
        text_begin = self.decode_tree(binary[BITS_PER_SIZE:])
        return self.decode_text(binary[BITS_PER_SIZE + text_begin:], size)


class DynamicHuffmanTree(HuffmanTree):
    def __init__(self, stream=[]):
        self.root = Leaf(0, None)
        self.NYT = self.root
        self.pointers = {}
        self.encoded = bitarray()
        self.nodes = List(self.NYT)
        for letter in stream:
            self.add(letter)
    
    def get_encoded(self):
        return bitarray(bin(self.root.weight)[2:].zfill(BITS_PER_SIZE)) + self.encoded

    def decode(self, binary):
        pointer = self.root
        decoded = []
        skipping = 0

        size = decode_size(binary)
        print(size)

        binary = binary[BITS_PER_SIZE:]

        for i, bit in enumerate(binary):
            skipping = skipping - 1 if skipping > 0 else 0
            if not size:
                break
            if not skipping:
                if isinstance(pointer, Leaf):
                    size -= 1
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
                    skipping = BITS_PER_LETTER
                    self.add(letter)
                    decoded.append(letter)
                    pointer = self.root
                else:
                    decoded.append(pointer.letter)
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
            while next is not None and not (isinstance(p, Leaf) ^ isinstance(next, Leaf)) and p.weight == next.weight:
                self._swap(p, next)
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
            self.nodes.extend(node, leaf, self.NYT)
            if self.NYT is self.root:
                self.root = node
            if parent is not None:
                parent.left = node
            node.parent = parent
            self.pointers[letter] = leaf
            p = node

        self._update(p, leaf)

    def _swap(self, node1, node2):
        index1 = node1.index
        index2 = node2.index
        self.nodes[index1], self.nodes[index2] = self.nodes[index2], self.nodes[index1]
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
                self._swap(node, next)
                next = self.next(node)
            node.weight += 1
            node = parent
            if node is not None:
                parent = node.parent

        if leaf is not None:
            next = self.next(leaf)
            while next is not None and not isinstance(next, Leaf) and next.weight == leaf.weight:
                self._swap(leaf, next)
                next = self.next(leaf)
            leaf.weight += 1


if __name__ == '__main__':

    string = "abracadabra"

    HT = StaticHuffmanTree(string)
    HT.save("static.png")
    array = bitarray()
    array.frombytes(HT.encoded)
    decoded = StaticHuffmanTree().decode(array)
    print(f'Encoded: {array}')
    print(f'Decoded: {decoded}')

    DHT = DynamicHuffmanTree()

    for i, letter in enumerate(string):
        DHT.add(letter)
        print(DHT.encoded)
        DHT.save(f"dynamic{i}.png")
