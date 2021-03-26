import pydot


def common_suffix_size(A, B):
    ctr = 0
    for i, letter in enumerate(A):
        if letter == B[i]:
            ctr += 1
        else:
            return ctr
    return ctr


class SuffixTreeNode:
    def __init__(self, start=None, end=None, parent=None):
        self.start = start
        self.end = end
        self.parent = parent
        self.children = []

    def length(self):
        return self.end - self.start + 1

    def slice(self):
        return (self.start, self.end)

    def subtext(self, text):
        return text[self.start:self.end+1]

    def _save(self, G, parent, text):
        node = pydot.Node(str(self), shape="point")
        G.add_node(node)
        label = str(self.subtext(text) if self.children or
                    self.start == self.end else self.slice())
        edge = pydot.Edge(parent, node, label=label)
        G.add_edge(edge)

        for child in self.children:
            child._save(G, node, text)

    def _add(self, text, i):
        for child in self.children:
            if text[child.start] == text[i]:
                A = text[i:i + child.length()]
                B = text[child.start:child.start + len(A)]
                if A == B:
                    child._add(text, i + child.length())
                    return
                size = common_suffix_size(A, B)
                subnode = SuffixTreeNode(child.start + size, child.end, parent=child)
                child.end = child.start + size - 1
                subnode.children = child.children
                leaf = SuffixTreeNode(i + size, len(text) - 1, parent=child)
                child.children = [subnode, leaf]
                return
        leaf = SuffixTreeNode(start=i, end=len(text) - 1, parent=self)
        self.children.append(leaf)


class SuffixTree:
    def __init__(self, text):
        self.root = SuffixTreeNode()
        self.text = text
        for i in range(len(text)):
            self.root._add(text, i)

    def save(self, filename):
        G = pydot.Dot(graph_type="graph", label=f"SuffixTree: {self.text}", labelloc='top')

        root = pydot.Node(str(None), shape="point")
        G.add_node(root)

        for child in self.root.children:
            child._save(G, root, self.text)

        G.write_png(filename)


class TrieNode:
    def __init__(self, letter=None, parent=None):
        self.letter = letter
        self.parent = parent
        self.children = {}

    def _save(self, graph, parent=None, prefix=""):
        word = prefix + self.letter
        node = pydot.Node(word, label=self.letter, shape="point")
        graph.add_node(node)

        if parent is not None:
            graph.add_edge(pydot.Edge(parent, node, label=self.letter))

        for child in self.children.values():
            child._save(graph, node, word)


class Trie:
    def __init__(self, text):
        self.root = TrieNode()
        self.text = text
        self._add(text)

    def _add(self, text):
        n = len(text)
        for i in range(n):
            pointer = self.root
            for j in range(i, n):
                letter = text[j]
                if letter not in pointer.children:
                    pointer.children[letter] = TrieNode(letter, pointer)
                pointer = pointer.children[letter]

    def save(self, filename):
        graph = pydot.Dot(graph_type="digraph", label=f"Trie: {self.text}", labelloc='top')

        root = pydot.Node("root", shape="point")
        graph.add_node(root)
        for child in self.root.children.values():
            child._save(graph, root)

        graph.write_png(filename)


if __name__ == '__main__':

    T = SuffixTree('aabbabd')
    T.save('out.png')