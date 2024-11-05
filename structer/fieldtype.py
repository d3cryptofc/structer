from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Union

from . import errors


class FieldType:
    def __init__(self, size: int):
        if not isinstance(size, int):
            raise TypeError('`size` parameter must be an integer')
        if size < 1:
            raise ValueError('`size` parameter must be greather than zero')
        self._size = size

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self._size)


class FieldTypeABC(ABC):
    @abstractproperty
    def size(self): ...

    @abstractmethod
    def _validate_encode(self, value: str) -> None: ...

    @abstractmethod
    def encode(self, value: str) -> bytes: ...

    @abstractmethod
    def decode(self, value: Union[bytes, bytearray], **kwargs) -> str: ...

    @abstractmethod
    def _validate_decode(self, value: Union[bytes, bytearray]) -> None: ...


class String(FieldTypeABC, FieldType):
    def __init__(self, size: int):
        super().__init__(size)
        self._size = size

    @property
    def size(self):
        return self._size

    def _validate_encode(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError('`text` parameter must be a string')

        if len(text.encode(encoding='utf8')) > self._size:
            raise errors.str_value_oversized_error(self)

    def encode(self, text: str) -> bytes:
        self._validate_encode(text)
        return text.encode(encoding='utf8') + (
            (self._size - len(text)) * b'\0'
        )

    def _validate_decode(self, value: Union[bytes, bytearray]) -> None:
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(
                '`value` parameter must be of type bytes or bytearray'
            )

        if len(value) > self._size:
            raise errors.str_value_oversized_error(self)

    def decode(self, value: Union[bytes, bytearray], **kwargs) -> str:
        self._validate_decode(value)

        string = ''
        for position, decimal in enumerate(value, 1):
            if decimal == 0:
                break

            string += chr(decimal)

            if not kwargs.get('no_limit_by_size') and position == self._size:
                break

        return string


class Char(String):
    def __init__(self):
        super().__init__(size=1)

    def encode(self, value: str) -> bytes:
        self._validate_encode(value)
        if value != '\0':
            return value.encode(encoding='utf8')
        else:
            return b'\0'

    def decode(self, value: Union[bytes, bytearray], **kwargs) -> str:
        self._validate_decode(value)

        if value != b'\0':
            return value.decode(encoding='utf8')
        else:
            return ''


Str = String
