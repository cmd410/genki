from unittest import TestCase
from itertools import product

from genki.http.url.parse import parse_url, url_parse_result
from genki.http.request import RequestBuilder
from genki.http.constants import Scheme
from genki.http.url.exceptions import InvalidURL


def generate_url():
    protos = ('http', 'https', '')
    domains = (
        'example.com', '[2001:db8::]', '127.0.0.1'
    )
    ports = (8080, 6204, '')
    usernames = ('username', '')
    passwords = ('password', '')
    paths = (
        '/',
        '/some/path'
    )
    queries = ('', '?param=value')
    fragments = ('', 'fragment')

    for proto, user, password, host, port, path, query, fragment in \
            product(protos, usernames, passwords,
                    domains, ports, paths, queries, fragments):
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
        if fragment:
            url += f'#{fragment}'
        if not port:
            port = 443 if proto == 'https' else 80

        yield url, url_parse_result(
            Scheme(proto),
            host,
            path,
            port,
            user,
            password if user else '',
            query[1:],
            fragment)


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
        s = 'GET {path} HTTP/1.1\r\n'

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
                if '://' in host:
                    host = host[host.find('://') + 3:]
                if ':' in host:
                    host = host[:host.find(':')]
                req_body = s.format(host=hosts[0], path=path)
                self.assertEqual(req.to_bytes(), (
                    ''.join(
                        [
                            req_body,
                            f'Host: {host}\r\n',
                            'Connection: close\r\n',
                            '\r\n',
                        ]
                    ).encode()))
