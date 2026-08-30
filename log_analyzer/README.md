# Linux Authentication Log Analyzer

A Python-based automation tool designed for Linux system administrators and security analysts. It parses system authentication logs to monitor user activity and detect brute-force attacks in real-time.

## Features
* **Root Rights Verification:** Checks if the script is running with superuser privileges (essential for protected log files).
* **Stat Gathering:** Counts successful (`Accepted`) and unsuccessful (`Failed`) login attempts.
* **Brute-Force Detection:** Flags IP addresses that exceed a user-defined threshold of failed logins.
* **CLI Arguments Support:** Allows customization of the target log file and threshold limit via terminal flags.
* **Reporting:** Generates a comprehensive summary report in a standalone text file.

## How to Run

1. Navigate to the project directory:
```bash
cd log_analyzer
```

2. Run the script with the default test log:
```bash
python3 log_analyzer.py --log test_auth.txt --limit 5
```

3. (Optional) Run on a live production server against the actual system logs (requires root privileges):
```bash
sudo python3 log_analyzer.py --log /var/log/auth.log --limit 5
```

## Requirements
* Python 3.x
* Linux environment (Tested on Parrot Security OS / Debian)
