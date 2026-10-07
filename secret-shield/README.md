# 🛡️ Pre-commit Secret Shield

A lightweight, standalone DevSecOps automation tool written in Python. It serves as a **Git Pre-commit Hook** that scans your code changes in real-time, preventing developers from accidentally committing sensitive credentials (API keys, tokens, passwords) to GitHub.

This project implements the **"Shift Left"** security principle by catching vulnerabilities directly on the developer's local machine before the code ever reaches a remote repository.

---

## ✨ Features

- **Automated Git Integration:** Automatically intercepts `git commit` commands via native Git Hooks.
- **Regex-Based Detection:** High-precision signature matching for popular cloud providers and platforms:
  - AWS Access Keys & Secret Tokens
  - Google Cloud & Yandex Cloud API Keys
  - GitHub PATs (Classic & Fine-Grained), GitLab Tokens
  - Telegram, Slack, and Discord Bot Tokens
  - OpenAI API Keys, Database Connection Strings, etc.
- **Shannon Entropy Analysis:** Sophisticated mathematical evaluation of string randomness to catch unique passwords and high-entropy generated hashes within code contexts.
- **Zero Third-Party Production Dependencies:** Built entirely using Python's standard library (`math`, `re`, `subprocess`, `pathlib`) for ultimate speed and supply-chain security.
- **ANSI Colorized CLI:** Clear, actionable, and visually distinct terminal logs (green for success, yellow/red for blocked commits).

---

## 📂 Project Structure

```text
secret_shield/
├── app/
│   ├── __init__.py
│   ├── main.py          # CLI entrypoint & Git interaction logic
│   └── scanner.py       # Secret detection algorithms (Regex & Entropy)
├── hooks/
│   └── pre-commit       # Native Git Hook bash wrapper
├── tests/
│   └── test_scanner.py  # Unit tests for verification
├── requirements.txt     # Production requirements (empty - uses standard lib)
├── requirements-dev.txt # Development requirements (pytest)
└── README.md            # Documentation
```

---

## 🚀 Installation & Setup

### 1. Clone & Navigate
Since this tool is part of the `python-portfolio` monorepository, navigate to the project directory:
```bash
cd secret_shield
```

### 2. Activate the Git Pre-commit Hook
To make this script run automatically before every commit, you need to copy the wrapper script into your local `.git/hooks/` directory.

From the root of the monorepository, run:
```bash
# Copy the hook wrapper
cp secret_shield/hooks/pre-commit .git/hooks/pre-commit

# Grant execution permissions (Linux/macOS)
chmod +x .git/hooks/pre-commit
```

---

## 🛠️ Development & Testing

If you want to contribute, modify rules, or run the test suite locally, follow these steps:

### 1. Install Developer Dependencies
```bash
pip install -r secret_shield/requirements-dev.txt
```

### 2. Run Unit Tests
The test suite ensures that signature rules and entropy calculations work flawlessly without breaking existing functionality:
```bash
cd secret_shield
PYTHONPATH=. pytest -v
```

### 3. CI/CD Integration
This project features automated testing via **GitHub Actions**. Any code updates pushed to the `secret_shield/` directory will trigger an isolated Linux workflow that installs dependencies, validates the test suite, and ensures code stability.

---

## 📝 Example Output

When a secret is detected during `git commit`:
```text
Secret Shield started...
Scanning secret_shield/app/main.py...
[String: 15] [Regex Match] [Found pattern: Google API Key]
Text: google_key = "AIzaSyAzX123456789012345678901234567890"

[-] Secrets found. Commit not committed.
```

When the code is clean:
```text
Secret Shield started...
Scanning secret_shield/app/main.py...
[+] No secrets found. Commit committed.
```
