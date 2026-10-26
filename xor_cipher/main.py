import os
import sys
import pyperclip
from pathlib import Path

CWD = Path.cwd()

def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_master_key() -> str:
    while True:
        master_key = str(input('Type your master-key: '))
        if len(master_key) > 0 and len(master_key) <= 50:
            return master_key
        print('Invalid master-key!')

def encrypt_text(text: str, key: str) -> str:
    crypted_chars = []
    key_lenth = len(key)
    if text.startswith('G# '):
        strings = text[3:].split()
        numbers = [int(string) for string in strings]
        for index, number in enumerate(numbers):
            key_char = key[index % key_lenth]
            crypted_char = chr(number ^ ord(key_char))
            crypted_chars.append(crypted_char)
            index += 1
        crypted_message = ''.join(crypted_chars)
    else:
        for index, char in enumerate(text):
            key_char = key[index % key_lenth]
            crypted_char = str(ord(char) ^ ord(key_char))
            crypted_chars.append(crypted_char)
            index += 1
        crypted_message = 'G# ' + ' '.join(crypted_chars)
    return crypted_message

def encrypt_file(file: Path, key: str) -> str:
    key_bytes = key.encode('utf-8')
    with open(file, 'rb') as f:
        data = f.read()

    processed_data = bytearray()
    key_lenth = len(key_bytes)
    for index, byte in enumerate(data):
        key_byte = key_bytes[index % key_lenth]
        crypted_byte = byte ^ key_byte
        processed_data.append(crypted_byte)
    processed_data = bytes(processed_data)

    with open(file, 'wb') as f:
        f.write(processed_data)

    return str(file)

def main():
    key = get_master_key()
    while True:
        try:
            clear_output()
            mode = int(input((f'Choose what you want:\n1 - encrypt text\n2 - encrypt file\n>- ')))
        except ValueError:
            input('Incorrect choice! Press enter to try again...')
            continue

        if mode not in [1, 2]:
            input('Incorrect choice! Press enter to try again...')
            continue

        while True:
            clear_output()
            if mode == 1:
                text = str(input('Type your text: '))
                result = encrypt_text(text, key)
                print(f'Result: {result}\n')
            elif mode == 2:
                file_name = str(input('Type your file name: '))
                file = CWD / file_name
                if not file.exists() or file.is_dir():
                    input(f'File "{file_name}" does not exist! It should be in the project folder. Press enter to try again...\n')
                    continue
                result = encrypt_file(file, key)
                print(f'File "{file_name}" encrypted.\n')
            else: break # plug for pyright

            action = input('Type "copy" if you want to copy the result.\nType "close" if you want to close application.\nPress "Enter" to continue.\n>- ')
            if action == 'copy':
                pyperclip.copy(result)
            elif action == 'close':
                sys.exit(0)


if __name__ == '__main__':
    main()