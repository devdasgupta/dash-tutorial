'''
    Chapter 3: Number Dates and Times
'''
## Performing Accurate Decimal Calculations
from decimal import Decimal

a = Decimal('4.2')
b = Decimal('2.1')
a + b # Decimal('6.3')

# Another example
from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a / b) # 0.7647058823529411764705882353
with localcontext() as ctx:
    ctx.prec = 3
    print(a / b) # 0.765


## Performing Complex-Valued Math
a = complex(2, 4)
b = 3 - 5j
a # (2+4j)
b # (3-5j)

a.real # 2.0
a.imag # 4.0

## Calculating with Fraction
from fractions import Fraction

a = Fraction(5, 4)
b = Fraction(7, 16)
print(a + b) # 27/16

print(a * b) # 35/64

# Getting numerator/denominator >>> c = a * b
c.numerator # 35
c.denominator # 64

# Converting to a float
float(c) # 0.546875

# Limiting the denominator of a value
print(c.limit_denominator(8)) # 4/7

# Converting a float to a fraction
x = 3.75
y = Fraction(*x.as_integer_ratio())
y # Fraction(15, 4)


# Finding the Date Range for the Current Month
'''
You have some code that needs to loop over each date in the current
month, and want an efficient way to calculate that date range.
'''
from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
return (start_date, end_date)

# Usage

>>> a_day = timedelta(days=1)
>>> first_day, last_day = get_month_range()
>>> while first_day < last_day:
...     print(first_day)
...     first_day += a_day
...
'''
2012-08-01
2012-08-02
2012-08-03
2012-08-04
2012-08-05
2012-08-06
2012-08-07 
2012-08-08
2012-08-09
#... and so on...
'''
