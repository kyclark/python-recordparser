import io
import pytest
import recordparser as p
from typing import NamedTuple


class Item(NamedTuple):
    id_: int
    name: str
    price: float


# --------------------------------------------------
def test_parse_01() -> None:
    """Parse OK"""

    text = io.StringIO('\n'.join(
        ['id_,name,price', '1,foo,3.25', '2,bar,.43', '3,baz,4.01']))
    data = list(p.parse(fh=text, cls=Item, delimiter=','))
    assert len(data) == 3

# --------------------------------------------------
def test_parse_extra_fields() -> None:
    """Parses OK when extra fields"""

    text = io.StringIO('\n'.join(
        ['id_,name,price', '1,foo,3.25', '2,bar,.43', '3,baz,4.01']))
    data = list(p.parse(fh=text, cls=Item, delimiter=','))
    assert len(data) == 3


# --------------------------------------------------
def test_missing_field() -> None:
    """Exception when missing a field"""

    text = io.StringIO('\n'.join(['id_,name', '1,foo', '2,bar', '3,baz']))

    with pytest.raises(Exception):
        data = list(p.parse(fh=text, cls=Item))


# --------------------------------------------------
def test_skip_bad_type() -> None:
    """Skips record with bad type"""

    text = io.StringIO('\n'.join(
        ['id_,name,price', '1,foo,3.25', '2,bar,O.43', '3,baz,4.01']))
    data = list(p.parse(fh=text, cls=Item))
    assert len(data) == 2
    assert 'bar' not in [r.name for r in data]
