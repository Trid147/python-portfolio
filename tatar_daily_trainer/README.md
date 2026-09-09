# Tatar Daily Trainer 🚀

Tatar Daily Trainer is a lightweight, interactive command-line application written in Python designed to help users practice and memorize Tatar vocabulary. It supports various training modes, tracks mistakes, and offers a color-coded terminal experience.

---

## ✨ Features

- **Multiple Training Modes:** Practice all words, a custom number of random words, specific parts of speech, or review only your mistakes.
- **Smart Mistake Tracking:** Automatically saves incorrect answers to a `mistakes.json` file so you can review them later. Correcting a previous mistake removes it from the list.
- **Categorized Vocabulary:** Words are split into structured JSON dictionaries (Verbs, Nouns, Adjectives, Numerals, Pronouns, and Adverbs).
- **PyInstaller Ready:** Configured to dynamically locate dictionaries whether run as a standard Python script or compiled into a standalone executable.
- **User-Friendly Interface:** Built with colorful terminal feedback using `colorama`.

---

## 🛠️ Project Structure

```text
├── main.py                  # Main application script
└── dicts/                   # Directory containing vocabulary JSON files
    ├── verbs.json
    ├── nouns.json
    ├── adjectives.json
    ├── numerals.json
    ├── pronouns.json
    ├── adverbs.json
    └── mistakes.json        # Automatically generated/updated history
```

*Note: Each dictionary JSON file should look like this:*
```json
{
    "яшел": "green",
    "китап": "book"
}
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Installed dependencies (`colorama`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Trid147/python-portfolio
   cd tatar-daily-trainer
   ```

2. **Install dependencies:**
   ```bash
   pip install colorama
   ```

3. **Prepare dictionaries:**
   Make sure the `dicts/` folder exists in the same directory as the script and contains the required `.json` files. If `mistakes.json` is missing, create an empty JSON object file:
   ```bash
   echo "{}" > dicts/mistakes.json
   ```

### Running the App

Run the script from your terminal:
```bash
python main.py
```

---

## 🎮 How to Play

Upon launch, you will be prompted to choose a practice mode:

| Mode ID | Mode Name | Description |
| :---: | :--- | :--- |
| `0` | **Exit** | Closes the application. |
| `1` | **All Words** | Standard quiz featuring every word from all dictionaries shuffled. |
| `2` | **Random** | Selects a specific number of random words to practice. |
| `3` | **Exact** | Allows you to target a specific part of speech (Verbs, Nouns, etc.). |
| `4` | **Mistakes** | Launches a session dedicated exclusively to words you previously got wrong. |

---

## 📦 Compiling to Executable (.exe)

Since the script includes a PyInstaller `sys._MEIPASS` fallback route, you can safely freeze it into a single binary file.

To build the executable, run:
```bash
pip install pyinstaller
pyinstaller --onefile --add-data "dicts;dicts" main.py
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
