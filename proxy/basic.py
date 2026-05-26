from enum import Enum
from typing import Dict, Optional, Tuple

from .parser import parse


class ProxyType(str, Enum):
    HTTP = 'http'
    SOCKS4 = 'socks4'
    SOCKS5 = 'socks5'
    SOCKS5h = 'socks5h'


class Proxy:
    def __init__(
        self,
        raw_proxy: str,
        proxy_type: ProxyType = ProxyType.HTTP,
        schema: Optional[str] = None,
    ) -> None:
        self.ip: str = ''
        self.port: str = ''
        self.username: str = ''
        self.password: str = ''
        self.type: ProxyType = proxy_type

        self.start_data: str = ''

        self.load(raw_proxy, schema=schema)

    _MASKED_PASSWORD = '***'

    def __str__(self) -> str:
        """Safe string for logs — password is masked.

        Use `full_url` / `aiohttp` / `requests` for the real proxy string with
        credentials.
        """
        if self.username or self.password:
            masked = self._MASKED_PASSWORD if self.password else ''
            return f'{self.type.value}://{self.username}:{masked}@{self.ip}:{self.port}'
        return f'{self.type.value}://{self.ip}:{self.port}'

    def __repr__(self) -> str:
        return f'Proxy({self})'

    def _identity(self) -> Tuple[ProxyType, str, str, str, str]:
        """Tuple of fields that define proxy equality and hash.

        Note: Proxy is mutable, so calling `load()` after putting an instance
        into a set/dict makes the hash inconsistent — the entry will be
        unreachable. Treat instances as values: build once, don't mutate.
        """
        return (self.type, self.ip, self.port, self.username, self.password)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Proxy):
            return NotImplemented
        return self._identity() == other._identity()

    def __hash__(self) -> int:
        return hash(self._identity())

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

    def load(self, proxy: str, schema: Optional[str] = None) -> None:
        self.start_data = proxy
        self.ip, self.port, self.username, self.password = parse(proxy, schema)

    def id(self) -> str:
        return f'{self.ip.replace(".", "")}{self.port}'
