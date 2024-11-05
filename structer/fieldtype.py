from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Union

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

