import pytest

from structer import Char, Field, Struct, structfy


@pytest.mark.parametrize('given', [None, 1, b'', [], (), {}, set()])
def test_parameter_name_must_be_str(given):
    expected = TypeError
    with pytest.raises(expected):
        structfy(given, (Field('one', Char()),))


def test_struct_class_name_must_be_equal_to_parameter_name():
    given = 'Test'
    expected = given
    assert structfy(given, (Field('one', Char()),)).__name__ == expected


def test_created_struct_class_is_subclass_of_struct():
    given = structfy('Test', (Field('one', Char()),))
    expected = True
    assert issubclass(given, Struct) == expected
