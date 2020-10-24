from typing import Union, Dict, Any
from collections import namedtuple

from ..constants import Method, StatusCode
from ..url import URL
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
        'protocol',
        'port',
        'http_version',
        'redirect_chain'
    )

    def __init__(self,
                 url: Union[URL, str],
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
        # TODO MessageBody class to handle different types of content
        self.body = body
        self.method = method
        self.http_version = http_version
        self.redirect_chain = []

    @property
    def url(self) -> URL:
        return self._url

    @url.setter
    def url(self, value: Union[URL, str]):
        if isinstance(value, str):
            self._url = URL(value)
        elif isinstance(value, URL):
            self._url = value
        else:
            raise TypeError(f'Invalid type for URL {type(value)}')

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
        source = self.url.copy()
        if location.startswith('/'):
            self.url.path = location
        else:
            self.url.string = location
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
        s = f'{self.method} {self.url.path} HTTP/{self.http_version}\r\n'\
            .encode('ascii')
        self._headers['Host'] = self.url.host
        self._headers.set_if_none('Connection', 'close')
        s += self.headers.to_bytes()
        if self.body:
            s += self.body
        return s

    def to_str(self) -> str:
        return self.to_bytes().decode('utf-8', errors='replace')
