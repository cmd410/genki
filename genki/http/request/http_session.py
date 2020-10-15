from typing import Optional, Union

from gevent import socket, ssl
from gevent.util import wrap_errors

from .request_builder import RequestBuilder
from ..constants import Protocol
from ..response import Response
from ..exceptions import network_exceptions


class HTTPSession:
    """Class responsible for connecting to servers and transmitting data

    request - Request builder object that will supply information for request.\n
    timeout - seconds till socket.timeout.\n
    chunk_size - how many bytes to read at a time.\n
    """

    def __init__(self,
                 request: RequestBuilder,
                 timeout: Optional[float] = 5,
                 chunk_size: Optional[int] = 1024
                 ):
        self.request = request
        self.timeout = timeout
        self.chunk_size = chunk_size

        self.conn: Optional[socket.socket] = None
        self.responce: Optional[Response] = None

    def _init_session(self):
        """Establish TCP connection to server
        """
        host, port = self.request.host, self.request.port
        self.conn = socket.create_connection((host, port))

        if self.request.protocol == Protocol.HTTPS:
            self.conn = ssl.wrap_socket(self.conn)

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
        try:
            self._init_session()

            self._send_data()
            self._read_response()

            self._end_session()
        except network_exceptions as err:
            return err

        return self.responce