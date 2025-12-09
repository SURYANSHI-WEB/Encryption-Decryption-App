"""Command-line interface for encryption_decryption_tool."""

from __future__ import annotations

import os
import sys
from typing import Optional

import click

from src import __app_name__, __version__
from src.ciphers import base64_mod, caesar
from src.utils.io_helpers import read_text_file, write_text_file


def _read_input(value: str) -> str:
    """Helper function to read input from file or use as direct text.
    
    Checks if the input value is a file path that exists. If it exists,
    reads the file content; otherwise treats it as plain text input.
    """
    return read_text_file(value) if os.path.exists(value) else value


def _write_output(output_path: Optional[str], text: str) -> str:
    """Helper function to write output to file or print to console.
    
    If an output path is provided, saves the text to that file.
    Otherwise, prints the text to stdout and returns a status message.
    """
    if output_path:
        write_text_file(output_path, text)
        return f"Saved to {output_path}"
    click.echo(text)
    return "Printed to stdout"


@click.group(invoke_without_command=True)
@click.option("--gui", is_flag=True, help="Launch Tkinter GUI.")
@click.version_option(version=__version__, prog_name=__app_name__)
@click.pass_context
def cli(ctx: click.Context, gui: bool) -> None:
    """Main CLI entry point - handles GUI flag and shows help if no command given.
    
    If --gui flag is set, launches the Tkinter GUI interface.
    Otherwise, if no subcommand is provided, displays the help message.
    """
    if gui:
        # Import GUI module only when needed to avoid Tkinter dependency issues
        from src import gui as gui_module

        gui_module.launch_gui()
        ctx.exit(0)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option("--algo", type=click.Choice(["caesar", "base64"]), required=True)
@click.option("--in", "input_value", required=True, help="Plaintext or path to file.")
@click.option("--shift", type=int, default=3, help="Shift (Caesar).")
@click.option("--out", "output_path", help="Optional output file path.")
def encrypt(algo: str, input_value: str, shift: int, output_path: str) -> None:
    """Encrypt command - encrypts text using the specified algorithm.
    
    Supports Caesar cipher (requires --shift) and Base64 encoding.
    Input can be direct text or a file path. Output can be saved to file or printed.
    """
    # Read input (from file or direct text)
    text = _read_input(input_value)
    result = ""

    # Apply encryption based on selected algorithm
    if algo == "caesar":
        result = caesar.encrypt_caesar(text, shift)
    elif algo == "base64":
        result = base64_mod.encode_base64(text)

    # Write output and show success message
    location = _write_output(output_path, result)
    click.echo(f"Encrypted successfully ({algo}). {location}")


@cli.command()
@click.option("--algo", type=click.Choice(["caesar", "base64"]), required=True)
@click.option("--in", "input_value", required=True, help="Ciphertext or path to file.")
@click.option("--shift", type=int, default=3, help="Shift (Caesar).")
@click.option("--out", "output_path", help="Optional output file path.")
def decrypt(
    algo: str,
    input_value: str,
    shift: int,
    output_path: str,
) -> None:
    """Decrypt command - decrypts text using the specified algorithm.
    
    Supports Caesar cipher (requires --shift) and Base64 decoding.
    Input can be direct text or a file path. Output can be saved to file or printed.
    Handles Base64 decode errors gracefully with clear error messages.
    """
    # Read input (from file or direct text)
    text = _read_input(input_value)
    result = ""

    # Apply decryption based on selected algorithm
    if algo == "caesar":
        result = caesar.decrypt_caesar(text, shift)
    elif algo == "base64":
        try:
            result = base64_mod.decode_base64(text)
        except ValueError as exc:
            # Base64 decode can fail if input is invalid - show error and exit
            click.echo(f"Error: {exc}")
            sys.exit(1)

    # Write output and show success message
    location = _write_output(output_path, result)
    click.echo(f"Decrypted successfully ({algo}). {location}")


@cli.command()
def examples() -> None:
    """Print quick usage examples and show path to sample messages file.
    
    Displays copy-paste ready command examples for common use cases.
    Also shows the location of the sample_messages.txt file for testing.
    """
    click.echo("Examples:")
    click.echo('  python -m src.cli encrypt --algo caesar --in "Hello" --shift 3')
    click.echo('  python -m src.cli decrypt --algo base64 --in "SGVsbG8="')
    click.echo("  python -m src.cli --gui")
    # Build path to samples directory relative to this file
    sample_path = os.path.join(os.path.dirname(__file__), "..", "samples", "sample_messages.txt")
    click.echo(f"Sample messages: {sample_path}")


def main() -> None:
    """Entry point for running CLI as a module."""
    cli()


if __name__ == "__main__":
    main()


