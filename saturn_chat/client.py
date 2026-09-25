import socket
import threading
import sys

SERVER_IP = '192.168.0.111' #your server ip
PORT = 5731

def receive_messages(client_socket):
    '''thread which only accepts messages from the server'''
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('\nDisconnected from the server.')
                break

            sys.stdout.write(f'\r\033[K{data.decode('utf-8')}\nYou: ')
            sys.stdout.flush()
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((SERVER_IP,PORT))
    except Exception as e:
        print(f'Could not connect to server: {e}')
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
            if message.strip():
                client.sendall(message.encode('utf-8'))
    finally:
        client.close()
        print('Disconnected.')

if __name__ == '__main__':
    main()