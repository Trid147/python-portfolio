# Py-Security-Linter

A lightweight, high-performance DevSecOps CLI tool written in Python to perform automated static application security testing (SAST) on `Dockerfile` variants and software composition analysis (SCA) on Python `requirements.txt` dependencies.

The tool helps developers implement the **Shift Left** security approach by identifying hardcoded secrets, misconfigured base images, and known vulnerabilities (CVEs) before code reaches production.

## 🚀 Features

- **Dockerfile SAST Scanner:**
  - Detects unsafe base images using the `:latest` tag or lacking explicit tags.
  - Scans for hardcoded secrets, API tokens, and passwords in `ENV` and `ARG` instructions.
  - Warns if no `USER` configuration is specified (container running with dangerous root privileges).
- **Dependency SCA Scanner:**
  - Parses standard `requirements.txt` files (filtering comments and hashes).
  - Performs asynchronous bulk queries using the official **Google OSV (Open Source Vulnerabilities) API**.
  - Generates a visual, structured vulnerability table directly in your terminal.
- **CI/CD Ready Outputs:**
  - Separates human-readable colored terminal output from machine-readable data.
  - Generates a uniform, clean `report.json` for seamless integration into automation pipelines (GitHub Actions, GitLab CI/CD).

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Console UI:** `rich`, `colorama`
- **Networking:** `requests`
- **Vulnerability Feed:** Google OSV API (PyPI ecosystem)

## 📦 Installation & Setup

1. **Clone the repository into your WSL / Linux environment:**
   ```bash
   git clone https://github.com
   cd py-security-linter
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure your project's `requirements.txt` contains: `requests`, `rich`, and `colorama`)*

## 💻 Usage

Run the scanner by executing `main.py` and passing the target file path as a positional command-line argument.

### Scan a Dockerfile:
```bash
python main.py tests/bad.Dockerfile
```

### Scan Python Dependencies:
```bash
python main.py tests/bad_requirements.txt
```

## 📁 Project Structure

```text
py-security-linter/
├── main.py            # CLI Entrypoint (Arguments parsing & validation)
├── linter.py          # Core logic (SAST & SCA scanning engines)
├── requirements.txt   # Tool dependencies
├── report.json        # Automatically generated scan report
└── tests/             # Local test suites
    ├── bad.Dockerfile
    ├── good.Dockerfile
    └── bad_requirements.txt
    └── good_requirements.txt
```

## 📊 Automation Report Format (`report.json`)

The scanner automatically outputs validation metrics into a structured JSON payload for external logging or build-breaking steps in CI pipelines:

```json
{
  "scan_meta": {
    "timestamp": "2026-09-16T16:24:00Z",
    "target_file": "/home/user/py-security-linter/tests/bad.Dockerfile",
    "status": "FAILED",
    "total_issues": 3
  },
  "issues": [
    {
      "type": "SECRET_LEAK",
      "severity": "CRITICAL",
      "line": 5,
      "message": "Hardcoded sensitive data found."
    }
  ]
}
```

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).