from collections import OrderedDict
from typing import Union, Mapping, Dict


class Headers(OrderedDict):
    @classmethod
    def from_bytes(cls, b: bytes):
        if b'\r\n\r\n' in b:
            b = b[:b.find(b'\r\n\r\n')]

        headers: Dict[str, Union[str, int]] = Headers()
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
        return headers

    def to_str(self):
        s = '\r\n'.join(
            [
                f'{key}: {value}'
                for key, value in self.items()
            ]
        )
        s += '\r\n\r\n'
        return s

    def to_bytes(self):
        return self.to_str().encode()

    def __bool__(self):
        return bool(self.headers)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.headers})'

    def __init__(self, headers: Mapping = dict()):
        for key, value in headers.items():
            self[key] = value
