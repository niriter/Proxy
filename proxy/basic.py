from enum import Enum

import requests
import aiohttp

from typing import Optional, Dict


class ProxyType(Enum):
    HTTP = 'http'
    SOCKS4 = 'socks4'
    SOCKS5 = 'socks5h'


class Proxy:
    def __init__(self, raw_proxy: str, proxy_type: ProxyType = ProxyType.SOCKS5):
        self.ip = ''
        self.port = ''
        self.username = ''
        self.password = ''
        self.type = proxy_type

        self.start_data = ''

        self.load(raw_proxy)

    def __str__(self):
        if self.username or self.password:
            return f'{self.type.value}://{self.username}:{self.password}@{self.ip}:{self.port}'
        return f'{self.type.value}://{self.ip}:{self.port}'

    @property
    def url(self) -> str:
        return f'{self.type.value}://{self.ip}:{self.port}'

    @property
    def full_url(self) -> str:
        return f'{self.type.value}://{self.one_line_proxy}'

    @property
    def auth(self) -> Optional[aiohttp.BasicAuth]:
        if self.username or self.password:
            return aiohttp.BasicAuth(self.username, self.password)
        return None

    @property
    def one_line_proxy(self):
        if self.username or self.password:
            return f'{self.username}:{self.password}@{self.ip}:{self.port}'
        return f'{self.ip}:{self.port}'

    @property
    def requests(self):
        return {'http': self.full_url, 'https': self.full_url}

    @property
    def aiohttp(self) -> Dict[str, str]:
        data = {'proxy': self.url}
        if self.auth:
            data['proxy_auth'] = self.auth
        return data

    def load(self, proxy):
        self.start_data = proxy
        parsed = self.start_data.split(':')
        self.ip = parsed[0]
        self.port = parsed[1]
        if len(parsed) == 4:
            self.username = parsed[2]
            self.password = parsed[3]

    def is_work(self):
        try:
            ip = requests.get('https://api.my-ip.io/ip', proxies=self.requests, timeout=2).text
            print(ip)
            if ip != self.ip:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def id(self):
        return f'{self.ip.replace(".", "")}{self.port}'
