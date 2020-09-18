## Data Structure and Algorithms
# Keeping the Last N Items
from collections import deque

def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)
    # Example use on a file

if __name__ == '__main__':
    with open('somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline, end='')
                print(line, end='')
                print('-'*20)


## Finding the Largest or Smallest N Items
import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2

portfolio = [
                {'name': 'IBM', 'shares': 100, 'price': 91.1},
                {'name': 'AAPL', 'shares': 50, 'price': 543.22},
                {'name': 'FB', 'shares': 200, 'price': 21.09},
                {'name': 'HPQ', 'shares': 35, 'price': 31.75},
                {'name': 'YHOO', 'shares': 45, 'price': 16.35},
                {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])

# Note: heap[0] always stores the minimum from a heap. So heapq.heappop(iter) will always return minimum value


## Mapping Keys to Multiple Values in a Dictionary
from collections import defaultdict
'''
d={
    'a' : [1, 2, 3],
    'b' : [4, 5]
}
e={
    'a' : {1, 2, 3},
    'b' : {4, 5}
}
'''
d = defaultdict(list)
d['a'].append(1)
d['a'].append(2) d['b'].append(4)

e = defaultdict(set)
e['a'].add(1)
e['a'].add(2)
e['b'].add(4)


# Ordered Dictionary
from collections import OrderedDict
d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
# Outputs "foo 1", "bar 2", "spam 3", "grok 4"
for key in d:
    (key, d[key]


# Finding Commonalities in Two Dictionaries
a={
'x' : 1,
'y' : 2,
'z' : 3
}

b={
'w' : 10,
'x' : 11,
'y' : 2
}

# Find keys in common
a.keys() & b.keys() # { 'x', 'y' }
# Find keys in a that are not in b
a.keys() - b.keys() # { 'z' }
# Find (key,value) pairs in common
a.items() & b.items() # { ('y', 2) }


## Removing Duplicates from a Sequence while Maintaining Order
def dedupe_hasable(items):
    seen = set()
    for item in items:
            if item not in seen:
                yield item
                seen.add(item)

a = [1, 5, 2, 1, 9, 1, 5, 10]
list(dedupe_hasable(a)) # [1, 5, 2, 9, 10]

def dedupe_dict(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)

a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
list(dedupe(a, key=lambda d: (d['x'],d['y']))) # [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
list(dedupe(a, key=lambda d: d['x'])) # [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]

# Determining the Most Frequently Occurring Items in a Sequence
words = [
'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the', 'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into', 'my', 'eyes', "you're", 'under'
]
from collections import Counter

word_counts = Counter(words)
top_three = word_counts.most_common(3)
print(top_three) # Outputs [('eyes', 8), ('the', 5), ('look', 4)]


## Sorting a List of Dictionaries by a Common Key
rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

from operator import itemgetter
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print(rows_by_fname)
# [
#     {'fname': 'Big', 'uid': 1004, 'lname': 'Jones'},
#     {'fname': 'Brian', 'uid': 1003, 'lname': 'Jones'},
#     {'fname': 'David', 'uid': 1002, 'lname': 'Beazley'},
#     {'fname': 'John', 'uid': 1001, 'lname': 'Cleese'}
# ]

print(rows_by_uid)
# [
#     {'fname': 'John', 'uid': 1001, 'lname': 'Cleese'},
#     {'fname': 'David', 'uid': 1002, 'lname': 'Beazley'},
#     {'fname': 'Brian', 'uid': 1003, 'lname': 'Jones'},
#     {'fname': 'Big', 'uid': 1004, 'lname': 'Jones'}
# ]

## Grouping Records Together Based on a Field
rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]
from operator import itemgetter
from itertools import groupby

# Sort by the desired field first
rows.sort(key=itemgetter('date'))
# Iterate in groups
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)

'''
    07/01/2012
        {'date': '07/01/2012', 'address': '5412 N CLARK'}
        {'date': '07/01/2012', 'address': '4801 N BROADWAY'}
    07/02/2012
        {'date': '07/02/2012', 'address': '5800 E 58TH'}
        {'date': '07/02/2012', 'address': '5645 N RAVENSWOOD'}
        {'date': '07/02/2012', 'address': '1060 W ADDISON'}
    07/03/2012
        {'date': '07/03/2012', 'address': '2122 N CLARK'}
    07/04/2012
        {'date': '07/04/2012', 'address': '5148 N CLARK'}
        {'date': '07/04/2012', 'address': '1039 W GRANVILLE'}
'''

## Use of compress while filtering Sequence Elements
addresses = [
    '5412 N CLARK',
    '5148 N CLARK', '5800 E 58TH',
    '2122 N CLARK'
    '5645 N RAVENSWOOD', '1060 W ADDISON', '4801 N BROADWAY', '1039 W GRANVILLE',
]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]
from itertools import compress
more5 = [n > 5 for n in counts] # [False, False, True, False, False, True, True, False]
list(compress(addresses, more5)) # ['5800 E 58TH', '4801 N BROADWAY', '1039 W GRANVILLE']

## Dictionary Comprehension
prices = {
'ACME': 45.23, 'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.20, 'FB': 10.75
}
# Make a dictionary of all prices over 200
p1 = { key:value for key, value in prices.items() if value > 200 }

# Make a dictionary of tech stocks
tech_names = { 'AAPL', 'IBM', 'HPQ', 'MSFT' }
p2 = { key:value for key,value in prices.items() if key in tech_names }
