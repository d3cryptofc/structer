from typing import Union

from .string import String


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