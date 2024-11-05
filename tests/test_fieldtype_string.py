import pytest

from structer import String


def test_field_property_size():
    given = 15
    expected = 15
    assert String(given).size == expected


def test_field_encode_non_string_value():
    given = None
    expected = TypeError
    with pytest.raises(expected):
        print(String(1).encode(given))


def test_field_encode_value_oversized():
    given = 'ABCDEF'
    expected = ValueError
    with pytest.raises(expected):
        String(len(given) - 1).encode(given)


@pytest.mark.parametrize(
    ('given_text', 'given_distance', 'expected'),
    [
        ('ABCDEF', 0, b'ABCDEF'),
        ('A', 5, b'A\0\0\0\0\0'),
        ('', 5, b'\0\0\0\0\0'),
    ],
)
def test_field_encode_value_non_oversized(
    given_text, given_distance, expected
):
    assert (
        String(len(given_text) + given_distance).encode(given_text) == expected
    )


def test_field_decode_non_bytes_value():
    given = None
    expected = TypeError
    with pytest.raises(expected):
        print(String(1).decode(given))


@pytest.mark.parametrize(
    ('given', 'expected'),
    [(b'ABCDEF', 'ABCDEF'), (b'A\0\0\0\0\0', 'A'), (b'\0\0\0\0\0\0', '')],
)
def test_field_decode(given, expected):
    instance = String(len(given))
    assert instance.decode(given) == expected
