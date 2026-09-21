# XOR Cipher CLI Tool

A lightweight Command Line Interface (CLI) application written in Python that encrypts and decrypts text using the bitwise **XOR (Exclusive OR)** operation. 

The project showcases clean code structure, user input validation, and automatic format detection using a custom protocol signature.

## Features

- **Smart Auto-Detection:** The script automatically detects whether the input is plain text (to encrypt) or an existing cipher (to decrypt) using a unique `G# ` prefix.
- **Data Integrity:** Encrypted data is converted into safe, copy-able space-separated integer codes. This prevents the console from breaking or swallowing invisible ASCII characters.
- **Clipboard Integration:** Automatically copies the resulting encrypted/decrypted text to your clipboard for instant sharing.
- **Robust Validation:** Features a safe loop for master-key entry with error handling.

## How It Works Under the Hood

1. **Encryption:** Takes your text, converts each character into its numeric Unicode code point (`ord()`), applies the XOR bitwise operator (`^`) with the master key, and saves the numbers as a string prefixed with `G# `.
2. **Decryption:** Detects the `G# ` prefix, splits the numbers, applies the inverse XOR operation with the same master key, and restores the original characters (`chr()`).

## Installation & Requirements

The project uses one external dependency for clipboard management.

1. Clone the repository and navigate to the project folder:
   ```bash
   cd cryptor
   ```

2. Install the required dependency:
   ```bash
   pip install pyperclip
   ```

## Usage

Run the script from your terminal:

```bash
python xor_cipher.py
```

### Example Workflow:

1. **Type your text:** `Hello World`
2. **Type your master-key symbol:** `K`
3. **Result:** `G# 43 46 47 47 44 91 22 44 53 47 41` *(Automatically copied to clipboard!)*

To decrypt, just run the script again, paste the `G# ...` cipher string, enter the **same key** (`K`), and you will get `Hello World` back.

## Future Roadmap

- [ ] Support multi-character master keys (Vigenère-style XOR shifting).
- [ ] Add standalone file encryption (.txt, .png, etc.).