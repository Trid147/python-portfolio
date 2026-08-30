# Async Network Scanner & Host Monitor (Async Net-Checker)

A fast, asynchronous Python CLI tool designed to scan multiple hosts, measure HTTP latency, and check specific network ports concurrently. Built using `asyncio` and `aiohttp`, this project demonstrates modern concurrent programming practices in Python.

---

## 🚀 About the Project
Instead of checking hosts one by one (synchronously), which can take minutes, this tool fires concurrent requests and scans everything in **just a couple of seconds**. It efficiently manages system resources using semaphores and prevents console output mixing (*race conditions*) by buffering logs.

## ✨ Features
* **Asynchronous HTTP/HTTPS Probing:** Leverages `aiohttp` to check host availability and measure response latency in milliseconds.
* **Concurrent TCP Port Scanning:** Uses low-level `asyncio.open_connection` to scan a list of custom ports (e.g., DNS, HTTP, HTTPS) in parallel.
* **Concurrency Control:** Utilizes `asyncio.Semaphore` to limit maximum simultaneous connections, keeping the script stealthy and network-friendly.
* **Thread-Safe Clean Output:** Implements string buffering before printing to prevent console output corruption caused by asynchronous execution overlap.
* **Clean Configuration:** Reads target IP addresses and domains dynamically from a structured `hosts.txt` file, bypassing empty lines and comments (`#`).

## 🛠️ Tech Stack & Key Concepts Demonstrated
* **Language:** Python 3.10+
* **Asynchronous Framework:** `asyncio` (`async/await`, `asyncio.gather`, `asyncio.Semaphore`, `asyncio.wait_for`)
* **Networking:** `aiohttp` (Asynchronous HTTP Client), low-level TCP streams (`open_connection`)
* **File I/O:** Modern path handling with `pathlib.Path`

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com
cd network-scanner
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure your targets:**
Create or modify `hosts.txt` in the root folder. You can add domains, IPs, or comments:
```text
# Public Websites
google.com
github.com

# Public DNS
8.8.8.8

# Dead host to test error handling
invalid-site-test-123.com
```

4. **Run the scanner:**
```bash
python main.py
```

---

## 📊 Sample Output

```text
ONLINE: https://google.com
Status: 200
Latency: 45ms
Port 53: CLOSED
Port 80: OPEN
Port 443: OPEN

OFFLINE: https://invalid-site-test-123.com
Error: ClientConnectorError
Port 53: CLOSED
Port 80: CLOSED
Port 443: CLOSED

Scan is fully completed after: 5 seconds
```

---
💡 *Feel free to star this repository if you find it useful or want to support my learning journey!*
