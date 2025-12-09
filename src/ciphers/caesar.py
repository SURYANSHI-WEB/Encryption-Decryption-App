"""Caesar cipher implementation with simple doctests.

The Caesar cipher is a substitution cipher where each letter in the plaintext
is shifted a certain number of places down the alphabet. Non-letter characters
(punctuation, digits, spaces) are preserved unchanged.
"""

from __future__ import annotations

import string

# Standard English alphabet (lowercase) - used as base for shifting
ALPHABET = string.ascii_lowercase


def _shift_char(ch: str, shift: int) -> str:
    """Internal helper to shift a single character by the given amount.
    
    Args:
        ch: Single character to shift
        shift: Number of positions to shift (can be negative for decryption)
    
    Returns:
        Shifted character, or original character if it's not a letter
    """
    # If character is not a letter, return it unchanged
    if ch.lower() not in ALPHABET:
        return ch
    
    # Choose uppercase or lowercase alphabet based on input character case
    base = ALPHABET if ch.islower() else ALPHABET.upper()
    
    # Find current position in alphabet
    idx = base.index(ch)
    
    # Shift position, wrapping around using modulo 26 (alphabet size)
    shifted = (idx + shift) % 26
    
    # Return character at new position
    return base[shifted]


def encrypt_caesar(plaintext: str, shift: int) -> str:
    """Encrypt plaintext with a Caesar shift.

    Shifts each letter forward by the specified number of positions.
    Non-letter characters (punctuation, digits, spaces) are preserved.
    
    Args:
        plaintext: Text to encrypt
        shift: Number of positions to shift (can be any integer, will wrap around)
    
    Returns:
        Encrypted ciphertext
    
    Examples:
        >>> encrypt_caesar("abc", 2)
        'cde'
        >>> encrypt_caesar("Hello, World!", 3)
        'Khoor, Zruog!'
    """
    # Normalize shift to 0-25 range (handles negative and large shifts)
    norm_shift = shift % 26
    # Apply shift to each character and join results
    return "".join(_shift_char(ch, norm_shift) for ch in plaintext)


def decrypt_caesar(ciphertext: str, shift: int) -> str:
    """Decrypt Caesar-shifted ciphertext.

    Shifts each letter backward by the specified number of positions.
    This is the inverse operation of encrypt_caesar.
    
    Args:
        ciphertext: Encrypted text to decrypt
        shift: Number of positions the text was shifted (same as encryption shift)
    
    Returns:
        Decrypted plaintext
    
    Examples:
        >>> decrypt_caesar("cde", 2)
        'abc'
        >>> decrypt_caesar("Khoor, Zruog!", 3)
        'Hello, World!'
    """
    # Normalize shift to 0-25 range
    norm_shift = shift % 26
    # Apply negative shift (backward) to each character and join results
    return "".join(_shift_char(ch, -norm_shift) for ch in ciphertext)


