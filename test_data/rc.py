#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Purpose: Proof of concept for recordparser
"""

import argparse
import recordparser
import sys
from typing import NamedTuple, TextIO, Optional, Iterable, Union


class Args(NamedTuple):
    file: TextIO
    delimiter: str
    quiet: bool


class Item(NamedTuple):
    id_: int
    name: str
    # price: float
    price: Union[float, str]
    # price: Optional[float]
    # can_discount: Optional[bool]


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Proof of concept for recordparser',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    parser.add_argument('-d',
                        '--delimiter',
                        help='Field delimiter',
                        metavar='DELIM',
                        type=str,
                        default=',')

    parser.add_argument('-q',
                        '--quiet',
                        help='Do not emit errors',
                        action='store_true')

    args = parser.parse_args()

    return Args(args.file, args.delimiter, args.quiet)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    try:
        # Normal
        parser: Iterable[Item] = recordparser.parse(fh=args.file,
                                                    cls=Item,
                                                    delimiter=args.delimiter,
                                                    quiet=args.quiet)

        # # Rename fields with "mapping"
        # mapping = {'id': 'id_', 'item': 'name', 'cost': 'price'}
        # parser: Iterable[Item] = recordparser.parse(fh=args.file,
        #                                             cls=Item,
        #                                             mapping=mapping,
        #                                             delimiter=args.delimiter,
        #                                             quiet=args.quiet)

        # # Input file with no columns
        # parser: Iterable[Item] = recordparser.parse(
        #     fh=args.file,
        #     cls=Item,
        #     fieldnames=['id_', 'name', 'price'],
        #     delimiter=args.delimiter,
        #     quiet=args.quiet)

        for rec in parser:
            print(rec)

    except Exception as err:
        print(err)


# --------------------------------------------------
if __name__ == '__main__':
    main()
