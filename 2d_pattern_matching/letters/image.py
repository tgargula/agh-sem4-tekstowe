import cv2
import matplotlib.pyplot as plt

HAYSTACK = {
    "n": lambda image, id: Image.segment(image, (37, 40), (47, 49), id),
    "e": lambda image, id: Image.segment(image, (37, 51), (47, 60), id),
    "o": lambda image, id: Image.segment(image, (37, 68), (47, 77), id),
    "pattern": lambda image, id: Image.segment(image, (474, 184), (491, 283), id),
}


class Image:
    def __init__(self, image, id=None):
        self.image = image
        self.id = id

    @classmethod
    def segment(cls, image, upperleft, lowerright, id):
        s, t = upperleft
        u, w = lowerright
        return cls(image[s:u, t:w], id)

    @classmethod
    def from_file(cls, filename):
        return cls(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    def show(self):
        plt.imshow(255 - self.image, cmap="Greys")
        plt.show()


class Haystack:
    def __init__(self):
        self.haystack = Image.from_file("haystack.png")
        self.image = self.haystack.image

    def get(self, pattern):
        if pattern not in HAYSTACK:
            raise TypeError("Pattern not recognised!")
        return HAYSTACK[pattern](self.haystack.image, pattern)