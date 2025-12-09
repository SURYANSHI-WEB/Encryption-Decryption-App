"""AES functionality removed per user request.

This module remains as a stub to avoid import errors; all calls will raise.
"""

from __future__ import annotations

AES_AVAILABLE = False


def encrypt_aes(*_: object, **__: object) -> None:  # pragma: no cover - stub
    raise RuntimeError("AES support removed in this build.")


def decrypt_aes(*_: object, **__: object) -> None:  # pragma: no cover - stub
    raise RuntimeError("AES support removed in this build.")


