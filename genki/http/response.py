from typing import Optional, Union

from .headers import Headers
from .constants import Code


class Response:

    __slots__ = (
        'source',
        'http_version',
        'status_code',
        'headers',
        '_body'
    )

    def __init__(self,
                 source: str,
                 status_line: str,
                 headers: Headers,
                 body: Union[bytes,]):
        self.http_version, status_code_str, *_ = status_line.split()
        self.status_code = Code(int(status_code_str))
        self.source = source
        self.headers = headers
        self._body = body

    def __repr__(self):
        return f'{self.__class__.__name__}({self.status_code})'

    @property
    def body(self) -> Union[bytes, str]:
        charset = self.charset
        if charset:
            return self._body.decode(charset)
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
