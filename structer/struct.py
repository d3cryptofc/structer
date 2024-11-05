from types import MappingProxyType
from typing import ClassVar, NoReturn, Sequence

from . import errors
from .field import Field


class Struct:
    __fields__: ClassVar[Sequence[Field]]
    __struct_fields__: ClassVar[MappingProxyType[str, Field]]
    __struct_size__: ClassVar[int]
    __struct_binary__: bytes
    __struct_offsets__: MappingProxyType[str, tuple[int, int]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if hasattr(cls, '__fields__'):
            fields = cls.__fields__[:]
        else:
            fields = ()

        if not fields:
            raise errors.EmptyStructFieldsError

        newfields = {}

        cls.__struct_size__ = 0
        for field in fields:
            if not issubclass(type(field), Field):
                raise errors.InvalidFieldTypeError(field)

            if hasattr(cls, field.name):
                raise AttributeError(
                    '{!r} field name already exists'.format(field.name)
                )

            setattr(cls, field.name, field)
            newfields[field.name] = field
            cls.__struct_size__ += field.type.size

        del cls.__fields__
        cls.__struct_fields__ = MappingProxyType(newfields)
        cls.__module__ = cls.__module__
        return cls

    def __init__(self, **kwargs):
        if not hasattr(self, '__struct_fields__'):
            raise errors.EmptyStructFieldsError

        setattr = object.__setattr__
        setattr(self, '__struct_binary__', b'')
        setattr(self, '__struct_size__', 0)

        start_range = 0
        setattr(self, '__struct_offsets__', {})

        for field in self.__struct_fields__.values():
            setattr(
                self,
                '__struct_binary__',
                self.__struct_binary__ + (field.type.size * b'\0'),
            )

            if field.name in kwargs:
                field_value = kwargs[field.name]
                field.type._validate_encode(field_value)
            else:
                field_value = field.type.decode(b'\0')

            self.__struct_offsets__[field.name] = (
                start_range,
                start_range + field.type.size,
            )
            self.__setattr__(field.name, field_value)
            setattr(
                self, '__struct_size__', self.__struct_size__ + field.type.size
            )

            start_range += field.type.size

        setattr(
            self,
            '__struct_offsets__',
            MappingProxyType(self.__struct_offsets__),
        )

    def __len__(self):
        return self.__struct_size__

    def __repr__(self):
        repr_parameters = ', '.join(
            '{}({})={!r}'.format(
                field.name, field.type._size, getattr(self, field.name)
            )
            for field in self.__struct_fields__.values()
        )
        return '{}({}) -> {!r}'.format(
            type(self).__name__, repr_parameters, self.__struct_size__
        )

    def __delattr__(self, _: str) -> NoReturn:
        raise AttributeError('attribute removal is not allowed')

    def __setattr__(self, name: str, value: str) -> None:
        if name not in self.__struct_fields__:
            msg = ('set attribute {!r} is not allowed').format(name)
            raise AttributeError(msg)

        setattr = object.__setattr__
        field = self.__struct_fields__[name]

        start_range, stop_range = self.__struct_offsets__[name]
        offset_range = range(start_range, stop_range + 1)

        field_data = field.type.encode(value)
        struct_data = bytearray(self.__struct_binary__)

        for index, decimal in zip(offset_range, field_data):
            struct_data[index] = decimal

        setattr(self, '__struct_binary__', bytes(struct_data))
        setattr(self, name, value)
