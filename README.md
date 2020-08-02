# Python recordparser

Parse delimited text file into a class

## Synopsis

The idea is to use a typed class to describe a record from a delimited 
text file and only return records that conform to this description.

For example, given an input file like this:

```
$ cat test_data/items.csv
id_,name,price
1,foo,3.25
2,bar,.43
3,baz,4.01
```

We can create a class to describe a record with the following field names 
and types:

```
from typing import NamedTuple, TextIO


class Item(NamedTuple):
    id_: int
    name: str
    price: float
```

The `recordparser.parse` function returns a generator of records that 
will be of the type `Item`.
Various problems may cause this to fail which are currently raised
with exceptions, so use `try`/`catch`:

```
try:
    parser = recordparser.parse(fh=open('test_data/items.csv'),
                                cls=Item,
                                delimiter=',',
                                quiet=False)

    for rec in parser:
        print(rec)

except Exception as err:
    print(err)
```

Each row from the input file will be converted to an `Item` which is based 
on `NamedTuple` and so therefore will be an _immutable_ instance (which is a
Good Thing).

Fields/columns from the input file which are not named in the given class will be ignored.

You can use `Optional` to allow for fields/columns to be absent or present.

You can use `Union[str, float]` to parse, e.g., a field as either a string or a floating point number

## Author

Ken Youens-Clark <kyclark@gmail.com>
