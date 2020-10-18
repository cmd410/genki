from collections import namedtuple
from typing import Tuple

from ..constants import Protocol
from ..exceptions import InvalidURL


url_parse_result = namedtuple(
    'URLParseResult',
    ['protocol', 'host', 'path', 'port', 'username', 'password', 'query'])


def parse_url(url: str) -> url_parse_result:
    """Parses given url, returns namedtuple of
    (protocol, host, path, port, username, password)
    """
    url = str(url).strip()

    # Parse protocol
    proto: Protocol = Protocol.HTTP
    if '://' in url:
        s = url.split('://', maxsplit=1)
        proto = Protocol(s[0].lower())
        host = s[1]
    else:
        host = url

    # Assume port based on protocol
    port = 80 if proto == Protocol.HTTP else 443

    if not host:
        raise InvalidURL(url)

    # Parse username and password
    username, password = '', ''
    if '@' in host:
        at_pos = host.find('@')
        user_info = host[:at_pos]
        host = host[at_pos + 1:]
        if ':' not in user_info:
            username = user_info
            password = ''
        else:
            username, password = user_info.split(':')

    # Parse path
    if '/' not in host:
        path = '/'
    else:
        host, path = host.split('/', maxsplit=1)
        path = '/' + path

    query = ''
    if '?' in path:
        query = path[path.find('?') + 1:]
        path = path[:path.find('?')]

    if not host:
        raise InvalidURL(url)

    # Parse port
    if ':' in host:
        host, port_str = host.split(':', maxsplit=1)
        if not all([host, port_str]):
            raise InvalidURL(url)
        port = int(port_str)

    return url_parse_result(
        proto,
        host,
        path,
        port,
        username,
        password,
        query
        )
