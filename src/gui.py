"""Minimal Tkinter GUI wrapper for encryption/decryption operations."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.ciphers import base64_mod, caesar


def launch_gui() -> None:
    """Launch the main GUI window with encryption/decryption interface.
    
    Creates a Tkinter window with:
    - Algorithm selection dropdown (Caesar or Base64)
    - Input text field
    - Algorithm-specific fields (shift for Caesar)
    - Encrypt/Decrypt buttons
    - Result display area
    """
    # Initialize main window
    app = tk.Tk()
    app.title("Encryption Decryption Tool")
    app.geometry("520x420")

    # Create Tkinter variables to hold user input and results
    algo_var = tk.StringVar(value="caesar")  # Selected algorithm
    text_var = tk.StringVar()  # Input text
    shift_var = tk.IntVar(value=3)  # Caesar shift value
    result_var = tk.StringVar()  # Result output

    def update_fields(*_: object) -> None:
        """Dynamically show/hide fields based on selected algorithm.
        
        When algorithm changes, hides all optional fields first, then shows
        only the fields relevant to the selected algorithm (e.g., shift for Caesar).
        """
        # Hide all optional fields first
        shift_label.grid_forget()
        shift_entry.grid_forget()

        # Show fields based on selected algorithm
        if algo_var.get() == "caesar":
            # Caesar cipher needs shift value
            shift_label.grid(row=2, column=0, sticky="w", padx=4, pady=4)
            shift_entry.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

    def do_encrypt() -> None:
        """Encrypt button handler - performs encryption based on selected algorithm.
        
        Reads input text and algorithm selection, calls appropriate encryption function,
        and displays result in the result area. Handles errors gracefully.
        """
        text = text_var.get()
        algo = algo_var.get()
        try:
            # Route to appropriate encryption function
            if algo == "caesar":
                result = caesar.encrypt_caesar(text, shift_var.get())
            elif algo == "base64":
                result = base64_mod.encode_base64(text)
            else:
                result = "Unsupported algorithm"
            result_var.set(result)
        except Exception as exc:  # noqa: BLE001
            # Show error message in result area if encryption fails
            result_var.set(f"Error: {exc}")

    def do_decrypt() -> None:
        """Decrypt button handler - performs decryption based on selected algorithm.
        
        Reads input text and algorithm selection, calls appropriate decryption function,
        and displays result in the result area. Handles errors gracefully.
        """
        text = text_var.get()
        algo = algo_var.get()
        try:
            # Route to appropriate decryption function
            if algo == "caesar":
                result = caesar.decrypt_caesar(text, shift_var.get())
            elif algo == "base64":
                result = base64_mod.decode_base64(text)
            else:
                result = "Unsupported algorithm"
            result_var.set(result)
        except Exception as exc:  # noqa: BLE001
            # Show error message in result area if decryption fails
            result_var.set(f"Error: {exc}")

    # === GUI Layout Setup ===
    
    # Algorithm selection dropdown
    tk.Label(app, text="Algorithm:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
    algo_menu = ttk.Combobox(
        app, textvariable=algo_var, values=["caesar", "base64"], state="readonly"
    )
    algo_menu.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
    # Update fields when algorithm selection changes
    algo_menu.bind("<<ComboboxSelected>>", update_fields)

    # Input text field
    tk.Label(app, text="Input text:").grid(row=1, column=0, sticky="nw", padx=4, pady=4)
    text_entry = tk.Entry(app, textvariable=text_var, width=60)
    text_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

    # Algorithm-specific fields (created but initially hidden)
    shift_label = tk.Label(app, text="Shift:")
    shift_entry = tk.Entry(app, textvariable=shift_var)

    # Encrypt/Decrypt buttons in a frame
    btn_frame = tk.Frame(app)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
    tk.Button(btn_frame, text="Encrypt", command=do_encrypt).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Decrypt", command=do_decrypt).pack(side="left", padx=5)

    # Result display area (read-only text box)
    tk.Label(app, text="Result:").grid(row=6, column=0, sticky="nw", padx=4, pady=4)
    result_box = tk.Text(app, height=10, width=60)
    result_box.grid(row=6, column=1, sticky="nsew", padx=4, pady=4)

    def sync_result(*_: object) -> None:
        """Sync result_var changes to the result text box.
        
        When result_var changes, update the text box to show the new result.
        Text box is kept read-only to prevent user editing.
        """
        result_box.configure(state="normal")
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, result_var.get())
        result_box.configure(state="disabled")

    # Connect result_var changes to text box updates
    result_var.trace_add("write", sync_result)
    
    # Initialize fields based on default algorithm selection
    update_fields()
    
    # Make column 1 expandable for responsive layout
    app.grid_columnconfigure(1, weight=1)
    
    # Start GUI event loop
    app.mainloop()


if __name__ == "__main__":
    launch_gui()


