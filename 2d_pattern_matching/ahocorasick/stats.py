class StatsInterface:

    def get_id(self, pattern):
        pass

class TextStats(StatsInterface):
    def __init__(self, patterns):
        letters = set()
        for pattern in patterns:
            for letter in pattern:
                letters.add(letter)
        
        letters = sorted(letters)
        self.indexes = {pattern: i+1 for i, pattern in enumerate(patterns)}
        self.letters = letters
        self.patterns = patterns

    def get_id(self, pattern):
        return self.indexes.get(pattern, 0)

    def get_patterns(self):
        return self.patterns

    def get_repr(self, id):
        return self.patterns[id]
        
        
class ImageStats(StatsInterface):
    def __init__(self, patterns):
        self.images = patterns
        self.letters = list(range(256))
        self.patterns = [pattern.image for pattern in patterns]
        self.lines = [tuple(line) for pattern in self.patterns for line in pattern]
        self.tuples = {}
        for i, line in enumerate(self.lines):
            self.tuples[line] = i+1
        self.indexes = {}
        for i, pattern in enumerate(self.patterns):
            t = tuple(self.tuples[tuple(line)] for line in pattern)
            self.indexes[t] = i+1
    
    def get_id(self, pattern):
        return self.tuples.get(pattern, (0,))
        
    def get_patterns(self):
        return [tuple(line) for pattern in self.patterns for line in pattern]
    
    def get_repr(self, t):
        return self.images[self.indexes[t]-1].id
    
    