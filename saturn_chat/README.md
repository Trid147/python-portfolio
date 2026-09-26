# 🪐 Saturn Chat (v1.3)

Saturn Chat is a production-grade, lightweight, asynchronous, and hyper-anonymous console-based messenger built using Python's native `socket` and `threading` libraries. 

Moving far beyond simple local networks, it now operates as a globally accessible darknet platform featuring mandatory **End-to-End Encryption (E2EE)** and **Tor Onion Hidden Services** integration. It enables secure, decentralized communication anywhere in the world without a public/static IP or port forwarding.

## 🔑 Key Features
* **Multi-threaded Room Routing:** Smoothly handles multiple concurrent clients split across dynamic, password-protected chat rooms using Python's `threading` module and fine-grained `Lock` state synchronization.
* **Pure End-to-End Encryption (E2EE):** All chat room messages are encrypted on the client side using the **AES-256 (Fernet)** symmetric encryption standard derived from room codes. The server only handles, broadcasts, and logs encrypted base64 byte streams, making host-side conversation spying mathematically impossible.
* **Socks5 Tor Routing (NAT Traversal):** Built-in support for global connections via Tor Onion Hidden Services (`.onion`), allowing the server to safely accept worldwide traffic from behind strict household firewalls and residential routers.
* **On-the-Fly Dynamic Registry:** Accounts are stored in a volatile, secure in-memory dictionary. Shutting down the server completely wipes the user registry, leaving zero digital footprints on the server's hard drive.
* **Secure Cryptographic Hashing:** User passwords and room master keys are heavily protected using the native `SHA-256` hash function.
* **Robust Packet Reassembly:** Features a smart data stream slicer (`.split('\n')`) on the client side to mitigate TCP packet concatenation bugs, ensuring persistent chat histories decrypt perfectly regardless of network latency.
* **Anti-Overlapping Terminal UI:** Uses advanced ANSI escape codes (`\r\033[K`) to dynamically wipe the prompt line, ensuring incoming background packets never disrupt active user terminal inputs.

## 📦 Dependencies
To run the latest version, clients must install the following Python packages:
```bash
pip install cryptography PySocks
```

---

## 🛠️ Installation & Usage

### 1. Host Server Configuration
Deploy `server.py` on your host machine (e.g., an Ubuntu Server laptop).

#### To expose the server to the Global Tor Network (Optional):
1. Install Tor: `sudo apt install tor -y`
2. Configure hidden service in `/etc/tor/torrc`:
   ```text
   HiddenServiceDir /var/lib/tor/saturn_chat/
   HiddenServicePort 5731 127.0.0.1:5731
   ```
3. Restart Tor (`sudo systemctl restart tor`) and fetch your public darknet address:
   ```bash
   sudo cat /var/lib/tor/saturn_chat/hostname
   ```
4. Fire up your script:
   ```bash
   python3 server.py
   ```

### 2. Client Connection Mode
Configure your target connection endpoints inside `client.py`:

#### Option A: Local Network Mode (Wi-Fi)
Set `SERVER_IP` to your server's local address (e.g., `192.168.0.109`) and execute:
```bash
python3 client.py
```

#### Option B: Global Darknet Mode (Tor)
Ensure **Tor Browser** or **AnonSurf** is running in the background to provide a local SOCKS5 proxy (port `9150` or `9050`), set your unique `.onion` address as the target host, and execute:
```bash
python3 client.py
```

### 3. Authenticate & Command Set
Upon connecting, use single-line layouts to pass through state validations:
* **Register/Login:** `[username] [password]` (e.g., `neo shadow_pass123`)
* **Create Room (E2EE Active):** `/room create [name] [code] [password]`
* **Join Room (E2EE Active):** `/room join [name] [code]`
* **Leave Room:** `/room leave [name]`
* **Private Whisper:** `/w [username] [message]`

---

## 🗺️ Roadmap (Upcoming Features)

Saturn Chat is actively evolving into a fully featured, decentralized local messenger. The following features are planned for future releases:

* [x] **Stage 6: Private Messaging (`/w`)** — Implement a custom routing mechanism using socket-to-username mapping dictionaries to allow secure private whispers between users.
* [x] **Stage 7: Password Management** — Add secure runtime options for users to update or reset their volatile session passwords.
* [x] **Stage 8: Private Rooms & Channels** — Introduce multi-room capabilities allowing users to create and join isolated chat segments.
* [x] **Stage 9: End-to-End Encryption (E2EE)** — Integrate asymmetric cryptography (RSA/AES) so that messages are encrypted on the client side. The server will only route encrypted bytes, making it impossible for the host to spy on conversations.
* [x] **Stage 10: Decentralized Hosting (Tor/WireGuard)** — Document and configure alternative routing paths via Tor Onion Services and Tailscale to eliminate the need for a public/static IP.

## 📄 License
This project is licensed under the MIT License - see the main repository for details.
