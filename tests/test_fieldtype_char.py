import pytest

from structer import Char


def test_create_char_and_check_size():
    given = Char()
    expected = 1
    assert given.size == expected


@pytest.mark.parametrize('given', [None, 1, b'', [], (), {}, set()])
def test_type_value_to_encode_must_be_str(given):
    expected = TypeError
    with pytest.raises(expected):
        Char().encode(given)


def test_null_byte_value_to_encode_must_return_null_byte():
    given = '\0'
    expected = b'\0'
    assert Char().encode(given) == expected


def test_non_null_byte_string_value_to_encode():
    given = 'f'
    expected = b'f'
    assert Char().encode(given) == expected


def test_empty_string_value_to_encode():
    given = ''
    expected = b''
    assert Char().encode(given) == expected


@pytest.mark.parametrize('given', [None, 1, '', [], (), {}, set()])
def test_type_value_to_decode_must_be_bytes(given):
    expected = TypeError
    with pytest.raises(expected):
        assert Char().decode(given) == expected


def test_oversized_value():
    given = b'abcd'
    expected = ValueError
    with pytest.raises(expected):
        assert Char().decode(given) == expected


def test_empty_byte_value_to_decode_must_return_empty_string():
    given = b''
    expected = ''
    assert Char().decode(given) == expected


def test_null_byte_value_to_decode_must_return_empty_string():
    given = b'\0'
    expected = ''
    assert Char().decode(given) == expected
