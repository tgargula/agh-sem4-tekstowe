from lcs import diff
from lcs.diff import diff_

if __name__ == '__main__':

    line1 = ['there', 'general', 'Kenobi', 'world']
    line2 = ['Hello', 'there', 'general', 'Kenobi']
    print(diff_(line1, line2))
    print(diff('data/data1.txt', 'data/data2.txt'))
