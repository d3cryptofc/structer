import pytest

from structer import Char, Field


@pytest.mark.parametrize('given', [None, 1, [], (), {}])
def test_invalid_type_for_field_name(given):
    expected = TypeError
    with pytest.raises(expected):
        Field(field_name=given, field_type=Char())


@pytest.mark.parametrize('given', ['_test', '#test;', '10test'])
def test_invalid_value_for_field_name(given):
    expected = ValueError
    with pytest.raises(expected):
        Field(field_name=given, field_type=Char())


@pytest.mark.parametrize('given', [int, str, list, dict, None, 1, ''])
def test_invalid_type_for_field_type(given):
    expected = TypeError
    with pytest.raises(expected):
        Field(field_name='test', field_type=given)


def test_field_name_property():
    given = 'test'
    expected = given
    assert Field(field_name=given, field_type=Char()).name == expected


def test_field_type_property():
    given = Char()
    expected = given
    assert Field(field_name='test', field_type=given).type == expected


def test_object_representation():
    given = dict(field_name='myfield', field_type=Char())
    expected = "Field('myfield', Char(1))"
    print(repr(Field(**given)))
    field = Field(**given)
    assert repr(field) == expected
