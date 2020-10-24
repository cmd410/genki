from collections import namedtuple

from ..constants import Protocol
from .exceptions import InvalidURL


url_parse_result = namedtuple(
    'URLParseResult',
    ['protocol', 'host', 'path', 'port',
     'username', 'password', 'query', 'fragment'])


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
    port = 443 if proto == Protocol.HTTPS else 80

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
        if not username:
            raise InvalidURL(url)

    if password and not username:
        raise InvalidURL(url)

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
    if '[' in host and (closing := host.find(']')) != -1:
        if closing != len(host) - 1:
            if host[closing + 1] == ':':
                port = int(host[closing + 2:])
                host = host[:closing + 1]
    elif ':' in host:
        host, port_str = host.split(':', maxsplit=1)
        if not all([host, port_str]):
            raise InvalidURL(url)
        port = int(port_str)

    fragment = ''
    if query:
        if (fragment_idx := query.find('#')) != -1:
            fragment = query[fragment_idx + 1:]
            query = query[:fragment_idx]
    else:
        if (fragment_idx := path.find('#')) != -1:
            fragment = path[fragment_idx + 1:]
            path = path[:fragment_idx]

    return url_parse_result(
        proto,
        host,
        path,
        port,
        username,
        password,
        query,
        fragment
        )
