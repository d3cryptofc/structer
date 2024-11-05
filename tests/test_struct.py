import pytest

from structer import Field, String, Struct
from structer.errors import EmptyStructFieldsError, InvalidFieldTypeError


def test_struct_empty_fields():
    expected = EmptyStructFieldsError
    with pytest.raises(expected):
        Struct()


@pytest.mark.parametrize('given', [None, int, str, (), [], {}, ''])
def test_struct_contains_invalid_fields(given):
    expected = InvalidFieldTypeError
    with pytest.raises(expected):
        type('Test', (Struct,), dict(__fields__=(given,)))


def test_attributes_for_field_names_created():
    given = (Field('one', String(5)), Field('two', String(5)))
    struct = type('Test', (Struct,), dict(__fields__=given))
    for field in given:
        assert getattr(struct, field.name) == field


def test_attributes_for_field_names_created_not_replace_existing():
    given = (Field('one', String(5)), Field('one', String(5)))
    expected = AttributeError
    with pytest.raises(expected):
        type('Test', (Struct,), dict(__fields__=given))


def test_get_struct_size_by_hidden_attribute_and_len():
    given = (Field('one', String(5)), Field('two', String(10)))
    expected = 15
    struct = type('Test', (Struct,), dict(__fields__=given))
    assert struct.__struct_size__ == expected
    assert len(struct()) == expected


@pytest.mark.parametrize(
    'given', ['one', 'two', '__struct_binary__', '__struct_fields__']
)
def test_delete_attribute_must_not_work(given):
    expected = AttributeError
    struct = type(
        'Test', (Struct,), dict(__fields__=(Field('one', String(5)),))
    )()
    with pytest.raises(expected):
        delattr(struct, given)


@pytest.mark.parametrize(
    'given', ['two', '__struct_binary__', '__struct_fields__']
)
def test_set_non_field_attribute_must_not_work(given):
    expected = AttributeError
    struct = type(
        'Test', (Struct,), dict(__fields__=(Field('one', String(5)),))
    )()
    with pytest.raises(expected):
        setattr(struct, given, '')


def test_create_struct_without_fields_attribute_must_not_work():
    given = {}
    expected = EmptyStructFieldsError
    with pytest.raises(expected):
        type('Test', (Struct,), given)()


def test_create_struct_passing_fields_as_keyword_argument():
    given = field_name, field_value = ('one', 'X')  # noqa: F841
    expected = field_value
    field = Field(field_name, String(1))

    struct = type('Test', (Struct,), dict(__fields__=(field,)))
    assert struct(**{field_name: field_value}).one == expected


def test_object_representation():
    given = type(
        'Test',
        (Struct,),
        dict(__fields__=(Field('one', String(5)), Field('two', String(10)))),
    )(one='hello')
    expected = "Test(one(5)='hello', two(10)='') -> 15"
    assert repr(given) == expected
