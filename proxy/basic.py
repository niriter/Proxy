from enum import Enum

from typing import Dict


class ProxyType(str, Enum):
    HTTP = 'http'
    SOCKS4 = 'socks4'
    SOCKS5 = 'socks5'
    SOCKS5h = 'socks5h'


class Proxy:
    def __init__(self, raw_proxy: str, proxy_type: ProxyType = ProxyType.HTTP) -> None:
        self.ip: str = ''
        self.port: str = ''
        self.username: str = ''
        self.password: str = ''
        self.type: ProxyType = proxy_type

        self.start_data: str = ''

        self.load(raw_proxy)

    def __str__(self) -> str:
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
    def one_line_proxy(self) -> str:
        if self.username or self.password:
            return f'{self.username}:{self.password}@{self.ip}:{self.port}'
        return f'{self.ip}:{self.port}'

    @property
    def requests(self) -> Dict[str, str]:
        return {'http': self.full_url, 'https': self.full_url}

    @property
    def aiohttp(self) -> Dict[str, str]:
        return {'proxy': self.full_url}

    def load(self, proxy: str) -> None:
        self.start_data = proxy
        parsed = self.start_data.split(':')
        self.ip = parsed[0]
        self.port = parsed[1]
        if len(parsed) == 4:
            self.username = parsed[2]
            self.password = parsed[3]

    def id(self) -> str:
        return f'{self.ip.replace(".", "")}{self.port}'
