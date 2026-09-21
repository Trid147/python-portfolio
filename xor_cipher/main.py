import sys
import pyperclip

def get_master_key():
    while True:
        try:
            master_key = str(input('Type your master-key symbol: '))
            if len(master_key) == 1:
                return master_key
            else:
                print('Invalid master-key! You should type only one symbol!')
                continue
        except ValueError:
            print('Invalid master-key! You should type a symbol.')
            continue

def xor_cipher(text, key):
    crypted_chars = []
    if text.startswith('G# '):
        strings = text[3:].split()
        numbers = [int(string) for string in strings]
        for number in numbers:
            crypted_char = chr(number ^ ord(key))
            crypted_chars.append(crypted_char)
        crypted_message = ''.join(crypted_chars)
    else:
        for char in text:
            crypted_char = str(ord(char) ^ ord(key))
            crypted_chars.append(crypted_char)
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