import sys
import pyperclip

def get_master_key():
    while True:
        try:
            master_key = str(input('Type your master-key: '))
            if len(master_key) > 0 and len(master_key) <= 50:
                return master_key
            else:
                print('Invalid master-key!')
                continue
        except ValueError:
            print('Invalid master-key!')
            continue

def xor_cipher(text, key):
    crypted_chars = []
    key_index = 0
    key_char = ''
    if text.startswith('G# '):
        strings = text[3:].split()
        numbers = [int(string) for string in strings]
        for number in numbers:
            key_char = key[key_index % len(key)]
            crypted_char = chr(number ^ ord(key_char))
            crypted_chars.append(crypted_char)
            key_index += 1
        crypted_message = ''.join(crypted_chars)
    else:
        for char in text:
            key_char = key[key_index % len(key)]
            crypted_char = str(ord(char) ^ ord(key_char))
            crypted_chars.append(crypted_char)
            key_index += 1
        crypted_message = 'G# ' + ' '.join(crypted_chars)
    return crypted_message

def main():
    key = get_master_key()
    while True:
        text = str(input('Type your text: '))
        message = xor_cipher(text, key)
        print(f'Result: {message}')
        action = input('Type "copy" if you want to copy the result.\nType "close" if you want to close application.\nPress "Enter" to continue.\n>- ')
        if action == 'copy':
            pyperclip.copy(message)
        elif action == 'close':
            sys.exit(0)


if __name__ == '__main__':
    main()