# Saturn Remote Administration Tool (SRAT)

A lightweight, multi-threaded asynchronous Remote Administration Tool written in Python using the **Paramiko** library. This project demonstrates how to implement secure, encrypted reverse shell connections using SSHv2 protocols without relying on pre-installed system OpenSSH servers on the client side.

## ⚠️ Disclaimer
This project was developed strictly for **educational purposes**, security research, and legitimate system administration. The author is not responsible for any misuse, damage, or illegal tracking caused by this software. Use it only on environments you own or have explicit authorized permission to test.

## ✨ Features
* **Multi-Threaded Architecture:** The server can accept and maintain multiple client connections simultaneously in the background using Python `threading`.
* **Encrypted Traffic:** All communication, commands, and outputs are fully encrypted using SSHv2 protocols via the `paramiko` library.
* **Smart Directory Traversal:** Implements custom native `cd` (change directory) command tracking, allowing true navigation across the remote filesystem.
* **Persistent Connection:** The client features an automated reconnection mechanism that attempts to re-establish the tunnel every 10 seconds if the server goes offline.
* **No Admin Privileges Required:** The client script executes completely in user space, requiring zero configuration or administrative rights on the managed machine.

## 🚀 Getting Started

### Prerequisites
Both server and client require Python 3.x and the `paramiko` library installed.

```bash
pip install paramiko
```

### 1. Generate Server Host Keys
Before running the server, you need to generate a private RSA key that the server will use to host the SSH session:

```bash
ssh-keygen -t rsa -f rsa.key -N ""
```
*Ensure the generated `rsa.key` file is placed in the same directory as `server.py`.*

### 2. Configure and Start the Control Server
1. Open `server.py` and set the desired port (default is `2222`).
2. Run the server on your controller machine (e.g., Linux/Parrot OS):
```bash
python3 server.py
```

### 3. Configure and Launch the Client
1. Open `client.py` and update the target variables with your server's credentials:
   * `IP`: Your server's accessible IP address.
   * `PORT`: The port your server is listening on.
2. Run the client on the target machine (e.g., Windows 10):
```bash
python client.py
```

## 🎮 Usage Reference
Once the client connects, you will see a main menu on the server side:
* **Option 1:** Displays all currently active devices and their unique IDs.
* **Option 2:** Allows you to enter interactive session mode with a specific device using its ID.

Inside the session mode, you can type standard OS commands (`dir`, `whoami`, `ipconfig`, etc.). 
* To return to the main menu without dropping the connection, type: `back`
* To completely close the session and disconnect the client, type: `exit`

## 🛠️ Technical Details & Architecture
Unlike traditional reverse SSH setups that require an active `sshd` daemon running on the target machine, this tool implements a custom `paramiko.ServerInterface` on the control server and handles command execution directly via Python's `subprocess` engine on the client. Traffic routing behaves completely synchronously (1 Request -> 1 Encrypted Reply), eliminating buffer desynchronization bugs.

## 🗺️ Future Roadmap
The project is actively being developed. The following features are planned for future releases:

- [x] **Secure File Transfer (SFTP Engine):** Native `download` and `upload` command handlers to easily exfiltrate or deliver files between the server and clients.
- [x] **Stealth Mode Deployment:** Integrating WinAPI compiler modifications (`pyinstaller --noconsole`) and window-hiding subroutines to run the client completely as a background service.
- [x] **System Persistence:** Automated registry integration (`CurrentVersion\Run`) and hidden directory staging to ensure the client automatically boots with the host OS.
- [x] **Interactive Dynamic Menu:** Upgrading the main menu loop to asynchronously refresh when a client drops or joins without requiring manual inputs.
