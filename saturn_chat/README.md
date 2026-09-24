# 🪐 Saturn Chat (v1.1)

Saturn Chat is a lightweight, asynchronous, and hyper-anonymous console-based chat application built using Python's native `socket` and `threading` libraries. 

Designed for maximum privacy within a local network (Wi-Fi), it features dynamic registration, zero-footprint credential storage, and real-time message broadcasting without relying on heavy external database engines.

## 🔑 Key Features
* **Multi-threaded Architecture:** Handles multiple concurrent client connections smoothly using Python's `threading` module.
* **On-the-Fly Authentication:** Users can register and log in instantly via a single command line (`login password`).
* **RAM-Only User Registry:** Accounts are stored in a secure in-memory dictionary. Shutting down the server completely wipes the user registry, leaving zero traces on the disk.
* **Secure Password Hashing:** Credentials are never stored in plaintext; Saturn Chat protects them using the `SHA-256` cryptographic hash function.
* **Persistent Chat History:** Messages are streamed and appended into a lightweight `.jsonl` (JSON Lines) file, preventing race conditions via thread locks. New users automatically receive the chat history upon successful login.
* **Clean Terminal UI:** Uses ANSI escape codes (`\r\033[K`) to prevent overlapping text, ensuring that incoming messages do not disrupt active console input.

## 🛠️ Installation & Usage

Each component is completely standalone. To run the chat within your local network:

### 1. Start the Server
Deploy `server.py` on your host machine (e.g., an Ubuntu Server laptop).
```bash
python3 server.py
```

### 2. Connect the Clients
Configure the `SERVER_IP` inside `client.py` to match your server's local IP address, then run the client on any machine within the same Wi-Fi network:
```bash
python3 client.py
```

### 3. Authenticate
Upon connection, enter your desired username and password separated by a space:
```text
Welcome to Saturn Chat! Enter [login password] to login/register.
-< neo shadow_pass123
```

---

## 🗺️ Roadmap (Upcoming Features)

Saturn Chat is actively evolving into a fully featured, decentralized local messenger. The following features are planned for future releases:

* [x] **Stage 6: Private Messaging (`/w`)** — Implement a custom routing mechanism using socket-to-username mapping dictionaries to allow secure private whispers between users.
* [x] **Stage 7: Password Management** — Add secure runtime options for users to update or reset their volatile session passwords.
* [ ] **Stage 8: Private Rooms & Channels** — Introduce multi-room capabilities allowing users to create and join isolated chat segments.
* [ ] **Stage 9: End-to-End Encryption (E2EE)** — Integrate asymmetric cryptography (RSA/AES) so that messages are encrypted on the client side. The server will only route encrypted bytes, making it impossible for the host to spy on conversations.
* [ ] **Stage 10: Decentralized Hosting (Tor/WireGuard)** — Document and configure alternative routing paths via Tor Onion Services and Tailscale to eliminate the need for a public/static IP.

## 📄 License
This project is licensed under the MIT License - see the main repository for details.
