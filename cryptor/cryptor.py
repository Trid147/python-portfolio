import os
import time
import json
import random
from colorama import init, Fore, Style

init(autoreset=True)

try:
    with open('config.json', 'r', encoding='utf-8') as file:
        cipher_table = json.load(file)
except FileNotFoundError:
    print(Fore.RED + "Error: config.json file not found! Please create it in the same folder.")
    time.sleep(3)
    exit()


decipher_table = {}
for key, values in cipher_table.items():
    if isinstance(values, list):
        for word in values:
            decipher_table[word] = key
    else:
        decipher_table[values] = key

print(Fore.GREEN + "Welcome to the Crypter!")

while True:
    try:
        mode = int(input("What do you want to do:\n1. Encrypt\n2. Decrypt\n3. Leave\nEnter your choice (from 1 to 3): "))
    except ValueError:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + "Error: Invalid input. Please enter a number (1, 2 or 3).")
        continue
    
    if mode == 1:
        message = input("Enter the message to encrypt: ")
        encrypt_table = []
        for char in message:
            char_lower = char.lower()
            if char_lower in cipher_table:
                substitution = cipher_table[char_lower]

                if isinstance(substitution, list):
                    chosen_word = random.choice(substitution)
                else:
                    chosen_word = substitution

                if char.isupper():
                    encrypt_table.append(chosen_word.upper())
                else:
                    encrypt_table.append(chosen_word)
            else:
                encrypt_table.append(char)
        encrypted_message = ' '.join(encrypt_table)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + f"Encrypted message: {encrypted_message}")
    elif mode == 2:
        message = input("Enter the message to decrypt: ")
        message_table = message.split()
        decrypt_table = []
        for word in message_table:
            word_lower = word.lower()
            if word_lower in decipher_table:
                if word.isupper():
                    decrypt_table.append(decipher_table[word_lower].upper())
                else:
                    decrypt_table.append(decipher_table[word_lower])
            else:
                decrypt_table.append(word)
        decrypted_message = ''.join(decrypt_table)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + f"Decrypted message: {decrypted_message}")
    elif mode == 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.GREEN + "Exiting the Crypter. Goodbye!")
        time.sleep(1)
        break
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + "Error: Invalid choice. Please enter 1, 2, or 3.")

