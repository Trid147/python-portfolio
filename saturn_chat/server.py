import socket
import threading
import hashlib
import json
from pathlib import Path

HOST = ''
PORT = 5731

server_dir = Path(__file__).parent
database = server_dir / 'database.json'
messages_history = server_dir / 'messages_history.jsonl'

clients = []
client_locks = threading.Lock()

users = {}
user_locks = threading.Lock()

if not database.exists():
    with open(database, 'w', encoding='utf-8') as file:
        json.dump({}, file)

if not messages_history.exists():
    messages_history.touch()

with open(database, 'r', encoding='utf-8') as file:
    users = json.load(file)

history_lock = threading.Lock()

def get_password_hash(password):
    '''hashing password for total security of database'''
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def broadcast(message, sender_socket):
    '''function sends the message everyone besides the sender'''
    with client_locks:
        for client in clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    pass

def handle_client(client_socket, client_address):
    print(f'New thread started for: {client_address}')
    username = None

    try:
        client_socket.sendall(f'\nWelcome to Saturn Chat! Enter [login password] to login/register.\n-< '.encode('utf-8'))

        auth_data = client_socket.recv(1024).decode('utf-8').strip()
        if not auth_data:
            return

        parts = auth_data.split(maxsplit=1)

        if len(parts) != 2:
            client_socket.sendall('ERROR: Invalid format. Disconnecting...\n'.encode('utf-8'))
            return

        user = parts[0]
        password = parts[1]

        # authorization checks
        with user_locks:
            if not user in users:
                users[user] = get_password_hash(password)
                client_socket.sendall('SUCCESS: You have registered successfully.\n'.encode('utf-8'))

                with open(database, 'w', encoding='utf-8') as file:
                    json.dump(users, file, ensure_ascii=False, indent=4)
            else:
                user_hash = get_password_hash(password)
                correct_hash = users[user]
                if user_hash == correct_hash:
                    client_socket.sendall('SUCCESS: You have logged in successfully.\n'.encode('utf-8'))
                else:
                    client_socket.sendall('ERROR: Login or password incorrect.\n'.encode('utf-8'))
                    return

        username = user

        with history_lock:
            with open(messages_history, 'r', encoding='utf-8') as file:
                with open(messages_history, 'r', encoding='utf-8') as file:
                    clean_lines = [line.strip().replace('"', '') for line in file if line.strip()]
                    raw_messages_history = '\n'.join(clean_lines)

        if raw_messages_history:
            client_socket.sendall(f'{raw_messages_history}\n'.encode('utf-8'))

        with client_locks:
            clients.append(client_socket)

        broadcast(f'Client {username} joined the chat.', client_socket)
        print(f'Client {username} connected.')

        # main chat cycle
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode('utf-8')
            print(f'[{username}]: {message}')

            chat_message = f'[{username}]: {message}'
            broadcast(chat_message, client_socket)

            with history_lock:
                with open(messages_history, 'a', encoding='utf-8') as file:
                    file.write(json.dumps(chat_message, ensure_ascii=False) + '\n')

    except Exception as e:
        print(f'An error with client: {e}')
    finally:
        with client_locks:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()

        if username:
            broadcast(f'User {username} left the chat.', None)
            print(f'Client {username} disconnected.')
        else:
            print(f'Unautheficated client {client_address} disconnected.')


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST,PORT))
    server.listen()

    print(f'Server started with port: {PORT}')

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()