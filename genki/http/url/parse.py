from collections import namedtuple

from ..constants import Scheme
from .exceptions import InvalidURL


url_parse_result = namedtuple(
    'URLParseResult',
    ['scheme', 'host', 'path', 'port',
     'username', 'password', 'query', 'fragment'])


default_ports = {
    Scheme.HTTP: 80,
    Scheme.HTTPS: 443
}


def parse_url(url: str) -> url_parse_result:
    """Parses given url, returns namedtuple of
    (scheme, host, path, port, username, password)
    """
    url = str(url).strip()

    # Parse scheme
    scheme: Scheme = Scheme.HTTP
    if '://' in url:
        s = url.split('://', maxsplit=1)
        scheme = Scheme(s[0].lower())
        host = s[1]
    else:
        host = url

    # Assume port based on scheme
    port = default_ports[scheme]

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
        scheme,
        host,
        path,
        port,
        username,
        password,
        query,
        fragment
        )
