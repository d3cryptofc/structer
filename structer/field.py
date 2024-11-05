import re

from .fieldtype import FieldTypeABC


class Field:
    def __init__(self, field_name: str, field_type: FieldTypeABC):
        if not isinstance(field_name, str):
            raise TypeError('`field_name` parameter must be a string')
        if field_name.startswith('_'):
            raise ValueError(
                '`field_name` parameter must not starts by underscores (_)'
            )
        if not re.search(r'^[A-za-z][A-za-z0-9_]*$', field_name):
            raise ValueError(
                '`field_name` parameter is invalid, must be alphanumeric'
            )

        if not issubclass(type(field_type), FieldTypeABC):
            raise TypeError(
                '`field_type` parameter must be a valid field type.'
            )

        self._name = field_name
        self._type = field_type

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def __repr__(self):
        return 'Field({!r}, {!r})'.format(self._name, self._type)
