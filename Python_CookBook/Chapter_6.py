'''
Data Encoding and Processing
'''

# Reading and Writing CSV Data
import csv
from collections import namedtuple

with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        # Process row

# Another alternative is to read the data as a sequence of dictionaries instead.
# To do that, use this code:
import csv
with open('stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        # process row

# Write to csv
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
        ]
with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

# If sequence as a Dictionary
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [
        {'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
        {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
        ]
with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)

# Read from a JSON files
'''
Normally, JSON decoding will create dicts or lists from the supplied data.
If you want to create different kinds of objects, supply the object_pairs_hook
or object_hook to json.loads(). For example, here is how you would decode
JSON data, preserving its order in an OrderedDict:
'''
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
>>> data
# OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])

# How you could turn a JSON dictionary into a Python object:
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

data = json.loads(s, object_pairs_hook=OrderedDict)
>>> data.name
# 'ACME'
>>> data.shares
# 50
>>> data.price
# 490.1


# Parsing Simple XML Data
from urllib.request import urlopen
from xml.etree.ElementTree import parse

# Download the RSS feed and parse it
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)
# Extract and output tags of interest
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()


# Parsing Huge XML Files Incrementally
'''
Use iterators/generators to parse huge file with minimum memory footprint
'''
from xml.etree.ElementTree import iterparse
def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))

    # Skip the root element
    next(doc)
    tag_stack = []
    elem_stack = []

    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass

'''
Usage: Suppose you want to write a script that ranks ZIP codes by the number
of pothole reports. To do it, you could write code like this:
'''
from collections import Counter

potholes_by_zip = Counter()
data = parse_and_remove('potholes.xml', 'row/row')
for pothole in data:
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)
