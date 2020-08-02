import io
import pytest
import recordparser as p
from typing import NamedTuple, Optional, Union


class Item(NamedTuple):
    id_: int
    name: str
    price: float


class Item2(NamedTuple):
    id_: int
    name: str
    price: float
    can_discount: bool


class Item3(NamedTuple):
    id_: int
    name: str
    price: float
    can_discount: Optional[bool]


class Item4(NamedTuple):
    id_: int
    name: str
    price: Union[float, str]
    can_discount: Optional[bool]


# --------------------------------------------------
def test_parse_01() -> None:
    """Parse OK"""

    text = io.StringIO('\n'.join(
        ['id_,name,price', '1,foo,3.25', '2,bar,.43', '3,baz,4.01']))
    data = list(p.parse(fh=text, cls=Item, delimiter=','))
    assert len(data) == 3
    assert isinstance(data[0].id_, int)
    assert isinstance(data[0].name, str)
    assert isinstance(data[0].price, float)


# --------------------------------------------------
def test_parse_delimiter() -> None:
    """Parse OK, set delimiter"""

    text = io.StringIO('\n'.join(
        ['id_\tname\tprice', '1\tfoo\t3.25', '2\tbar\t.43', '3\tbaz\t4.01']))
    data = list(p.parse(fh=text, cls=Item, delimiter='\t'))
    assert len(data) == 3
    assert isinstance(data[0].id_, int)
    assert isinstance(data[0].name, str)
    assert isinstance(data[0].price, float)


# --------------------------------------------------
def test_parse_skip_extra_fields() -> None:
    """Parses OK when extra fields"""

    text = io.StringIO('\n'.join([
        'id_,name,price,can_discount', '1,foo,3.25,True', '2,bar,.43,False',
        '3,baz,4.01,True'
    ]))

    data = list(p.parse(fh=text, cls=Item, delimiter=','))
    assert len(data) == 3


# --------------------------------------------------
def test_parse_02() -> None:
    """Parse OK"""

    text = io.StringIO('\n'.join([
        'id_,name,price,can_discount', '1,foo,3.25,True', '2,bar,.43,False',
        '3,baz,4.01,True'
    ]))
    data = list(p.parse(fh=text, cls=Item2, delimiter=','))
    assert len(data) == 3
    assert isinstance(data[0].id_, int)
    assert isinstance(data[0].name, str)
    assert isinstance(data[0].price, float)
    assert isinstance(data[0].can_discount, bool)


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


# --------------------------------------------------
def test_optional_field_missing() -> None:
    """Handle missing/optional"""

    text = io.StringIO('\n'.join(
        ['id_,name,price', '1,foo,3.25', '2,bar,0.43', '3,baz,4.01']))
    data = list(p.parse(fh=text, cls=Item3))
    assert len(data) == 3
    assert data[0].can_discount is None


# --------------------------------------------------
def test_optional_field_present() -> None:
    """Handle missing/optional"""

    text = io.StringIO('\n'.join([
        'id_,name,price,can_discount', '1,foo,3.25,True', '2,bar,0.43,False',
        '3,baz,4.01,True'
    ]))
    data = list(p.parse(fh=text, cls=Item3))
    assert len(data) == 3
    assert data[0].can_discount is True


# --------------------------------------------------
def test_union() -> None:
    """Handle Union"""

    text = io.StringIO('\n'.join(
        ['id_,name,price', '1,foo,3.25', '2,bar,NA', '3,baz,4.01']))
    data = list(p.parse(fh=text, cls=Item4))
    assert len(data) == 3
    assert data[0].price == 3.25
    assert data[1].price == 'NA'
