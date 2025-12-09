# Encryption Decryption Tool (Caesar & Base64)

## Title Page
- Title: Encryption & Decryption Tool (Caesar, Base64)
- Student: Suryanshi Singh (Roll No: 2201003121)
- Guide: Er. Anjana
- Department: Computer Science & Engineering
- Academic Year: 2025

## Certificate
This is to certify that the project report titled **“Encryption & Decryption Tool”** submitted by **Suryanshi Singh (Roll No: 2201003121)** has been carried out under my guidance and is a bonafide record of work.

Guide: Er. Anjana  
Date: _____________

## Declaration
I hereby declare that this report is my original work and has not been submitted elsewhere. All external sources have been acknowledged.

Suryanshi Singh  
Date: _____________

## Acknowledgement
I thank my guide Er. Anjana for mentorship, faculty for feedback, and peers for testing help.

## Abstract
This project delivers a small yet practical encryption-decryption utility combining two approachable schemes: Caesar cipher for introductory substitution and Base64 for text-safe encoding. The tool offers both a command-line interface built with Click and a minimal Tkinter GUI, targeting ease of use across Windows, Linux, and macOS. Sample datasets, unit tests, and concise documentation accompany the codebase, enabling students to explore cryptography workflows end-to-end—from preprocessing inputs to producing ciphertext and restoring plaintext. AES functionality was initially planned but removed on request to keep dependencies minimal. Overall, the project emphasizes readability, correctness, and reproducibility so learners can adapt it for coursework, demonstrations, or further research on secure communications.

## Table of Contents
1. Introduction  
2. Literature / Background  
3. System Design  
4. Implementation  
5. Testing & Results  
6. Conclusion & Future Work  
7. References  
8. Appendix  

## Chapter 1: Introduction
- **Purpose:** Provide a compact, comprehensible tool to demonstrate encryption/decryption workflows.
- **Motivation:** Students often need runnable examples that bridge theory (Caesar/Base64/AES) with practice (CLI/GUI, files).
- **Objectives:** Cross-platform usability, clear code, optional strong crypto, automated tests, and academic-ready documentation.

## Chapter 2: Literature / Background
- **Caesar Cipher:** Monoalphabetic shift by N positions; easy to break, good for teaching substitution.
- **Base64:** Binary-to-text encoding using 64-character alphabet; not encryption but ensures safe text transport.
- **Note on AES:** Modern strong encryption like AES was scoped but removed here to keep the tool dependency-light; see Future Work for reintroduction guidance.

## Chapter 3: System Design
- **Modules:**
  - `ciphers/caesar.py`: shift-based cipher.
  - `ciphers/base64_mod.py`: Base64 encode/decode using pybase64.
- `ciphers/base64_mod.py`: Base64 encode/decode using pybase64.
- `utils/crypto_helpers.py`: Padding helpers kept minimal after AES removal.
  - `utils/io_helpers.py`: file IO and safe input.
  - `cli.py`: Click commands (encrypt, decrypt, examples, --gui).
  - `gui.py`: Tkinter interface with dynamic fields.
- **Flow (ASCII in `docs/design_diagram_ascii.txt`):**
  Input → Preprocess → Cipher Module → Output; interfaces via CLI or GUI.
- **Data Flow (DFD sample):**
  User → CLI/GUI → Algorithm Selector → Cipher Engine → Output Writer → User.

## Chapter 4: Implementation
- **Language & Libs:** Python 3.10+, Click for CLI, Tkinter for GUI, pybase64, optional PyCryptodome/cryptography.
- **File Structure:** See `README.md`.
- **Key Snippets:**
  - Caesar shift wraps around alphabet; preserves case/non-letters.
  - Base64 uses UTF-8 encode/decode with clear error on invalid input.
  - AES: PBKDF2-derived 256-bit key, random salt/IV, PKCS7 padding, Base64 ciphertext output.
- **CLI Examples:**
  - `python -m src.cli encrypt --algo caesar --in "Hello" --shift 3`
  - `python -m src.cli decrypt --algo base64 --in "SGVsbG8="`
- (AES example removed per scope change)
- **GUI:** Dropdown for algorithm, fields for shift/password/salt/iv, encrypt/decrypt buttons, result area.
- **Placeholders:** GUI screenshot can be captured from running app; none embedded to keep repo small.

## Chapter 5: Testing & Results
- **Unit Tests:** Pytest suites for Caesar and Base64 (AES tests skipped after removal).
- **Sample Data:** `samples/sample_messages.txt` and expected outputs in `sample_output.md`.
- **Observed Results:** Round-trip tests pass; Base64 invalid input raises `ValueError`; AES decrypt matches plaintext when backend installed.

## Chapter 6: Conclusion & Future Work
- **Conclusion:** The tool meets educational goals—demonstrating two ciphers with approachable code, CLI/GUI access, and automated tests.
- **Future Work:** Reintroduce AES or other modern ciphers, add file drag-and-drop GUI, integrate SHA hashing, support streaming encryption, and offer FFI bindings for other languages.

## References
- RFC 4648: Base64 Data Encodings.
- PKCS #5 v2.0: Password-Based Cryptography Specification.
- PyCryptodome and cryptography official docs (useful if AES is reintroduced).

## Appendix
- **Run Commands:** See `docs/USAGE.md` and `README.md`.
- **Environment Setup:** `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- **Execution:** `python -m src.cli examples` or `python -m src.cli --gui`
- **Code Pointers:** Cipher modules under `src/ciphers/`; helpers in `src/utils/`.


