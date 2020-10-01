from logging import getLogger
from typing import Union

from gevent import socket, ssl, spawn

from .headers import Headers
from .constants import Method, Code, Protocol
from .util import parse_url
from .response import Response

logger = getLogger('genki')


def encode_body(body: Union[bytes, bytearray, str]) -> bytes:
    if isinstance(body, bytes) or isinstance(body, bytearray):
        return body
    elif isinstance(body, str):
        return bytes(body, encoding='utf-8')
    else:
        raise TypeError(f'Cannot encode body of type {type(body).__name__}')


def request(url:str,
            headers: Headers=Headers(),
            method: Method=Method.GET,
            body: Union[bytes, bytearray, str]=b'',
            follow_redirects=True
            ) -> Response:
    logger.debug(f'Requesting: {url}')
    proto, host, path, port = parse_url(url)
    first_line = f'{method} {path} HTTP/1.1\r\n'

    headers['Host'] = host
    request_body = encode_body(body)

    if request_body:
        headers.set_if_none('Content-Length', len(request_body))

    request_head = first_line + headers.to_str()
    request_bytes = bytes(request_head, encoding='ascii') + request_body
    
    sock = socket.create_connection((host, port))

    if proto == Protocol.HTTPS:
        sock = ssl.wrap_socket(sock)
    
    sock.sendall(request_bytes)

    response = b''
    while b'\r\n\r\n' not in response:
        response += sock.recv(512)
    
    r_headers_bytes, r_body_bytes = response.split(b'\r\n\r\n', maxsplit=1)

    response_headers = Headers.from_bytes(response)

    body_length = response_headers.get('Content-Length', 0)

    while len(r_body_bytes) < body_length:
        r_body_bytes += sock.recv(512)

    sock.close()

    response = Response(url,
                        response[:response.find(b'\r\n')].decode(),
                        response_headers,
                        r_body_bytes)

    if 300 <= response.status_code < 400 and follow_redirects:
        new_location = response.headers.get("Location")
        logger.debug(f'Being redirected to: {new_location}')
        return spawn(request,
                     new_location,
                     method=method,
                     headers=headers,
                     body=body,
                     follow_redirects=follow_redirects).get()

    return response
