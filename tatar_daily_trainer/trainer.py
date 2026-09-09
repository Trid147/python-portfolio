import sys
from pathlib import Path
import random
import time
import json
from colorama import Fore, init

init(autoreset=True)

if getattr(sys, 'frozen', False):
    current_path = Path(sys._MEIPASS)
else:
    current_path = Path(__file__).resolve().parent

dicts_dir = current_path / 'dicts'

with open(dicts_dir / 'verbs.json', 'r', encoding='utf-8') as f:
    verbs = json.load(f)

with open(dicts_dir / 'nouns.json', 'r', encoding='utf-8') as f:
    nouns = json.load(f)

with open(dicts_dir / 'adjectives.json', 'r', encoding='utf-8') as f:
    adjectives = json.load(f)

with open(dicts_dir / 'numerals.json', 'r', encoding='utf-8') as f:
    numerals = json.load(f)

with open(dicts_dir / 'pronouns.json', 'r', encoding='utf-8') as f:
    pronouns = json.load(f)

all_words = verbs | nouns | adjectives | numerals | pronouns
random_words = {}

modes = {
    1: all_words,
    2: random_words,
    3: verbs,
    4: nouns,
    5: adjectives,
    6: numerals,
    7: pronouns
}

def start_training(dict):
    keys = list(dict.keys())
    correct_answers = 0

    random.shuffle(keys)

    for key in keys:
        answer = str(input(f'\n{key}: ')).strip().lower()
        if answer == dict[key]:
            print(f'{Fore.GREEN}Correct!')
            correct_answers += 1
            time.sleep(1)
        else:
            print(f'{Fore.RED}Incorrect! Correct answer: {dict[key]}')
            time.sleep(1)

    print(f'{Fore.CYAN}Training is completed. Your correct answers amount: {correct_answers}\n')
    random_words.clear()

def random_words_mode():
    all_words_len = len(all_words)
    while True:
        try:
            count = int(input(f'{Fore.CYAN}Type how many words you want to practice: '))
            if 1 <= count <= all_words_len:
                random_keys = random.sample(list(all_words.keys()), count)
                sampled_dict = {key: all_words[key] for key in random_keys}
                random_words.update(sampled_dict)
                break
            else:
                print(f'{Fore.RED}You can not practice more than {all_words_len} words and less than 1 word!')
        except ValueError:
            print(f'\n{Fore.RED}Please enter a valid number!')
            continue

print(f'{Fore.CYAN}Welcome to Tatar Daily Trainer!\n')

def main():
    while True:
        try:
            mode = int(input(f'{Fore.CYAN}Choose the mode: \n0-exit\n1-all\n2-random\n3-verbs\n4-nouns\n5-adjectives\n6-numerals\n7-pronouns\n-< '))
        except ValueError:
            print(f'\n{Fore.RED}Please enter a valid number!')
            continue

        if mode in modes:
            print(f'\n{Fore.GREEN}Mode chosen successfully!')
            if mode == 2: random_words_mode()
            start_training(modes[mode])
        elif mode == 0:
            print(f'\n{Fore.CYAN}Trainer is closing...')
            sys.exit()
        else:
            print(f'\n{Fore.RED}{mode} is not a correct mode!')

if __name__ == '__main__':
    main()