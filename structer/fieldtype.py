class FieldType:
    def __init__(self, size: int):
        if not isinstance(size, int):
            raise TypeError('`size` parameter must be an integer')
        if size < 1:
            raise ValueError('`size` parameter must be greather than zero')
        self._size = size

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self._size)
