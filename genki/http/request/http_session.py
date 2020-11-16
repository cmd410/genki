from typing import Optional, Union

from gevent import socket, ssl, spawn

from .request_builder import RequestBuilder
from ..constants import Protocol
from ..response import Response
from ..exceptions import network_exceptions


class HTTPSession:
    """Class responsible for connecting to servers and transmitting data

    request - Request builder object that
    will supply information for request.\n
    timeout - seconds till socket.timeout.\n
    chunk_size - how many bytes to read at a time.\n
    follow_redirects - should redirects be followed
    """

    __slots__ = (
        'request',
        'timeout',
        'chunk_size',
        'conn',
        'responce',
        'follow_redirects',
        'redirects_limit'
    )

    def __init__(self,
                 request: RequestBuilder,
                 timeout: Optional[float] = 5,
                 chunk_size: Optional[int] = 1024,
                 follow_redirects: bool = True,
                 redirects_limit: int = 5
                 ):
        self.request = request
        self.timeout = timeout
        self.chunk_size = chunk_size
        self.follow_redirects = follow_redirects
        self.redirects_limit = redirects_limit

        self.conn: Optional[socket.socket] = None
        self.responce: Optional[Response] = None

    def _init_session(self):
        """Establish TCP connection to server
        """
        host, port = self.request.url.host, self.request.url.port
        self.conn = socket.create_connection(
            (host, port),
            timeout=self.timeout
            )
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
        if self.request.url.protocol == Protocol.HTTPS:
            self.conn = ctx.wrap_socket(self.conn, server_hostname=host)

        return self

    def _send_data(self):
        """Send request data to server
        """
        assert self.conn is not None

        data = self.request.to_bytes()

        self.conn.sendall(data)

    def _read_response(self):
        """Read response from server
        """
        assert self.conn is not None

        responce_bytes = b''

        # Read till headers end
        while b'\r\n\r\n' not in responce_bytes:
            responce_bytes += self.conn.recv(self.chunk_size)

        headers_bytes, body_bytes = \
            responce_bytes.split(b'\r\n\r\n', maxsplit=1)

        # Figure out how much data left
        body_length = 0
        for line in headers_bytes.split(b'\r\n'):
            if line.lower().startswith(b'content-length:'):
                body_length = int(
                    line.split(b':', maxsplit=1)[1]
                        .strip())
                break

        if body_length:
            # Read remaining body
            while len(body_bytes) < body_length:
                body_bytes += self.conn.recv(self.chunk_size)
        elif not responce_bytes.endswith(b'\r\n\r\n'):
            while True:
                new_data = self.conn.recv(self.chunk_size)
                if not new_data:
                    break
                body_bytes += new_data
        self.responce = Response(
            self.request,
            headers_bytes+b'\r\n\r\n'+body_bytes
        )

    def _end_session(self):
        """Close connection to server
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return self

    def perform(self) -> Union[Response, Exception]:
        """Perfrom HTTP request
        """
        try:
            self._init_session()

            self._send_data()
            self._read_response()
        except network_exceptions as err:
            return err
        finally:
            self._end_session()

        if 300 < self.responce.status_code < 400 \
                and self.follow_redirects:
            if self.redirects_limit:
                if len(self.request.redirect_chain) >= self.redirects_limit:
                    return self.responce

            self.request.redirect_to(
                self.responce.status_code,
                self.responce.headers['Location']
                )
            return spawn(self.perform).get()
        return self.responce
