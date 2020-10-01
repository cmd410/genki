from typing import Union, Optional, Tuple
from json import dumps
from logging import getLogger
from functools import wraps

from .async_request import AsyncRequest
from .http import spawn_request, Headers, Method

logger = getLogger('genki')


def prepare_data(data) -> Optional[Tuple[Union[str, bytes], bool]]:
    """Jsonify data when possible

    returns new_data and boolean result of successfull encoding
    """
    if data is None:
        return None, False
    success = False
    if not (isinstance(data, bytes) or
            isinstance(data, bytearray) or
            isinstance(data, str)):
        try:
            data = dumps(data)
            success = True
        except TypeError:
            logger.warning(
                'Data given is not bytes, '
                + 'nor string, and can\'t be jsonified. '
                + 'Something might just go wrong. '
                + f'Data type is {type(data)}'
                )
    return data, success


def request_method(method: Method):
    def decorator(func):
        @wraps(func)
        def wrapper(url,
                    data=None,
                    params=None,
                    headers: Headers = Headers(),
                    timeout: Optional[float] = None):
            """A generic http request function reused for every method
            """

            data, is_json = prepare_data(data)
            if is_json:
                headers.set_if_none(
                    'Content-Type',
                    'application/json; charset=UTF-8'
                )
            req = AsyncRequest(
                spawn_request(
                    url=url,
                    body=data,
                    method=method,
                    timeout=timeout
                )
            )
            return req
        return wrapper
    return decorator


@request_method(Method.GET)
def get(url,
        data=None,
        params=None,
        headers: Headers = Headers(),
        timeout: Optional[float] = None
        ) -> AsyncRequest:
    pass


@request_method(Method.POST)
def post(url,
         data=None,
         params=None,
         headers: Headers = Headers(),
         timeout: Optional[float] = None) -> AsyncRequest:
    pass


@request_method(Method.PATCH)
def patch(url,
          data=None,
          params=None,
          headers: Headers = Headers(),
          timeout: Optional[float] = None) -> AsyncRequest:
    pass


@request_method(Method.PUT)
def put(url,
        data=None,
        params=None,
        headers: Headers = Headers(),
        timeout: Optional[float] = None) -> AsyncRequest:
    pass


@request_method(Method.DELETE)
def delete(url,
           data=None,
           params=None,
           headers: Headers = Headers(),
           timeout: Optional[float] = None) -> AsyncRequest:
    pass


@request_method(Method.CONNECT)
def connect(url,
            data=None,
            params=None,
            headers: Headers = Headers(),
            timeout: Optional[float] = None) -> AsyncRequest:
    pass


@request_method(Method.OPTIONS)
def options(url,
            data=None,
            params=None,
            headers: Headers = Headers(),
            timeout: Optional[float] = None) -> AsyncRequest:
    pass


@request_method(Method.TRACE)
def trace(url,
          data=None,
          params=None,
          headers: Headers = Headers(),
          timeout: Optional[float] = None) -> AsyncRequest:
    pass


@request_method(Method.HEAD)
def head(url,
         data=None,
         params=None,
         headers: Headers = Headers(),
         timeout: Optional[float] = None) -> AsyncRequest:
    pass
