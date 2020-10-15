from typing import Optional, Union
from contextlib import suppress

from .headers import Headers
from .constants import StatusCode
from .request import RequestBuilder


class Response:

    __slots__ = (
        'status_code',
        'request',
        'raw_bytes',
        'headers',
        '_body'
    )

    def __init__(self, request: RequestBuilder, raw_bytes: bytes):
        self.request = request
        self.raw_bytes = raw_bytes

        headers_bytes, self._body = raw_bytes.split(b'\r\n\r\n', maxsplit=1)
        self.status_code = \
            StatusCode(
                int(headers_bytes[
                    :headers_bytes.find(b'\r\n')
                    ].split(b' ', maxsplit=2)[1].decode())
                )
        self.headers = Headers.from_bytes(headers_bytes)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.status_code})'

    @property
    def raw_body(self) -> bytes:
        """Returns raw bytes of HTTP body as recieved from server
        """
        return self._body

    @property
    def body(self) -> Union[bytes, str]:
        """Retruns HTTP body, decoded when possibe
        """
        if self.content_type.startswith('text/'):
            charset = self.charset

            with suppress(ValueError):
                if charset:
                    return self._body.decode(charset)
                else:
                    return self._body.decode('utf-8')
        return self._body

    @property
    def content_type(self) -> str:
        return self.headers.get('Content-Type', '')

    @property
    def is_html(self) -> bool:
        return self.content_type.strip().startswith('text/html')

    @property
    def charset(self) -> Optional[str]:
        content_type = self.content_type
        if content_type is None:
            return None
        if ';' not in content_type:
            return None
        *_, charset = content_type.split(';')
        return charset.split('=')[-1].lower()
