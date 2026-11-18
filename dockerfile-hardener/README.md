# Dockerfile Hardener (GUI)

A lightweight desktop DevSecOps tool built with Python and Tkinter to audit `Dockerfile` configurations for security misconfigurations and automatically generate hardened versions.

## Features

* **Static Security Analysis:** Scans Dockerfiles line-by-line and calculates a severity score based on CIS Docker Benchmark best practices:
  * **High Severity:**
    * Potential hardcoded secrets detected via **Shannon Entropy** analysis (ignoring `@sha256:` image digests).
    * Missing non-root `USER` instruction (containers running as `root` by default).
    * Exposed administrative ports (`22` SSH / `23` Telnet).
  * **Medium Severity:**
    * Unpinned `:latest` base image tags.
    * Use of `ADD` instead of `COPY` for local file transfers.
  * **Low Severity:**
    * `pip install` commands missing `--no-cache-dir`.
    * `apt-get install` commands missing `--no-install-recommends`.
* **Automated Remediation (`Harden file`):** Generates a `.hardened` copy of your `Dockerfile` without overwriting the original file:
  * Replaces `ADD` with `COPY`.
  * Injects `--no-cache-dir` and `--no-install-recommends` flags.
  * Strips insecure ports (`22`, `23`) from `EXPOSE` instructions.
  * Creates and switches to a non-root user (`appuser`) before `CMD` or `ENTRYPOINT`.
  * Inserts inline security warning comments above lines containing suspected hardcoded secrets.
* **Zero External Dependencies:** Built 100% with the Python Standard Library (`tkinter`, `math`, `pathlib`).

## Project Structure

```text
dockerfile-hardener/
├── main.py                  # Main Tkinter GUI and auditing/hardening engine
├── examples/
│   ├── Dockerfile.bad       # Sample insecure Dockerfile for testing
│   └── Dockerfile.good      # Sample hardened Dockerfile reference
└── README.md
```

## How to Run

1. Make sure you have **Python 3.8+** installed with Tkinter support (included by default on Windows and macOS; on Linux, install via `sudo apt-get install python3-tk`).
2. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/Trid147/python-portfolio
   cd python-portfolio/dockerfile-hardener
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Click **Select file** and choose any `Dockerfile` (or `*.dockerfile`).
2. Click **Analyze file** to run the security audit and view color-coded findings and the total severity score.
3. Click **Harden file** to generate a remediated `<filename>.hardened` file in the same directory.

## Future Improvements

* Add support for multi-stage build recommendations.
* Add automatic `rm -rf /var/lib/apt/lists/*` cleanup for `apt-get` layers.
* Export audit findings to JSON or Markdown reports for CI/CD pull request reviews.