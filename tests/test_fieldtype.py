import pytest

from structer.fieldtypes.base import FieldType


def test_non_integer_size():
    given = None
    expected = TypeError
    with pytest.raises(expected):
        FieldType(given)


@pytest.mark.parametrize('given', (0, -1))
def test_invalid_integer_size(given):
    expected = ValueError
    with pytest.raises(expected):
        FieldType(given)
