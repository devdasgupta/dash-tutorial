## Classes and Objects

# Changing the String Representation of Instances
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)

>>> p = Pair(3, 4)
>>> p
Pair(3, 4) # __repr__() output
>>> print(p)
(3, 4) # __str__() output

'''
The use of format() in the solution might look a little funny, but the format
code {0.x} specifies the x-attribute of argument 0. So, in the following
function, the 0 is actually the instance self:
'''
def __repr__(self):
    return 'Pair({0.x!r}, {0.y!r})'.format(self)
'''
As an alternative to this implementation, you could also use
the % operator and the following code:
'''
def __repr__(self):
    return 'Pair(%r, %r)' % (self.x, self.y)

# Customizing String Formatting
'''
You want an object to support customized formatting through the
format() function and string method.
'''
_formats = {
            'ymd' : '{d.year}-{d.month}-{d.day}',
            'mdy' : '{d.month}/{d.day}/{d.year}',
            'dmy' : '{d.day}/{d.month}/{d.year}'
            }
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

>>> d = Date(2012, 12, 21)
>>> format(d)
'2012-12-21'
>>> format(d, 'mdy')
'12/21/2012'
>>> 'The date is {:ymd}'.format(d)
'The date is 2012-12-21'
>>> 'The date is {:mdy}'.format(d)
'The date is 12/21/2012'

# Making Objects Support the Context-Management Protocol
'''
You want to make your objects support the context-management protocol (the with statement).
Solution: In order to make an object compatible with the with statement,
you need to implement __enter__() and __exit__() methods.
'''
from socket import socket, AF_INET, SOCK_STREAM
class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

def __enter__(self):
    if self.sock is not None:
        raise RuntimeError('Already connected')
    self.sock = socket(self.family, self.type)
    self.sock.connect(self.address)
    return self.sock

def __exit__(self, exc_ty, exc_val, tb):
    self.sock.close()
    self.sock = None

#Usage
from functools import partial
conn = LazyConnection(('www.python.org', 80)) # Connection closed
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b'')) # conn.__exit__() executes: connection closed


# Creating Managed Attributes
'''
You want to add extra processing (e.g., type checking or validation)
to the getting or setting of an instance attribute.
@getter and @setter functions using property
'''
# Example 1
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

# Example 2
class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)

    # Getter function
    def get_first_name(self):
        return self._first_name

    # Setter function
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

    # Make a property from existing get/set methods
    name = property(get_first_name, set_first_name, del_first_name)


# Extending a Property in a Subclass
'''
Within a subclass, you want to extend the functionality
of a property defined in a parent class.
'''
class Person:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")

class SubPerson(Person): @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)


# Creating a New Kind of Class or Instance Attribute
'''
You want to create a new kind of instance attribute type
with some extra functionality, such as type checking.
'''
# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]



# Using Lazily Computed Properties
'''
You’d like to define a read-only attribute as a property that only gets
computed on access. However, once accessed, you’d like the value to be
cached and not recomputed on each access.
'''
class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

#Utilize the code
import math
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

#Outputs
>>> c = Circle(4.0)
>>> c.radius
4.0
>>> c.area
Computing area
50.26548245743669
>>> c.area
50.26548245743669
>>> c.perimeter
Computing perimeter
25.132741228718345
>>> c.perimeter
25.132741228718345



# Simplifying the Initialization of Data Structures
'''
You are writing a lot of classes that serve as data structures, but you are
getting tired of writing highly repetitive and boilerplate __init__() functions.
'''
class Structure:
    # Class variable that specifies expected fields
    _fields= []

    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

# Example class definitions
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    class Point(Structure):
        _fields = ['x','y']

    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2



# Defining an Interface or Abstract Base Class
'''
You want to define a class that serves as an interface or abstract base class
from which you can perform type checking and ensure that certain methods
are implemented in subclasses.
'''
from abc import ABCMeta, abstractmethod
class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass

class SocketStream(IStream):
    def read(self, maxbytes=-1):
        ...

    def write(self, data):
        ...

    def serialize(obj, stream):
        if not isinstance(stream, IStream):
            raise TypeError('Expected an IStream')
        ...


# Implementing a Data Model or Type System
'''
You want to define various kinds of data structures, but want to enforce constraints
on the values that are allowed to be assigned to certain attributes.
'''
# Base class. Uses a descriptor to set a value
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

# Descriptor for enforcing types
class Typed(Descriptor):
    expected_type = type(None)
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('expected ' + str(self.expected_type))
        super().__set__(instance, value)

# Descriptor for enforcing values
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance, value)

class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
            super().__set__(instance, value)


# Usage of the above Classes to create Type
class Integer(Typed):
    expected_type = int

class UnsignedInteger(Integer, Unsigned):
    pass

class Float(Typed):
    expected_type = float

class UnsignedFloat(Float, Unsigned):
    pass

class String(Typed):
    expected_type = str

class SizedString(String, MaxSized):
    pass

'''
Using these type objects, it is now possible to define a class such as this:
'''
class Stock:
    # Specify constraints
    name = SizedString('name',size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, shares, price):
        self.name = name self.shares = shares self.price = price

# Another way to use these type Objects
# Class decorator to apply constraints is using decorators
def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate

# Example
@check_attributes(name=SizedString(size=8), shares=UnsignedInteger,price=UnsignedFloat)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price



# Defining More Than One Constructor in a Class
'''
You’re writing a class, but you want users to be able to create instances in
more than the one way provided by __init__().
'''
import time
class Date:
    # Primary constructor
    def __init__(self, year, month, day):
        self.year = year self.month = month self.day = day

    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

# Usage
a = Date(2012, 12, 21) # Primary
b = Date.today() # Alternate
