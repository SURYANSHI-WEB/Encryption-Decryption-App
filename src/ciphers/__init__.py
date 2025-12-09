"""Cipher modules package - exports encryption/decryption functions.

This package provides implementations of various cipher algorithms:
- Caesar cipher: Simple substitution cipher with shift-based encryption
- Base64: Encoding scheme for converting binary data to text format

All cipher functions are exported here for convenient importing.
"""

# Import Caesar cipher functions
from .caesar import decrypt_caesar, encrypt_caesar

# Import Base64 encoding/decoding functions
from .base64_mod import decode_base64, encode_base64

# Define public API - these are the functions users should import
__all__ = ["encrypt_caesar", "decrypt_caesar", "encode_base64", "decode_base64"]


