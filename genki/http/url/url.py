from typing import AnyStr, Union
from copy import copy

from ..constants import Protocol
from .parse import parse_url


class URL:

    __slots__ = (
        '_string',
        '_protocol',
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

    @string.setter
    def string(self, value: AnyStr):
        if isinstance(value, bytes):
            value = value.decode()

        parse_result = parse_url(value)
        self._protocol = parse_result.protocol
        self._host = parse_result.host
        self._path = parse_result.path
        self._port = parse_result.port
        self._query = parse_result.query
        self._username = parse_result.username
        self._password = parse_result.password
        self._fragment = parse_result.fragment

        self._dirty = True

    @property
    def protocol(self):
        return self._protocol

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

    @protocol.setter
    def protocol(self, value):
        self._protocol = Protocol(value.lower())
        self._dirty = True

    @host.setter
    def host(self, value):
        self._host = value
        self._dirty = True

    @path.setter
    def path(self, value):
        if not value.startswith('/'):
            value = f'/{value}'
        self._path = value
        self._dirty = True

    @port.setter
    def port(self, value):
        self._port = int(value)
        self._dirty = True

    @query.setter
    def query(self, value):
        self._query = value
        self._dirty = True

    @username.setter
    def username(self, value):
        self._username = value
        self._dirty = True

    @password.setter
    def password(self, value):
        self._password = value
        self._dirty = True

    @fragment.setter
    def fragment(self, value):
        self._fragment = value
        self._dirty = True

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
                self.port == 443 and self.protocol == 'https',
                self.port == 80 and self.protocol == 'http'
                ]):
            port_str = ''
        else:
            port_str = f':{self.port}'

        url = f'{self.protocol}://{userinfo_str}{self.host}{port_str}' +\
            f'{self.path}'

        if self.query:
            url += f'?{self.query}'
        if self.fragment:
            url += f'#{self.fragment}'

        self._string = url
        self._dirty = False

    def copy(self):
        return copy(self)
