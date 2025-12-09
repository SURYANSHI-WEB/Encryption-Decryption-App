"""Lightweight crypto helper utilities.

Provides PBKDF2 key derivation and PKCS7 padding helpers that are shared
between AES implementations. These functions rely only on the Python stdlib
for portability and clarity.
"""

from __future__ import annotations

import hashlib
from typing import Final

# PBKDF2 iteration count - higher is more secure but slower
# 100k is a reasonable balance for academic/demo use
PBKDF2_ITERATIONS: Final[int] = 100_000

# AES-256 requires a 32-byte (256-bit) key
KEY_LEN: Final[int] = 32  # 256-bit AES key size

# AES block size is always 16 bytes (128 bits)
BLOCK_SIZE: Final[int] = 16  # AES block size in bytes


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit encryption key from a password and salt using PBKDF2.

    PBKDF2 (Password-Based Key Derivation Function 2) is a key derivation function
    that makes password-based encryption more secure by adding computational cost.
    It uses HMAC-SHA256 as the underlying pseudorandom function.
    
    Args:
        password: User-provided password string
        salt: Random salt bytes (should be unique per encryption)
    
    Returns:
        32-byte (256-bit) key derived from password and salt
    
    Note:
        The iteration count is set to ~100k for a balance between security and
        speed for academic/demo use; increase for production settings (e.g., 600k+).
    """
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS, dklen=KEY_LEN
    )


def pad(data: bytes) -> bytes:
    """Apply PKCS7 padding to align data to AES block size.
    
    AES encryption requires data to be a multiple of the block size (16 bytes).
    PKCS7 padding adds bytes at the end, where each padding byte equals the
    number of padding bytes added. This allows unambiguous removal during decryption.
    
    Args:
        data: Raw bytes to pad
    
    Returns:
        Padded bytes (length is multiple of BLOCK_SIZE)
    
    Example:
        If data is 10 bytes, adds 6 bytes of value 0x06 to make 16 bytes total.
    """
    # Calculate how many bytes needed to reach next block boundary
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    # Append padding bytes (each byte equals pad_len)
    return data + bytes([pad_len] * pad_len)


def unpad(data: bytes) -> bytes:
    """Remove PKCS7 padding from decrypted data.
    
    Reads the last byte to determine padding length, verifies padding is valid,
    then removes the padding bytes to return original data.
    
    Args:
        data: Padded bytes (must be multiple of BLOCK_SIZE)
    
    Returns:
        Original unpadded bytes
    
    Raises:
        ValueError: if data is empty, padding length is invalid, or padding bytes are incorrect
    
    Example:
        If last byte is 0x06, removes last 6 bytes and returns the rest.
    """
    if not data:
        raise ValueError("Cannot unpad empty data")
    
    # Last byte tells us how many padding bytes were added
    pad_len = data[-1]
    
    # Validate padding length is within expected range
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding length")
    
    # Verify all padding bytes match the expected value
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid PKCS7 padding bytes")
    
    # Return data without padding
    return data[:-pad_len]


