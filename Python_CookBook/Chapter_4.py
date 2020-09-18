'''
    Chapter 4: Iterators and Generators
'''
# Manually Consuming an Iterator
with open('/etc/passwd') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass

# Usage
import psycopg2
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
cur = conn.cursor()
with open('user_accounts.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'users', sep=',')

conn.commit()

# Creating New Iteration Patterns with Generators
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

list(frange(0, 1, 0.125))

# Implementing the Iterator Protocol
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))
    for ch in root.depth_first():
        print(ch)
        # Outputs Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)


# Iterating in Reverse
a = [1, 2, 3, 4]
for x in reversed(a):
    print(x) # 4 3 2 1


# Taking a Slice of an Iterator
def count(n):
    while True:
        yield n
        n += 1

c = count(0)
'''
This throws TypeError
c[10:12]
'''
from itertools import islice
for x in islice(c, 10, 12):
    print(x) # 10, 11

# This works of we know how may items to skip
items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):
    print(x) # 1, 4, 10, 15

# Skipping the First Part of an Iterable
from itertools import dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')

# Iterating Over the Index-Value Pairs of a Sequence
'''
map words in a file to the lines in which they occur,
'''
word_summary = defaultdict(list)
with open('myfile.txt', 'r') as f:
    lines = f.readlines()
for idx, line in enumerate(lines):
    # Create a list of words in current line
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)

# Iterating Over Multiple Sequences Simultaneously
from itertools import zip_longest

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']

for i in zip(a,b):
    print(i)
'''
(1, 'w')
(2, 'x')
(3, 'y')
'''

for i in zip_longest(a,b):
    print(i)
'''
(1, 'w')
(2, 'x')
(3, 'y')
(None, 'z')
'''

for i in zip_longest(a, b, fillvalue=0):
    print(i)
'''
(1, 'w')
(2, 'x')
(3, 'y')
(0, 'z')
'''

# Iterating on Items in Separate Containers
from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)
'''
1
2
3
4
x
y
z
'''

# Creating Data Processing Pipelines
'''
You want to process data iteratively in the style of a data processing pipeline
(similar to Unix pipes). For instance, you have a huge amount of data that
needs to be processed, but it can’t fit entirely into memory.
'''
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)


# Flattening a Nested Sequence
from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]

for x in flatten(items):
    print(x) # Produces 1 2 3 4 5 6 7 8

# Iterating in Sorted Order Over Merged Sorted Iterables
import heapq
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]

for c in heapq.merge(a, b):
    print(c)
'''
1
2
4
5
6
7
10
11
'''
# Usage
import heapq
with open('sorted_file_1', 'rt') as file1, \
    open('sorted_file_2') 'rt' as file2, \
    open('merged_file', 'wt') as outf:
    for line in heapq.merge(file1, file2):
        outf.write(line)
