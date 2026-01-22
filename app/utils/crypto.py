from __future__ import annotations

import hashlib
import secrets


def make_opaque_token(nbytes: int = 48) -> str:
    return secrets.token_urlsafe(nbytes)


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
