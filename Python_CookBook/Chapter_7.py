## Functions

# Writing Functions That Only Accept Keyword Arguments
def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

minimum(1, 5, 2, -5, 10) # Returns -5
minimum(1, 5, 2, -5, 10, clip=0) # Returns 0


# Making an N-Argument Callable Work As a Callable with Fewer Arguments
'''
You have a callable that you would like to use with some other Python code,
possibly as a callback function or handler, but it takes too many arguments
and causes an exception when called.
'''
def spam(a, b, c, d):
    print(a, b, c, d)

>>> from functools import partial
>>> s1 = partial(spam, 1)
>>> s1(2, 3, 4)
1 2 3 4
>>> s1(4, 5, 6)
# a = 1
1 4 5 6
>>> s2 = partial(spam, d=42)
>>> s2(1, 2, 3)
1 2 3 42
>>> s2(4, 5, 5)
4 5 5 42
>>> s3 = partial(spam, 1, 2, d=42) # a = 1, b = 2, d = 42 >>> s3(3)
1 2 3 42
>>> s3(4)
1 2 4 42
>>> s3(5)
1 2 5 42

# Another example
points = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

# Now I want to sort the points based on distance from one point (4, 3)
pt = (4, 3)
points.sort(key=partial(distance, pt))
# [(3, 4), (1, 2), (5, 6), (7, 8)]


# Replacing Single Method Classes with Functions
'''
You have a class that only defines a single method besides __init__().
However, to simplify your code, you would much rather just have a simple function.
'''
from urllib.request import urlopen
class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# Example use. Download stock data from yahoo
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

''' Replace the above with the below '''
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener
# Example use
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))



# Inlining Callback Functions
'''
You’re writing code that uses callback functions, but you’re concerned about the
proliferation of small functions and mind boggling control flow. You would like
some way to make the code look more like a normal sequence of procedural steps.
'''

def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)
    # Invoke the callback with the result
    callback(result)

from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def inlined_async(func):
        @wraps(func)
        def wrapper(*args): f = func(*args)
            result_queue = Queue() result_queue.put(None)
            while True:
                result = result_queue.get()
                try:
                    a = f.send(result)
                    apply_async(a.func, a.args, callback=result_queue.put)
                except StopIteration:
                    break
        return wrapper

def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')
'''
5
helloworld
0
2
4
6
8
10
12
14
16
18
Goodbye
'''

# Accessing Variables Defined Inside a Closure
'''
You would like to extend a closure with functions that
allow the inner variables to be accessed and modified.
'''
def sample():
    n=0
    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func

f = sample()
f() # n= 0
f.set_n(10)
f() # n= 10
f.get_n() # 10
