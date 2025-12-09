"""IO helper functions for reading/writing text files and safe user input.

Provides utility functions for file operations with UTF-8 encoding and
error handling for user input scenarios.
"""

from __future__ import annotations

import os
from typing import Union


def read_text_file(path: Union[str, os.PathLike]) -> str:
    """Read UTF-8 encoded text from a file.
    
    Opens the file in read mode with UTF-8 encoding and returns its contents.
    Raises FileNotFoundError if the file doesn't exist.
    
    Args:
        path: Path to the text file to read
    
    Returns:
        Contents of the file as a string
    
    Raises:
        FileNotFoundError: if the file doesn't exist
        UnicodeDecodeError: if file contains invalid UTF-8
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: Union[str, os.PathLike], text: str) -> None:
    """Write UTF-8 encoded text to a file, creating parent directories if needed.
    
    Creates any necessary parent directories, then writes the text to the file.
    Overwrites existing files if they exist.
    
    Args:
        path: Path where the file should be written
        text: Text content to write to the file
    
    Example:
        write_text_file("output/result.txt", "Hello World")
    """
    # Create parent directories if they don't exist (e.g., "output/" folder)
    # Use "." if path has no directory component
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    # Write text with UTF-8 encoding
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def safe_input(prompt: str) -> str:
    """Safe input wrapper that handles EOF errors gracefully.
    
    Wraps Python's input() function to catch EOFError exceptions that can occur
    when running in non-interactive environments (IDEs, scripts, etc.).
    
    Args:
        prompt: Prompt string to display to user
    
    Returns:
        User input string, or empty string if EOFError occurs
    """
    try:
        return input(prompt)
    except EOFError:
        # Return empty string instead of crashing when input is unavailable
        return ""


