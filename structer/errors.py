from .fieldtypes.base import FieldType


class EmptyStructFieldsError(Exception):
    def __init__(self) -> None:
        self.args = ('struct fields must not be empty',)


class InvalidFieldTypeError(Exception):
    def __init__(self, value: object) -> None:
        self.args = ('struct field {} is not supported'.format(type(value)),)


def str_value_oversized_error(field_type: FieldType) -> ValueError:
    message = (
        '`{}` value size must be {} bytes at most '
        '(accents usually occupy more than one byte)'
    ).format(type(field_type).__name__, field_type._size)
    return ValueError(message)
