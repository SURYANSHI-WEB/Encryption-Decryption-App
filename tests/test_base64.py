"""Unit tests for Base64 encoding/decoding implementation.

Tests encoding, decoding, and error handling for invalid Base64 input.
"""

import pytest

from src.ciphers import base64_mod


def test_round_trip():
    """Test that encoding followed by decoding returns original text.
    
    This is a critical test - Base64 should be perfectly reversible.
    Encodes a string, then decodes it, and verifies the result matches the original.
    """
    text = "Hello Base64!"
    enc = base64_mod.encode_base64(text)
    assert base64_mod.decode_base64(enc) == text


def test_invalid_decode():
    """Test that invalid Base64 input raises ValueError.
    
    Base64 decoding should fail gracefully with a clear error message
    when given invalid Base64 strings (e.g., containing invalid characters).
    """
    with pytest.raises(ValueError):
        base64_mod.decode_base64("not-valid@@@")


