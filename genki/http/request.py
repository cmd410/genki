from logging import getLogger
from typing import Union, Optional
from contextlib import suppress

from gevent import socket, ssl, spawn, Greenlet, GreenletExit
from gevent.util import wrap_errors

from .headers import Headers
from .constants import Method, Protocol
from .util import parse_url
from .response import Response

logger = getLogger('genki')


def expect(errs):
    errs = tuple(errs)
    def decorator(func):
        return wrap_errors(errs, func)
    return decorator


def encode_body(body: Union[bytes, bytearray, str]) -> bytes:
    """Encodes body data into string if needed
    """
    if isinstance(body, bytes) or isinstance(body, bytearray):
        return body
    elif isinstance(body, str):
        return bytes(body, encoding='utf-8')
    else:
        raise TypeError(f'Cannot encode body of type {type(body).__name__}')


@expect((socket.timeout,
         ConnectionRefusedError,
         ConnectionError,
         ConnectionAbortedError,
         ConnectionResetError))
def request(url: str,
            headers: Headers = Headers(),
            method: Method = Method.GET,
            body: Union[bytes, bytearray, str] = b'',
            follow_redirects=True,
            timeout: Optional[float] = None
            ) -> Union[Response, Exception]:
    logger.debug(f'Requesting: {url}')

    # Parse given url
    proto, host, path, port = parse_url(url)
    first_line = f'{method} {path} HTTP/1.1\r\n'
    headers['Host'] = host

    # Construct request
    if body is not None:
        request_body = encode_body(body)
        headers.set_if_none('Content-Length', len(request_body))
        request_head = first_line + headers.to_str()
        request_bytes = request_head.encode('ascii') + request_body
    else:
        request_head = first_line + headers.to_str()
        request_bytes = request_head.encode('ascii')

    try:
        # Connecting to server
        sock = socket.create_connection((host, port), timeout=timeout)

        # SSL Wrapping for HTTPS addresses
        if proto == Protocol.HTTPS:
            sock = ssl.wrap_socket(sock)

        sock.sendall(request_bytes)

        # recving headers first
        response = b''
        while b'\r\n\r\n' not in response:
            response += sock.recv(512)

        r_headers_bytes, r_body_bytes = response.split(b'\r\n\r\n', maxsplit=1)

        response_headers = Headers.from_bytes(r_headers_bytes)

        # If headers have Content-Length recv body to the end
        body_length = response_headers.get('Content-Length', 0)
        while len(r_body_bytes) < body_length:
            r_body_bytes += sock.recv(512)

        response_obj = Response(url,
                                response[:response.find(b'\r\n')].decode(),
                                response_headers,
                                r_body_bytes)

        if 300 <= response_obj.status_code < 400 and follow_redirects:
            new_location = response_obj.headers.get("Location")
            logger.debug(f'Being redirected to: {new_location}')
            return spawn(request,
                         url=new_location,
                         method=method,
                         headers=headers,
                         body=body,
                         follow_redirects=follow_redirects).get()

        return response_obj
    except (socket.timeout, GreenletExit) as err:
        return err
    finally:
        with suppress(UnboundLocalError):
            sock.close()


def spawn_request(url: str,
                  headers: Headers = Headers(),
                  method: Method = Method.GET,
                  body: Union[bytes, bytearray, str] = b'',
                  follow_redirects=True,
                  timeout: Optional[float] = None
                  ) -> Greenlet:
    return spawn(
        request,
        url=url,
        headers=headers,
        method=method,
        body=body,
        follow_redirects=follow_redirects,
        timeout=timeout
        )
