"""
RecordParser

Parse a delimited text file into records of a given class
converting the types to those described by the class.

Author : Ken Youens-Clark <kyclark@gmail.com>
"""

import csv
import sys
from typing import TextIO, Iterable, Any


# --------------------------------------------------
def parse(cls: type, fh: TextIO, delimiter: str = ',', quiet: bool = False) -> Iterable[Any]:
    """Create a parser"""

    reader = csv.DictReader(fh, delimiter=delimiter)
    fields = cls._field_types
    missing = [name for name in fields if name not in reader.fieldnames]

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
            if not fld_name in row:
                warn(f'{row_num}: Missing field "{fld_name}"')
                continue

            raw_val = row[fld_name]
            val = None
            try:
                val = fld_type(raw_val)
            except:
                pass

            if val is None:
                warn(f'{row_num}: Cannot convert "{raw_val}" to "{fld_type}"')
                continue

            rec[fld_name] = val

        if len(rec) == len(fields):
            yield(cls(**rec))
