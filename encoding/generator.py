import string
import sys
import random
from optparse import OptionParser
        

Sigma = list(string.ascii_letters) + ['\n', ' ']

def generate_file(length, filename):
    text = ''.join([random.choice(Sigma) for _ in range(length)])
    with open(filename, "w") as f:
        f.write(text)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", type="int", dest="num", help="specify text length", default=1000)
    parser.add_option("-f", "--file", dest="filename", metavar="FILE", default="out.txt")
    options, args = parser.parse_args()
    
    generate_file(options.num, options.filename)