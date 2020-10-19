from typing import Union, Optional, Tuple, Mapping
from json import dumps
from logging import getLogger
from functools import wraps

from gevent import spawn

from .async_request import AsyncRequest
from .http import Headers, Method, HTTPSession, RequestBuilder

logger = getLogger('genki')


def prepare_data(data) -> Tuple[Optional[Union[str, bytes]], bool]:
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
                    headers: Union[Headers, Mapping] = Headers(),
                    timeout: Optional[float] = None,
                    follow_redirects: bool = True,
                    redirects_limit: int = 5
                    ):
            """A generic http request function reused for every method
            """
            data, is_json = prepare_data(data)

            builder = RequestBuilder(
                        url=url,
                        headers=headers,
                        body=data,
                        method=method)

            if is_json:
                builder.headers.set_if_none(
                    'Content-Type',
                    'application/json; charset=UTF-8'
                )

            session = HTTPSession(
                builder,
                timeout=timeout,
                follow_redirects=follow_redirects,
                redirects_limit=redirects_limit
            )
            return AsyncRequest(
                spawn(session.perform)
                )
        return wrapper
    return decorator


@request_method(Method.GET)
def get(url,
        data=None,
        params=None,
        headers: Union[Headers, Mapping] = Headers(),
        timeout: Optional[float] = None,
        follow_redirects: bool = True,
        redirects_limit: int = 5
        ) -> AsyncRequest:
    pass


@request_method(Method.POST)
def post(url,
         data=None,
         params=None,
         headers: Union[Headers, Mapping] = Headers(),
         timeout: Optional[float] = None,
         follow_redirects: bool = True,
         redirects_limit: int = 5
         ) -> AsyncRequest:
    pass


@request_method(Method.PATCH)
def patch(url,
          data=None,
          params=None,
          headers: Union[Headers, Mapping] = Headers(),
          timeout: Optional[float] = None,
          follow_redirects: bool = True,
          redirects_limit: int = 5
          ) -> AsyncRequest:
    pass


@request_method(Method.PUT)
def put(url,
        data=None,
        params=None,
        headers: Union[Headers, Mapping] = Headers(),
        timeout: Optional[float] = None,
        follow_redirects: bool = True,
        redirects_limit: int = 5
        ) -> AsyncRequest:
    pass


@request_method(Method.DELETE)
def delete(url,
           data=None,
           params=None,
           headers: Union[Headers, Mapping] = Headers(),
           timeout: Optional[float] = None,
           follow_redirects: bool = True,
           redirects_limit: int = 5
           ) -> AsyncRequest:
    pass


@request_method(Method.CONNECT)
def connect(url,
            data=None,
            params=None,
            headers: Union[Headers, Mapping] = Headers(),
            timeout: Optional[float] = None,
            follow_redirects: bool = True,
            redirects_limit: int = 5
            ) -> AsyncRequest:
    pass


@request_method(Method.OPTIONS)
def options(url,
            data=None,
            params=None,
            headers: Union[Headers, Mapping] = Headers(),
            timeout: Optional[float] = None,
            follow_redirects: bool = True,
            redirects_limit: int = 5
            ) -> AsyncRequest:
    pass


@request_method(Method.TRACE)
def trace(url,
          data=None,
          params=None,
          headers: Union[Headers, Mapping] = Headers(),
          timeout: Optional[float] = None,
          follow_redirects: bool = True,
          redirects_limit: int = 5
          ) -> AsyncRequest:
    pass


@request_method(Method.HEAD)
def head(url,
         data=None,
         params=None,
         headers: Union[Headers, Mapping] = Headers(),
         timeout: Optional[float] = None,
         follow_redirects: bool = True,
         redirects_limit: int = 5
         ) -> AsyncRequest:
    pass
