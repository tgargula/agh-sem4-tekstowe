from queue import Queue
from .stats import TextStats, ImageStats
import pydot
import numpy as np


class Node:
    def __init__(self, letter=None):
        self.letter = letter
        self.children = {}
        self.fail = None
        self.output = None

    def next(self, letter):
        return self.children.get(letter, None)

    def save(self, G, parent):
        node = pydot.Node(str(self), shape="point")
        G.add_node(node)
        label = str(self.letter)
        edge = pydot.Edge(parent, node, label=label)
        G.add_edge(edge)
        if self.fail:
            fail = pydot.Edge(node, str(self.fail), label=f"-{self.letter}", color="gray")
            G.add_edge(fail)

        for child in self.children.values():
            child.save(G, node)


class Trie:
    def __init__(self, words):
        self._create_trie(words)

    def _create_trie(self, words):
        self.root = Node()
        for i, word in enumerate(words):
            self._add(word, i + 1)

    def _add(self, word, id=0):
        node = self.root
        for letter in word:
            if letter in node.children:
                node = node.children[letter]
                continue
            new = Node(letter)
            node.children[letter] = new
            node = new
        node.output = id


class Automaton(Trie):
    def __init__(self, stats):
        super().__init__(stats.get_patterns())
        self.stats = stats
        self._build_fail()

    def _build_fail(self):
        Q = Queue()
        root = self.root

        for letter in self.stats.letters:
            node = root.next(letter)
            if node is not None:
                node.fail = root
                Q.put(node)

        while not Q.empty():
            node = Q.get()
            for letter in self.stats.letters:
                next = self.next(node, letter)
                if next is not None:
                    Q.put(next)

                    fail = node.fail
                    while self.next(fail, letter) is None:
                        fail = fail.fail

                    next.fail = self.next(fail, letter)
    
    def next(self, node, letter):
        next = node.next(letter)
        if node == self.root:
            return next if next is not None else self.root
        return next

    def search(self, line):
        node = self.root
        output = np.zeros(shape=len(line), dtype='int')
        for i, letter in enumerate(line):
            while self.next(node, letter) is None:
                node = node.fail
            
            node = self.next(node, letter)
            if node.output is not None:
                output[i] = node.output
        
        return output


class TrieVisualiser:
    def __init__(self, trie):
        self.trie = trie

    def save(self, filename):
        G = pydot.Dot(graph_type="digraph", label="Trie", labelloc="top")

        root = pydot.Node(str(self.trie.root), shape="point")
        G.add_node(root)

        for child in self.trie.root.children.values():
            child.save(G, root)

        G.write_png(filename)


class Automaton2d(Automaton):
    def __init__(self, stats):
        super().__init__(stats)
    
    @classmethod
    def text(cls, patterns):
        stats = TextStats(patterns)
        return cls(stats)
    
    @classmethod
    def images(cls, patterns):
        stats = ImageStats(patterns)
        return cls(stats)
    
    def search2d(self, lines, patterns=None):
        if patterns is None:
            patterns = self.stats.indexes
        array = self.search_array(lines)
        lengths = {len(pattern)-1 for pattern in patterns}
        results = []
        for n in lengths:
            for i in range(n - 1, len(array)):
                # Note: zip has the length of the smallest of zipped elements!
                zipped = zip(*array[i-n : i+1])
                for j, z in enumerate(zipped):
                    if z in patterns:
                        results.append((i + 1, j + 1, z))
                    
        return results
    
    def search_array(self, lines):
        return [self.search(line) for line in lines]
    