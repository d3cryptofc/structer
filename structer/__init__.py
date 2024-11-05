from inspect import currentframe
from typing import Sequence

from .field import Field  # noqa: F401
from .fieldtypes.char import Char  # noqa: F401
from .fieldtypes.string import Str, String  # noqa: F401
from .struct import Struct  # noqa: F401


def structfy(name: str, fields: Sequence[Field]):
    if not isinstance(name, str):
        raise TypeError('`name` parameter must be a string')

    namespace = dict(__fields__=fields)

    frame = currentframe()
    if frame and frame.f_back:
        namespace['__module__'] = frame.f_back.f_globals['__name__']

    return type(name, (Struct,), namespace)
