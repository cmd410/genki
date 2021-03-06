from typing import Optional, Union
from contextlib import suppress

from chardet import detect
from chardet.universaldetector import UniversalDetector

from .headers import Headers
from .constants import StatusCode
from .request import RequestBuilder


class Response:
    """Class represents reponse from server
    """

    __slots__ = (
        'status_code',
        'request',
        'raw_bytes',
        'headers',
        '_body'
    )

    def __init__(self,
                 request: RequestBuilder,
                 raw_bytes: bytes,
                 headers: Optional[Headers] = None):
        self.request = request
        self.raw_bytes = raw_bytes

        headers_bytes, self._body = raw_bytes.split(b'\r\n\r\n', maxsplit=1)
        self.status_code = \
            StatusCode(
                int(headers_bytes[
                    :headers_bytes.find(b'\r\n')
                    ].split(b' ', maxsplit=2)[1].decode())
                )
        if headers is None:
            self.headers = Headers.from_bytes(headers_bytes)
        else:
            self.headers = headers

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
            if charset is not None:
                with suppress(ValueError):
                    if charset:
                        return self._body.decode(charset)
                    else:
                        return self._body.decode('utf-8')
            else:
                # detect small content
                if len(self._body) < 1024 * 10:
                    chardet_result = detect(self._body)
                    if round(chardet_result['confidence']):
                        return self._body.decode(chardet_result['encoding'])
                else:
                    # detect large content
                    detector = UniversalDetector()
                    for i in range(0, len(self._body), 1024):
                        detector.feed(self._body[i:i+1024])
                        if detector.done:
                            break

                    chardet_result = detector.close()
                    if round(chardet_result['confidence']):
                        return self._body.decode(chardet_result['encoding'])
        return self._body

    @property
    def content_type(self) -> str:
        """Shorthand for getting Content-Type headers
        """
        return self.headers.get('Content-Type', '')

    @property
    def is_html(self) -> bool:
        """True if Content-Type is \"text/html\"
        """
        return self.content_type.strip().startswith('text/html')

    @property
    def charset(self) -> Optional[str]:
        """Tries to read body charset
        from Content-Type header and returns it.
        If no charset found in headers, returns None
        """
        content_type = self.content_type
        if content_type is None:
            return None
        if ';' not in content_type:
            return None
        *_, charset = content_type.split(';')
        return charset.split('=')[-1].lower()
