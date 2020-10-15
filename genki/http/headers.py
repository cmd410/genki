from typing import Union, Dict


class Headers:
    __slots__ = ('_headers')

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value: dict):
        self._headers: dict = value

    @classmethod
    def from_bytes(cls, b: bytes):
        if b'\r\n\r\n' in b:
            b = b[:b.find(b'\r\n\r\n')]

        headers: Dict[str, Union[str, int]] = dict()
        for line in b.split(b'\r\n'):
            if b':' in line:
                header, *value = line.split(b':', maxsplit=1)
                if not value:
                    continue

                header_str, value_str = \
                    header.decode().strip(), value[0].decode().strip()

                if header_str in headers.keys():
                    # Multiple message-header fields
                    # Accoring to RFC 2616
                    headers[header_str] = \
                        str(headers[header_str]) + ',' + value_str
                elif value_str.isdigit():
                    value_int = int(value_str)
                    headers[header_str] = value_int
                else:
                    headers[header_str] = value_str
        return Headers(headers)

    def to_str(self):
        s = '\r\n'.join(
            [
                f'{key}: {value}'
                for key, value in self.headers.items()
            ]
        )
        s += '\r\n\r\n'
        return s

    def to_bytes(self):
        return self.to_str().encode()

    def get(self, key, default=None):
        return self.headers.get(key, default)

    def set_if_none(self, key, value):
        if key not in self.headers.keys():
            self.headers[key] = value

    def remove_header(self, key: str):
        self._headers.pop(key)

    def __bool__(self):
        return bool(self.headers)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.headers})'

    def __init__(self, headers: dict = dict()):
        self.headers = headers

    def __getitem__(self, key):
        return self.headers[key]

    def __setitem__(self, key, value):
        self.headers[key] = value

    def __contains__(self, item):
        return item in self.headers.keys()
