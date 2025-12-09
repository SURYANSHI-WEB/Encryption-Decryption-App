"""Base64 encoding/decoding wrapper using pybase64 library.

Base64 is an encoding scheme that converts binary data into ASCII text format.
It's commonly used for encoding data in URLs, emails, and other text-based protocols.
Note: Base64 is encoding, not encryption - it's easily reversible and not secure.
"""

from __future__ import annotations

import pybase64


def encode_base64(plaintext: str) -> str:
    """Encode plaintext string to Base64-encoded string.
    
    Converts the input text to UTF-8 bytes, then encodes those bytes to Base64,
    and returns the result as a UTF-8 string.
    
    Args:
        plaintext: Text string to encode
    
    Returns:
        Base64-encoded string (safe for text transmission)
    
    Example:
        >>> encode_base64("Hello")
        'SGVsbG8='
    """
    # Convert string to UTF-8 bytes, encode to Base64, then decode back to string
    return pybase64.b64encode(plaintext.encode("utf-8")).decode("utf-8")


def decode_base64(b64text: str) -> str:
    """Decode Base64-encoded string back to original text.

    Takes a Base64-encoded string, decodes it to bytes, then converts to UTF-8 text.
    
    Args:
        b64text: Base64-encoded string to decode
    
    Returns:
        Decoded plaintext string
    
    Raises:
        ValueError: if the input is not valid Base64 format
    
    Example:
        >>> decode_base64("SGVsbG8=")
        'Hello'
    """
    try:
        # Decode Base64 to bytes, then decode bytes to UTF-8 string
        return pybase64.b64decode(b64text).decode("utf-8")
    except Exception as exc:  # noqa: BLE001 broad to rewrap
        # Re-raise with clearer error message for invalid Base64 input
        raise ValueError("Invalid Base64 input") from exc


