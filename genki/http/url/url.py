from typing import AnyStr, Union
from copy import copy

from ..constants import Scheme
from .parse import parse_url


class URL:

    __slots__ = (
        '_string',
        '_scheme',
        '_host',
        '_path',
        '_port',
        '_query',
        '_username',
        '_password',
        '_fragment',
        '_dirty'
    )

    def __init__(self, url: str):
        self.string = url

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return f'URL({repr(self.string)})'

    def __eq__(self, value: Union[str, 'URL']) -> bool:
        if isinstance(value, str):
            return self.string == value
        elif isinstance(value, URL):
            return self.string == value.string

    @property
    def string(self) -> str:
        if self._dirty:
            self.update()
        return self._string

    @property
    def scheme(self):
        return self._scheme

    @property
    def host(self):
        return self._host

    @property
    def path(self):
        return self._path

    @property
    def port(self):
        return self._port

    @property
    def query(self):
        return self._query

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def fragment(self):
        return self._fragment

    @string.setter
    def string(self, value: AnyStr):
        if isinstance(value, bytes):
            value = value.decode()

        parse_result = parse_url(value)
        self._scheme = parse_result.scheme
        self._host = parse_result.host
        self._path = parse_result.path
        self._port = parse_result.port
        self._query = parse_result.query
        self._username = parse_result.username
        self._password = parse_result.password
        self._fragment = parse_result.fragment

    @scheme.setter
    def scheme(self, value):
        if self._scheme != value:
            self._dirty = True
        self._scheme = Scheme(value.lower())

    @host.setter
    def host(self, value):
        if self._host != value:
            self._dirty = True
        self._host = value

    @path.setter
    def path(self, value):
        if not value.startswith('/'):
            value = f'/{value}'
        if self._path != value:
            self._dirty = True
        self._path = value

    @port.setter
    def port(self, value):
        if self._port != value:
            self._dirty = True
        self._port = int(value)

    @query.setter
    def query(self, value):
        if self._query != value:
            self._dirty = True
        self._query = value

    @username.setter
    def username(self, value):
        if self._username != value:
            self._dirty = True
        self._username = value

    @password.setter
    def password(self, value):
        if self._password != value:
            self._dirty = True
        self._password = value

    @fragment.setter
    def fragment(self, value):
        if self._fragment != value:
            self._dirty = True
        self._fragment = value

    def update(self):
        """Rebuilds url string
        """
        url = ''
        if self.username:
            userinfo_str = self.username
            if self.password:
                userinfo_str += f':{self.password}'
            userinfo_str += '@'
        else:
            userinfo_str = ''

        if any([
                self.port == 443 and self.scheme == 'https',
                self.port == 80 and self.scheme == 'http'
                ]):
            port_str = ''
        else:
            port_str = f':{self.port}'

        url = f'{self.scheme}://{userinfo_str}{self.host}{port_str}' +\
            f'{self.path}'

        if self.query:
            url += f'?{self.query}'
        if self.fragment:
            url += f'#{self.fragment}'

        self._string = url
        self._dirty = False

    def copy(self):
        return copy(self)
