from typing import Union, Dict, Any
from collections import namedtuple

from ..constants import Method, StatusCode
from .util import parse_url
from ..headers import Headers


redirect = namedtuple(
    'Redirect',
    ['source', 'destination', 'status_code']
    )


class RequestBuilder:
    __slots__ = (
        '_url',
        '_headers',
        '_method',
        '_body',
        '_host',
        'username',
        'password',
        'protocol',
        'path',
        'port',
        'http_version',
        'query',
        'redirect_chain'
    )

    def __init__(self,
                 url: str,
                 params: Dict[str, Any] = dict(),
                 headers: Union[
                     Headers,
                     Dict[str, Union[str, int]],
                     bytes] = Headers(),
                 body: Union[str, bytes, bytearray] = b'',
                 method: Union[Method, str] = Method.GET,
                 http_version: str = '1.1'):
        self.headers = headers
        self.url = url
        self.body = body
        self.method = method
        self.http_version = http_version
        self.redirect_chain = []

    @property
    def url(self) -> str:
        url = f'{self.protocol}://'
        if self.username:
            url += f'{self.username}'
            if self.password:
                url += f':{self.password}'
            url += '@'

        url += self.host
        if self.port not in {80, 443}:
            url += str(self.port)

        url += self.path
        if self.query:
            url += f'?{self.query}'
        return url

    @url.setter
    def url(self, value: str):
        parse_result = parse_url(value)

        self.protocol = parse_result.protocol
        self.host = parse_result.host
        self.path = parse_result.path
        self.port = parse_result.port
        self.query = parse_result.query
        self.username = parse_result.username
        self.password = parse_result.password

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
                value: Union[Headers, Dict[str, Union[str, int]], bytes]):
        if isinstance(value, Headers):
            self._headers = value
        elif isinstance(value, Dict):
            self._headers = Headers(value)
        elif isinstance(value, bytes):
            self._headers = Headers.from_bytes(value)
        else:
            raise TypeError(
                f'Unsuitable type for Request headers: {type(value)}'
            )
        self._headers.set_if_none('Connection', 'close')

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

    def redirect_to(self, code: StatusCode, location: str):
        source = self.url
        if location.startswith('/'):
            self.path = location
        else:
            self.url = location
        destination = self.url
        self.redirect_chain.append(redirect(source, destination, code))

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
