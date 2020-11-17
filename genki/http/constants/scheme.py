from enum import Enum

class Scheme(str, Enum):
    HTTPS = 'https'
    HTTP = 'http'
