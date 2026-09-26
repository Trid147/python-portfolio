import socket
import threading
import sys
import hashlib
import base64
import socks
from cryptography.fernet import Fernet

SERVER_ONION = 'xyzxwoexvdzddlbhk5nfwdq65yqhb3rrtls3zu7y6eyhp4r4dx3nqiqd.onion' #your server onion adress
PORT = 5731

current_room = None
current_crypto = None

def make_crypto_object(room_code: str) -> Fernet:
    '''creates fernet crypto object'''
    key_32_bytes = hashlib.sha256(room_code.encode('utf-8')).digest()
    fernet_key = base64.urlsafe_b64encode(key_32_bytes)
    return Fernet(fernet_key)

def check_and_decrypt(raw_text: str) -> str:
    '''only gets crypted message and decrypts it'''
    global current_crypto
    if not current_crypto:
        return raw_text

    lines = raw_text.split('\n')
    decrypted_lines = []

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        if ']: ' in line_clean and ' [' in line_clean:
            header, rest = line_clean.split(']: ', 1)
            cipher_text, timestamp = rest.rsplit(' [', 1)

            try:
                decrypted_bytes = current_crypto.decrypt(cipher_text.strip().encode('utf-8'))
                decrypted_text = decrypted_bytes.decode('utf-8')
                
                decrypted_lines.append(f'{header}]: {decrypted_text} [{timestamp}')
            except Exception:
                decrypted_lines.append(line_clean)
        else:
            decrypted_lines.append(line_clean)

    if decrypted_lines:
        return '\n'.join(decrypted_lines) + '\n'
    return raw_text

def receive_messages(client_socket):
    '''thread which only accepts messages from the server'''
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('\nDisconnected from the server.')
                break

            raw_message = data.decode('utf-8')
            decrypted_message = check_and_decrypt(raw_message)

            sys.stdout.write(f'\r\033[K{decrypted_message}You: ')
            sys.stdout.flush()
        except:
            break

def main():
    global current_room, current_crypto

    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9150)

    socket.socket = socks.socksocket

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print('Connection to Saturn Chat via Tor network... Please, wait...')
        client.connect((SERVER_ONION,PORT))
    except Exception as e:
        print(f'Could not connect to server: {e}')
        print('Make sure you are connect to the Tor Network!')
        return

    welcome_msg = client.recv(1024).decode('utf-8')
    auth_input = input(welcome_msg)
    client.sendall(auth_input.encode('utf-8'))

    auth_status = client.recv(1024).decode('utf-8')
    print(auth_status)

    if 'ERROR' in auth_status:
        client.close()
        return

    while True:
        chunk = client.recv(1024).decode('utf-8')

        if '<END_OF_HISTORY>\n' in chunk:
            final_text = chunk.replace('<END_OF_HISTORY>\n', '')
            sys.stdout.write(final_text)
            break

        sys.stdout.write(chunk)
        sys.stdout.flush()

    receive_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    receive_thread.start()

    try:
        while True:
            message = input('You: ')
            if not message.strip():
                continue

            if message.startswith('/room'):
                parts = message.split()
                if len(parts) >= 5 and parts[1] == 'create':
                    current_room = parts[2]
                    current_crypto = make_crypto_object(parts[3])
                elif len(parts) >= 4 and parts[1] == 'join':
                    current_room = parts[2]
                    current_crypto = make_crypto_object(parts[3])
                elif len(parts) >= 3 and parts[1] == 'leave':
                    current_room = None
                    current_crypto = None

            if not message.startswith('/') and current_crypto:
                encrypted_text = current_crypto.encrypt(message.encode('utf-8'))
                client.sendall(encrypted_text)
            else:
                client.sendall(message.encode('utf-8'))
    finally:
        client.close()
        print('Disconnected.')

if __name__ == '__main__':
    main()