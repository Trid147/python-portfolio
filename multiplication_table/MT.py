import random
import os
import time
from colorama import init, Fore, Style

init(autoreset=True)

multiplication_table = {}

for i in range(1, 11):
    for j in range(1, 11):
        key = f"{i} * {j}"
        multiplication_table[key] = i * j

all_examples = list(multiplication_table.keys())

def StartTesting():
    print(Fore.CYAN + "To stop the trainer, answer the example: '0'.")

    while True:
        random_example = random.choice(all_examples)
        correct_answer = multiplication_table[random_example]

        while True:
            try:
                answer = int(input(random_example + " = "))
            except ValueError:
                print(Fore.RED + "Please enter a number!")
                continue

            if answer == 0:
                print(Fore.CYAN + "The trainer is stopping.")
                time.sleep(2)
                os.system("cls" if os.name == "nt" else "clear")
                return 

            if answer == correct_answer:
                print(Fore.GREEN + "Correct!")
                break
            else:
                print(Fore.RED + "Incorrect! Try again.")

def PrintMultiplicationTable():
    print("    ", end="")
    for j in range(1, 11):
        print(f"{j:4}", end="")
    print("\n" + "    " + "—" * 42) 

    for i in range(1, 11):
        print(f"{i:2} |", end="") 
        for j in range(1, 11):
            key = f"{i} * {j}"
            result = multiplication_table[key]

            if i == j:
                print(Fore.YELLOW + f"{result:4}" + Fore.RESET, end="")
            else:
                print(f"{result:4}", end="")
        print()
    print()

os.system('cls' if os.name == 'nt' else 'clear')

print(Fore.MAGENTA + "Welcome to the multiplication table trainer!\n")

while True:
    try:
        choice = int(input(Fore.CYAN + "Choose what you want to do:\n1 - test your knowledge of the multiplication table\n2 - view the multiplication table\n3 - exit the program\n"))
    except ValueError:
        print(Fore.RED + "You need to enter a number, either 1, 2 or 3.\n")
        continue

    os.system('cls' if os.name == 'nt' else 'clear')

    if choice == 1:
        print(Fore.GREEN + "Selected training mode.")
        StartTesting()
    elif choice == 2:
        print(Fore.GREEN + "Selected multiplication table view.")
        print(Fore.CYAN + "\nMultiplication Table\n:")
        PrintMultiplicationTable()
        input(Fore.CYAN + "Press Enter to return to the main menu...")
        os.system('cls' if os.name == 'nt' else 'clear')
    elif choice == 3:
        print(Fore.BLUE + "The trainer is closing. See you later!")
        time.sleep(2)
        break
    else:
        print(Fore.RED + "That command does not exist. Please enter 1, 2 or 3.\n")
        continue