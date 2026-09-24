import socket
import threading
import hashlib
import json
import time
import os
from pathlib import Path
from datetime import datetime

HOST = ''
PORT = 5731

server_dir = Path(__file__).parent
database = server_dir / 'database.json'
messages_history = server_dir / 'messages_history.jsonl'

clients = []
client_locks = threading.Lock()

users = {}
user_locks = threading.Lock()

active_users = {}
active_users_locks = threading.Lock()

if not database.exists():
    with open(database, 'w', encoding='utf-8') as file:
        json.dump({}, file)

if not messages_history.exists():
    messages_history.touch()

with open(database, 'r', encoding='utf-8') as file:
    users = json.load(file)

history_lock = threading.Lock()

start_time = 0

def process_command(client, username, command, args):
    if command == '/w':
        error_message = 'Wrong format. Usage: "/w [username] [message]"\n'
        if len(args) >= 2:
            target_user = args[0]
            private_message = ' '.join(args[1:])
            if active_users.get(target_user):
                target_socket = active_users.get(target_user)
                formatted_message = f'PM from {username}: {private_message}\n'
                target_socket.sendall(formatted_message.encode('utf-8'))
            else:
                client.sendall(error_message.encode('utf-8'))
        else:
            client.sendall(error_message.encode('utf-8'))
    elif command == '/password':
        error_message = 'Wrong format. Usage: "/password [old_password] [new_password]"\n'
        if len(args) == 2:
            old_password = args[0]
            new_password = args[1]

            if get_password_hash(old_password) == users.get(username):
                with user_locks:
                    users[username] = get_password_hash(new_password)
                    with open(database, 'w', encoding='utf-8') as file:
                        json.dump(users, file, ensure_ascii=False, indent=4)
                client.sendall('Password changed successfully.\n'.encode('utf-8'))
            else:
                client.sendall('Wrong old password.\n'.encode('utf-8'))
        else:
            client.sendall(error_message.encode('utf-8'))
    elif command == '/uptime':
        global start_time
        running_time = int(time.time() - start_time)
        client.sendall(f'Server running for {running_time} seconds.\n'.encode('utf-8'))
    elif command == '/ping':
        client.sendall(f'Pong!\n'.encode('utf-8'))
    elif command == '/online':
        online_list = ['Users online:\n']
        for user in active_users:
            online_list.append(f'{user}\n')
        online_string = ''.join(online_list)
        client.sendall(online_string.encode('utf-8'))
    elif command == '/clear':
        client.sendall(b'\033[2J\033[H')

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

        with active_users_locks:
            active_users[username] = client_socket

        with history_lock:
            with open(messages_history, 'r', encoding='utf-8') as file:
                clean_lines = [line.strip().replace('"', '') for line in file if line.strip()]

        if clean_lines:
            for line in clean_lines:
                client_socket.sendall(f'{line}\n'.encode('utf-8'))

        client_socket.sendall(f'<END_OF_HISTORY>\n'.encode('utf-8'))

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

            if message.startswith('/'):
                parts = message.split()
                command = parts[0].lower()
                args = parts[1:]
                process_command(client_socket, username, command, args)
                continue
            else:
                print(f'[{username}]: {message} [{datetime.now()}]')

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
            with active_users_locks:
                if username in active_users:
                    del active_users[username]
            broadcast(f'User {username} left the chat.', None)
            print(f'Client {username} disconnected.')
        else:
            print(f'Unauthenticated client {client_address} disconnected.')


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST,PORT))
    server.listen()

    print(f'Server started with port: {PORT}')

    global start_time
    start_time = time.time()

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()