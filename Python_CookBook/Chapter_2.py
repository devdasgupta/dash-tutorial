# Strings and Text
## Matching Strings Using Shell Wildcard Patterns
from fnmatch import fnmatch, fnmatchcase
fnmatch('foo.txt', '*.txt') # True
fnmatch('foo.txt', '?oo.txt') # True
fnmatch('Dat45.csv', 'Dat[0-9]*') # True
names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
[name for name in names if fnmatch(name, 'Dat*.csv')] # ['Dat1.csv', 'Dat2.csv']


## Sanitizing the text
import unicodedata
import sys

s = 'pýtĥöñ\fis\tawesome\r\n'
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None
}

s.translate(remap)

b = unicodedata.normalize('NFD', a)
# 'pýtĥöñ is awesome\n'
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
b.translate(cmb_chrs)
# 'python is awesome\n'
