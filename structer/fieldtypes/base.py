from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Union


class FieldTypeABC(ABC):
    _size: int

    @abstractproperty
    def size(self) -> int: ...

    @abstractmethod
    def _validate_encode(self, value: str) -> None: ...

    @abstractmethod
    def encode(self, value: str) -> bytes: ...

    @abstractmethod
    def decode(
        self, value: Union[bytes, bytearray], **kwargs: bool
    ) -> str: ...

    @abstractmethod
    def _validate_decode(self, value: Union[bytes, bytearray]) -> None: ...


class FieldType(FieldTypeABC):
    def __init__(self, size: int) -> None:
        if not isinstance(size, int):
            raise TypeError('`size` parameter must be an integer')
        if size < 1:
            raise ValueError('`size` parameter must be greather than zero')
        self._size = size

    @property
    def size(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return '{}({!r})'.format(type(self).__name__, self._size)
