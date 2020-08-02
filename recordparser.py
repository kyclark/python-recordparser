"""
RecordParser

Parse a delimited text file into records of a given class
converting the types to those described by the class.

Author : Ken Youens-Clark <kyclark@gmail.com>
"""

import csv
import sys
import typing


# --------------------------------------------------
def parse(cls: type,
          fh: typing.TextIO,
          delimiter: str = ',',
          quiet: bool = False) -> typing.Iterable[typing.Any]:
    """Create a parser"""

    reader = csv.DictReader(fh, delimiter=delimiter)
    fields = cls._field_types
    req_flds = [
        name for name, typ in fields.items()
        if (typing.get_origin(typ) is None) or (
            type(None) not in typing.get_args(typ))
    ]
    opt_flds = [
        name for name, typ in fields.items()
        if type(None) in typing.get_args(typ)
    ]
    missing = [name for name in req_flds if name not in reader.fieldnames]

    if missing:
        print(missing)
        raise Exception(f'Missing field: {", ".join(missing)}')

    def warn(msg):
        """Print message to STDERR"""

        if not quiet:
            print(msg, file=sys.stderr)

    for row_num, row in enumerate(reader):
        rec = {}
        for fld_name, fld_type in fields.items():
            # Handle optional fields
            if fld_name not in row:
                rec[fld_name] = None
                continue

            # Try to convert raw values
            raw_val = row[fld_name]
            val = None

            # Handle Union types
            if typing.get_origin(fld_type) is typing.Union:
                for typ in typing.get_args(fld_type):
                    if typ is not None and val is None:
                        try:
                            val = typ(raw_val)
                        except:
                            pass
            # Simple types (?), worry about Generic?
            else:
                try:
                    val = fld_type(raw_val)
                except:
                    pass

            if val is None:
                warn(f'{row_num}: Cannot convert "{raw_val}" to "{fld_type}"')
                continue

            rec[fld_name] = val

        for opt in opt_flds:
            if opt not in rec:
                rec[opt] = None

        if len(rec) == len(fields):
            yield (cls(**rec))
