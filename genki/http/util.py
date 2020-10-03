from typing import Tuple

from .constants import Protocol
from .exceptions import InvalidURL


def parse_url(url: str) -> Tuple[Protocol, str, str, int]:
    """Parses given url, returns tuple of (protocol, host, path, port)
    """
    url = str(url).strip()

    proto: Protocol = Protocol.HTTP
    if '://' in url:
        s = url.split('://', maxsplit=1)
        proto = Protocol(s[0].lower())
        address = s[1]
    else:
        address = url

    port = 80 if proto == Protocol.HTTP else 443

    if not address:
        raise InvalidURL(url)

    if '/' not in address:
        if ':' in address:
            address, port_str = address.split(':', maxsplit=1)
            if not all([address, port_str]):
                raise InvalidURL(url)
            port = int(port_str)
        return proto, address, '/', port

    host, path = address.split('/', maxsplit=1)
    if not host:
        raise InvalidURL(url)

    if ':' in host:
        host, port_str = host.split(':', maxsplit=1)
        if not all([host, port_str]):
            raise InvalidURL(url)
        port = int(port_str)

    return proto, host, '/'+path, port