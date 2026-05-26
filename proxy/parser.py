import re
from typing import Optional, Tuple
from urllib.parse import urlsplit


_FIELD_ALIASES = {
    'host': 'host', 'ip': 'host',
    'port': 'port',
    'user': 'user', 'username': 'user',
    'pass': 'pass', 'password': 'pass',
}


def parse_with_schema(s: str, schema: str) -> Tuple[str, str, str, str]:
    """Parse `s` according to explicit `schema` like 'host:port:user:pass'.

    Separator is whatever non-alphanumeric character appears in the schema
    (e.g. ',' for schema='host,port,user,pass').
    """
    sep_match = re.search(r'[^a-zA-Z0-9_]', schema)
    if not sep_match:
        raise ValueError(f"Schema has no separator: {schema!r}")
    sep = sep_match.group(0)

    raw_fields = schema.split(sep)
    fields = []
    for raw in raw_fields:
        if raw not in _FIELD_ALIASES:
            raise ValueError(
                f"Unknown schema field {raw!r}. "
                f"Allowed: {sorted(set(_FIELD_ALIASES))}"
            )
        fields.append(_FIELD_ALIASES[raw])

    if len(set(fields)) != len(fields):
        raise ValueError(f"Duplicate fields in schema: {schema!r}")

    parts = s.split(sep)
    if len(parts) != len(fields):
        raise ValueError(
            f"Schema {schema!r} expects {len(fields)} parts separated by {sep!r}, "
            f"got {len(parts)} in {s!r}"
        )

    mapping = dict(zip(fields, parts))
    return (
        mapping.get('host', ''),
        mapping.get('port', ''),
        mapping.get('user', ''),
        mapping.get('pass', ''),
    )


def parse_url(s: str) -> Tuple[str, str, str, str]:
    """Parse URL form like 'http://user:pass@host:port'."""
    u = urlsplit(s)
    host = u.hostname
    port = u.port
    if not host:
        raise ValueError(f"Bad proxy URL (no host): {s!r}")
    if port is None:
        raise ValueError(f"Bad proxy URL (no port): {s!r}")
    return host, str(port), u.username or '', u.password or ''


def parse_legacy(s: str) -> Tuple[str, str, str, str]:
    """Parse legacy form 'host:port' or 'host:port:user:pass'."""
    parts = s.split(':')
    if len(parts) == 2:
        host, port, user, pwd = parts[0], parts[1], '', ''
    elif len(parts) == 4:
        host, port, user, pwd = parts[0], parts[1], parts[2], parts[3]
    else:
        raise ValueError(
            f"Legacy form must be 'host:port' or 'host:port:user:pass', "
            f"got {len(parts)} parts in {s!r}"
        )

    if not host or not port:
        raise ValueError(f"Empty host or port in {s!r}")
    return host, port, user, pwd


def parse(s: str, schema: Optional[str] = None) -> Tuple[str, str, str, str]:
    """Parse a proxy string. Returns (host, port, user, pass).

    Priority:
      1. If `schema` is given — use it strictly.
      2. If '://' in `s` — parse as URL.
      3. If '@' in `s` (URL without scheme) — prepend 'http://' and parse as URL.
      4. Fallback — legacy 'host:port[:user:pass]'.
    """
    if not s:
        raise ValueError("Empty proxy string")

    if schema is not None:
        return parse_with_schema(s, schema)

    if '://' in s:
        return parse_url(s)

    if '@' in s:
        return parse_url(f'http://{s}')

    return parse_legacy(s)
