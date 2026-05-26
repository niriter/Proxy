from enum import Enum

import requests
import aiohttp

from typing import Optional, Dict, Union


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
    def auth(self) -> Optional[aiohttp.BasicAuth]:
        if self.username or self.password:
            return aiohttp.BasicAuth(self.username, self.password)
        return None

    @property
    def one_line_proxy(self) -> str:
        if self.username or self.password:
            return f'{self.username}:{self.password}@{self.ip}:{self.port}'
        return f'{self.ip}:{self.port}'

    @property
    def requests(self) -> Dict[str, str]:
        return {'http': self.full_url, 'https': self.full_url}

    @property
    def aiohttp(self) -> Dict[str, Union[str, aiohttp.BasicAuth]]:
        data: Dict[str, Union[str, aiohttp.BasicAuth]] = {'proxy': self.url}
        if self.auth:
            data['proxy_auth'] = self.auth
        return data

    def load(self, proxy: str) -> None:
        self.start_data = proxy
        parsed = self.start_data.split(':')
        self.ip = parsed[0]
        self.port = parsed[1]
        if len(parsed) == 4:
            self.username = parsed[2]
            self.password = parsed[3]

    def is_work(self) -> bool:
        try:
            ip = requests.get('https://api.my-ip.io/ip', proxies=self.requests, timeout=2).text
            print(ip)
            if ip != self.ip:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def id(self) -> str:
        return f'{self.ip.replace(".", "")}{self.port}'
