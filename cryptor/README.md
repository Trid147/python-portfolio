# Crypter — Message Encryption & Decryption Tool

A lightweight, console-based Python utility for **encrypting and decrypting messages** using a customizable substitution cipher table defined in a JSON configuration file. The tool automatically preserves text casing and features a colorized terminal interface.

## Features
*   **Highly Customizable:** The cipher rules are fully managed through an external `config.json` file.
*   **Homophonic Substitution:** If a single character maps to a list of substitute words, the script randomly chooses one during encryption to increase cipher complexity.
*   **Case Preservation:** Automatically detects uppercase letters and reflects the casing in the encrypted or decrypted output.
*   **Colorized Interface:** Uses the `colorama` library for clear, visual separation of menus, errors, and results.

---

## Tech Stack
*   **Language:** Python 3.x
*   **Libraries:** `colorama`, `json`, `os`, `time`, `random`

---

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd your-repo-name
   ```

2. Install the required dependency (`colorama`):
   ```bash
   pip install colorama
   ```

---

## Configuration (`config.json`)

Before running the program, make sure to create a `config.json` file in the **same directory** as the script. This file dictates your cipher table. Characters can map to either a single string or an array of replacement strings.

**Example `config.json` structure:**
```json
{
  "a": "alpha",
  "b": "bravo",
  "c": ["charlie", "cherry"],
  "x": "xray"
}
```
*Note: Since the letter "c" maps to an array `["charlie", "cherry"]`, the script will randomly select one of these two words every time it encounters the letter "c" during encryption.*

---

## How to Use

Run the script using your terminal:
```bash
python main.py
```

### Menu Options:
1.  **Encrypt:** Converts your plain text into a sequence of encrypted cipher words separated by spaces.
2.  **Decrypt:** Takes a space-separated string of cipher words and restores the original text.
3.  **Leave:** Safely exits the application.

---

## Example Usage

**Encryption (Mode 1):**
*   *Input:* `A bc`
*   *Config:* `"a": "one", "b": "two", "c": "three"`
*   *Console Output:* `ONE two three`

**Decryption (Mode 2):**
*   *Input:* `ONE two three`
*   *Console Output:* `A bc`

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
