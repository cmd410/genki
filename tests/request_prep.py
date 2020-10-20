from unittest import TestCase
from itertools import product

from genki.http.request.util import parse_url, url_parse_result
from genki.http.request import RequestBuilder
from genki.http.constants import Protocol
from genki.http.exceptions import InvalidURL


def generate_url():
    protos = ('http', 'https', '')
    domains = (
        'example.com', '[2001:db8::]'
    )
    ports = (8080, 6204, '')
    usernames = ('username', '')
    passwords = ('password', '')
    paths = (
        '/',
        '/some/path'
    )
    queries = ('', '?param=value')

    for proto, user, password, host, port, path, query in \
            product(protos, usernames, passwords,
                    domains, ports, paths, queries):
        url = ''
        if proto:
            url = f'{proto}://'
            if not port:
                port = 443 if proto == 'https' else 80
        else:
            proto = 'http'
        if user:
            url += f'{user}'
            if password:
                url += f':{password}'
            url += '@'
        url += f'{host}'
        if port:
            url += f':{port}'
        url += f'{path}{query}'
        if not port:
            port = 443 if proto == 'https' else 80

        yield url, url_parse_result(
            Protocol(proto),
            host,
            path,
            port,
            user,
            password if user else '',
            query[1:])


class RequestPreparations(TestCase):
    def test_url(self):
        """Check that url parses correctly
        """
        cases = list(generate_url())

        for url, result in cases:
            with self.subTest(url=url):
                r = parse_url(url)
                self.assertEqual(r, result)

    def test_invalid_urls(self):
        """Make sure invalid urls will raise an error
        """
        invalid_cases = [
            'https://',
            '/',
            '',
            'example.com:',
            ':example.com',
            'http://example.com:',
            'http://:example.com'
        ]

        for url in invalid_cases:
            with self.subTest(url=url):
                self.assertRaises(InvalidURL, RequestBuilder, url)

    def test_to_bytes(self):
        """Test that request converts to bytes correctly
        """
        s = 'GET {path} HTTP/1.1\r\nHost: {host}\r\n'

        hosts = [
            'example.com',
            'http://example.com',
            'https://example.com',
            'http://example.com:8080'
        ]

        paths = [
            '/',
            '/some/path'
        ]

        for host, path in product(hosts, paths):
            url = host + path
            with self.subTest(url=url):
                req = RequestBuilder(url)
                req.set_header('Connection', 'close')
                req.append_body('Hello world!')

                req_body = s.format(host=hosts[0], path=path)
                self.assertEqual(req.to_bytes(), (
                    ''.join(
                        [
                            req_body,
                            'Connection: close\r\n',
                            f'Content-Length: {len(req.body)}',
                            '\r\n\r\n',
                            'Hello world!'
                        ]
                    ).encode()))
                self.assertEqual(req.headers['Content-Length'], len('Hello world!'))
