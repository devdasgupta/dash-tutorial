## Files and I/O

# Iterating Over Fixed-Sized Records
'''
Instead of iterating over a file by lines, you want to
iterate over a collection of fixed- sized records or chunks.
'''
from functools import partial

RECORD_SIZE = 32

with open('somefile.data', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        ...


# Manipulating Pathnames
>>> import os
>>> path = '/Users/beazley/Data/data.csv'

>>> # Get the last component of the path
>>> os.path.basename(path)
'data.csv'

>>> # Get the directory name
>>> os.path.dirname(path)
'/Users/beazley/Data'

>>> # Join path components together
>>> os.path.join('tmp', 'data', os.path.basename(path))
'tmp/data/data.csv'

>>> # Expand the user's home directory
>>> path = '~/Data/data.csv'
>>> os.path.expanduser(path)
'/Users/beazley/Data/data.csv'

>>> # Split the file extension
>>> os.path.splitext(path)
('~/Data/data', '.csv')
>>>


# Making Temporary Files and Directories
from tempfile import TemporaryFile
with TemporaryFile('w+t') as f:
    # Read/write to the file
    f.write('Hello World\n')
    f.write('Testing\n')

    # Seek back to beginning and read the data
    f.seek(0)
    data = f.read()
# Temporary file is destroyed

'''
On most Unix systems, the file created by TemporaryFile() is unnamed and
won’t even have a directory entry. If you want to relax this constraint,
use NamedTemporary File() instead. For example:
'''
from tempfile import NamedTemporaryFile
with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)
    ...
# File automatically destroyed

'''
To make a temporary directory, use tempfile.TemporaryDirectory(). For example:
'''
from tempfile import TemporaryDirectory
with TemporaryDirectory() as dirname:
    print('dirname is:', dirname) # Use the directory
    ...
# Directory and all contents destroyed
