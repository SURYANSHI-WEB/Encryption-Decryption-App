"""Unit tests for Caesar cipher implementation.

Tests encryption and decryption with various inputs including:
- Basic letter shifting
- Case preservation
- Punctuation handling
- Empty strings
- Non-letter characters
- Negative shifts
"""

import pytest

from src.ciphers import caesar


@pytest.mark.parametrize(
    "text,shift,expected",
    [
        ("abc", 2, "cde"),  # Basic forward shift
        ("Hello, World!", 3, "Khoor, Zruog!"),  # Mixed case with punctuation
        ("Hello, World!", -3, "Ebiil, Tloia!"),  # Negative shift (backward)
        ("", 5, ""),  # Empty string edge case
        ("123!", 10, "123!"),  # Non-letter characters preserved
    ],
)
def test_encrypt(text, shift, expected):
    """Test Caesar cipher encryption with various inputs.
    
    Verifies that encryption produces expected output for different
    text inputs, shift values, and edge cases.
    """
    assert caesar.encrypt_caesar(text, shift) == expected


@pytest.mark.parametrize(
    "cipher,shift,expected",
    [
        ("cde", 2, "abc"),  # Basic decryption
        ("Khoor, Zruog!", 3, "Hello, World!"),  # Decrypt with positive shift
        ("Ebiil, Tloia!", -3, "Hello, World!"),  # Decrypt with negative shift
        ("", 5, ""),  # Empty string edge case
        ("123!", 10, "123!"),  # Non-letter characters preserved
    ],
)
def test_decrypt(cipher, shift, expected):
    """Test Caesar cipher decryption with various inputs.
    
    Verifies that decryption correctly reverses encryption and produces
    the original plaintext for different ciphertexts and shift values.
    """
    assert caesar.decrypt_caesar(cipher, shift) == expected


