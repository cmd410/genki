from typing import Union, Mapping

from ..constants import Method
from .util import parse_url
from ..headers import Headers


class RequestBuilder:
    __slots__ = (
        '_url',
        '_headers',
        '_method',
        '_body',
        '_host',
        'protocol',
        'path',
        'port',
        'http_version',
    )

    def __init__(self,
                 url: str,
                 headers: Union[
                     Headers,
                     Mapping[str, Union[str, int]]
                    ] = Headers(),
                 body: Union[str, bytes, bytearray] = b'',
                 method: Union[Method, str] = Method.GET,
                 http_version: str = '1.1'):
        self.headers = headers
        self.url = url
        self.body = body
        self.method = method
        self.http_version = http_version

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        self.protocol,\
            self.host,\
            self.path,\
            self.port = parse_url(value)

        self._url = value

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value
        self.headers['Host'] = value

    @property
    def headers(self) -> Headers:
        return self._headers

    @headers.setter
    def headers(self,
                value: Union[Headers, Mapping[str, Union[str, int]], bytes]):
        if isinstance(value, Headers):
            self._headers = value
        elif isinstance(value, dict):
            self._headers = Headers(value)
        elif isinstance(value, bytes):
            self._headers = Headers.from_bytes(value)
        else:
            raise TypeError(
                f'Unsuitable type for Request headers: {type(value)}'
            )

    @property
    def method(self) -> Method:
        return self._method

    @method.setter
    def method(self, value: Union[Method, str]):
        self._method = Method(value)

    @property
    def body(self) -> bytes:
        return self._body

    @body.setter
    def body(self,
             value: Union[str, bytes, bytearray, None],
             str_encoding='utf-8'):
        if not value:
            self._body = b''
        elif isinstance(value, bytes):
            self._body = value
        elif isinstance(value, bytearray):
            self._body = bytes(value)
        elif isinstance(value, str):
            self._body = value.encode(str_encoding)
        else:
            raise TypeError(f'Unsuitable type for body: {type(value)}')

        if self.body:
            self.headers['Content-Length'] = len(self.body)
        elif self.headers.get('Content-Length') is not None:
            self.headers.remove_header('Content-Length')

    def append_body(self, b: Union[str, bytes, bytearray], encoding='utf-8'):
        if b:
            if isinstance(b, str):
                b = b.encode(encoding)
            self.body = self.body + b

    def set_header(self, key: str, value: Union[str, int]) -> 'RequestBuilder':
        self.headers[key] = value
        return self

    def remove_header(self, key: str) -> 'RequestBuilder':
        self.headers.remove_header(key)
        return self

    def to_bytes(self) -> bytes:
        s: bytes = f'{self.method} {self.path} HTTP/{self.http_version}\r\n'\
            .encode('ascii')
        s += self.headers.to_bytes()
        if self.body:
            s += self.body
        return s

    def to_str(self) -> str:
        return self.to_bytes().decode('utf-8', errors='replace')
