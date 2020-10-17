from enum import Enum


class Method(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    CONNECT = 'CONNECT'
    TRACE = 'TRACE'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'
    HEAD = 'HEAD'
