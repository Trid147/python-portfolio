import os
from colorama import init, Fore, Style

init(autoreset=True)

def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

class TatarWord:
    def __init__(self, word):
        self.original_word = word
        self.word = word.lower()
        
        self.hard_vowels = ['а', 'у', 'о', 'ы']
        self.soft_vowels = ['ә', 'ү', 'ө', 'е', 'и']
        
        self.is_hard = self._analyze_harmony()

    def _analyze_harmony(self):
        for char in reversed(self.word):
            if char in self.hard_vowels:
                return True
            elif char in self.soft_vowels:
                return False
        return True

class Noun(TatarWord):
    def __init__(self, word):
        super().__init__(word)
     
        self.nasal_consonants = ['м', 'н', 'ң']
        self.voiceless_consonants = ['п', 'к', 'т', 'с', 'ш', 'ч', 'ц', 'х', 'һ', 'ф', 'щ']

    def to_plural(self):
        last_char = self.word[-1]

        if last_char in self.nasal_consonants:
            suffix = "нар" if self.is_hard else "нәр"
        else:
            suffix = "лар" if self.is_hard else "ләр"

        plural_word = self.word + suffix
        if self.original_word.istitle():
            return plural_word.capitalize()
        return plural_word

    def add_possession(self, person, is_plural_owner=False):
        last_char = self.word[-1]
        is_vowel_ending = last_char in self.hard_vowels or last_char in self.soft_vowels
        
        base_word = self.word

        if not is_vowel_ending:
            if last_char == 'п':
                base_word = base_word[:-1] + 'б'
            elif last_char == 'к':
                base_word = base_word[:-1] + 'г'

        suffix = ""

        if person == 1:
            if not is_plural_owner: 
                if is_vowel_ending:
                    suffix = "м"
                else:
                    suffix = "ым" if self.is_hard else "ем"
            else:
                if is_vowel_ending:
                    suffix = "быз" if self.is_hard else "без"
                else:
                    suffix = "ыбыз" if self.is_hard else "ебез"

        elif person == 2:
            if not is_plural_owner:
                if is_vowel_ending:
                    suffix = "ң"
                else:
                    suffix = "ың" if self.is_hard else "ең"
            else:
                if is_vowel_ending:
                    suffix = "гыз" if self.is_hard else "гез"
                else:
                    suffix = "ыгыз" if self.is_hard else "егез"

        elif person == 3:
            if is_vowel_ending:
                suffix = "сы" if self.is_hard else "се"
            else:
                suffix = "ы" if self.is_hard else "е"

        result_word = base_word + suffix

        if self.original_word.istitle():
            return result_word.capitalize()
        return result_word

    def add_case(self, case_type):
        last_char = self.word[-1]
        
        is_voiceless = last_char in self.voiceless_consonants
        is_nasal = last_char in self.nasal_consonants
        
        suffix = ""
        
        if case_type == "of": 
            suffix = "ның" if self.is_hard else "нең"
        elif case_type == "acc": 
            suffix = "ны" if self.is_hard else "не"
        elif case_type == "to": 
            if is_voiceless:
                suffix = "ка" if self.is_hard else "кә"
            else:
                suffix = "га" if self.is_hard else "гә"
        elif case_type == "in": 
            if is_voiceless:
                suffix = "та" if self.is_hard else "тә"
            else:
                suffix = "да" if self.is_hard else "дә"
        elif case_type == "from":
            if is_voiceless:
                suffix = "тан" if self.is_hard else "тән"
            elif is_nasal:
                suffix = "нан" if self.is_hard else "нән"
            else:
                suffix = "дан" if self.is_hard else "дән"
        else:
            return self.original_word
            
        result_word = self.word + suffix
        if self.original_word.istitle():
            return result_word.capitalize()
        return result_word


class Verb(TatarWord):
    def __init__(self, word):
        super().__init__(word)
        self.voiceless_consonants = ['п', 'к', 'т', 'с', 'ш', 'ч', 'ц', 'х', 'һ', 'ф', 'щ']
        self.stem = self._extract_stem()

    def _extract_stem(self):
        """Извлекает корень (основу) глагола из инфинитива."""
        w = self.word
   
        vowel_stems = [
            'сөйлә', 'эшлә', 'аша', 'яшә', 'уйна', 
            'йокла', 'аңла', 'кара', 'сора', 'телә', 
            'сайла', 'җырла', 'башла', 'уйла', 'аңла',
            'булыш' # можно пополнять по мере изучения
        ]
     
        for stem in vowel_stems:
            if w == stem + 'ргә' or w == stem + 'рга':
                return stem
            
        if w.endswith("ырга") or w.endswith("ергә"):
            return w[:-4]
        elif w.endswith("арга") or w.endswith("әргә"):
            return w[:-4]
        elif w.endswith("рга") or w.endswith("ргә"):
            return w[:-3]
            
        return w

    def make_negative(self):
        suffix = "ма" if self.is_hard else "мә"
        self.stem += suffix

    def add_tense(self, tense, person, is_plural=False):
        last_char = self.stem[-1]
        is_voiceless = last_char in self.voiceless_consonants
        is_vowel = last_char in self.hard_vowels or last_char in self.soft_vowels
        
        result = self.stem

        if tense == "past":
            if is_voiceless:
                tense_suffix = "ты" if self.is_hard else "те"
            else:
                tense_suffix = "ды" if self.is_hard else "де"
            
            person_suffix = ""
            if person == 1:
                person_suffix = "к" if is_plural else "м"
            elif person == 2:
                person_suffix = ("гыз" if self.is_hard else "гез") if is_plural else "ң"
            elif person == 3:
                person_suffix = ("лар" if self.is_hard else "ләр") if is_plural else ""
            
            result += tense_suffix + person_suffix

        elif tense == "present":
            if is_vowel:
                if last_char == 'а':
                    result = result[:-1] + "ый"
                elif last_char == 'ә':
                    result = result[:-1] + "и"
                else:
                    result += "й"
            else:
                result += "а" if self.is_hard else "ә"
            
            person_suffix = ""
            if person == 1:
                person_suffix = ("быз" if self.is_hard else "без") if is_plural else "м"
            elif person == 2:
                person_suffix = ("сыз" if self.is_hard else "сез") if is_plural else ("сың" if self.is_hard else "сең")
            elif person == 3:
                person_suffix = ("лар" if self.is_hard else "ләр") if is_plural else ""
            
            result += person_suffix

        elif tense == "fut_def":
            if is_vowel:
                result += "ячак" if self.is_hard else "ячәк"
            else:
                result += "ачак" if self.is_hard else "әчәк"
            
            person_suffix = ""
            if person == 1:
                person_suffix = ("быз" if self.is_hard else "без") if is_plural else ("мын" if self.is_hard else "мен")
            elif person == 2:
                person_suffix = ("сыз" if self.is_hard else "сез") if is_plural else ("сың" if self.is_hard else "сең")
            elif person == 3:
                person_suffix = ("лар" if self.is_hard else "ләр") if is_plural else ""
                
            result += person_suffix

        elif tense == "fut_indef":
            if is_vowel:
                result += "р"
            else:
                result += "ыр" if self.is_hard else "ер" 
            
            person_suffix = ""
            if person == 1:
                person_suffix = ("быз" if self.is_hard else "без") if is_plural else ("мын" if self.is_hard else "мен")
            elif person == 2:
                person_suffix = ("сыз" if self.is_hard else "сез") if is_plural else ("сың" if self.is_hard else "сең")
            elif person == 3:
                person_suffix = ("лар" if self.is_hard else "ләр") if is_plural else ""
                
            result += person_suffix

        if self.original_word.istitle():
            return result.capitalize()
        return result

class Numeral(TatarWord):
    def __init__(self, word):
        super().__init__(word)
        self.last_char = self.word[-1]
        self.suffix = ""

    vowels = ['а', 'ә', 'е', 'ё', 'и', 'о', 'ө', 'у', 'ү', 'ы', 'э', 'ю', 'я']
    consonants = ['б', 'в', 'г', 'д', 'ж', 'җ', 'з', 'й', 'к', 'л', 'м', 'н', 'ң', 'п', 'р', 'с', 'т', 'ф', 'х', 'һ', 'ц', 'ч', 'ш', 'щ']

    def set_category(self, category):
        if category == 'ordinal':
            return self.set_ordinal()
        elif category == 'collective':
            return self.set_collective()
        elif category == 'distributive':
            return self.set_distributive()

    def set_ordinal(self):
        if self.last_char in self.vowels:
            self.suffix = "нчы" if self.is_hard else "нче"
        elif self.last_char in self.consonants:
            self.suffix = "ынчы" if self.is_hard else "енче"

        result_word = self.word + self.suffix
        if self.original_word.istitle():
            return result_word.capitalize()
        return result_word

    def set_collective(self):
        base_word = self.word

        if self.last_char in self.vowels:
            base_word = base_word[:-1]

        self.suffix = "ау" if self.is_hard else "әү"

        result_word = base_word + self.suffix
        if self.original_word.istitle():
            return result_word.capitalize()
        return result_word

    def set_distributive(self):
        if self.last_char in self.vowels:
            self.suffix = "шар" if self.is_hard else "шәр"
        elif self.last_char in self.consonants:
            self.suffix = "ар" if self.is_hard else "әр"

        result_word = self.word + self.suffix
        if self.original_word.istitle():
            return result_word.capitalize()
        return result_word
            


if __name__ == "__main__":
    print(Fore.GREEN + "======================================================")
    print(Fore.WHITE + "Добро пожаловать в Татарский Морфологический Генератор!")
    print(Fore.RED + "======================================================\n")

    while True:
        print("Доступные части речи: noun, verb, numeral")
        pos = input("Введите часть речи (или 'exit' для выхода): ").strip().lower()

        if pos == 'exit':
            ClearConsole()
            print(Fore.CYAN + "Сау бул! (До свидания!)")
            break

        if pos == "noun":
            word_input = input("Введите существительное: ").strip()
            
            print("\nВведите аргументы через запятую: [множ. число], [принадлежность], [падеж]")
            print("Пример: true, my, in")
            args_input = input(Fore.CYAN + "> ").strip()

            args = [arg.strip().lower() for arg in args_input.split(",")]
 
            plural_arg = args[0] if len(args) > 0 else "none"
            poss_arg = args[1] if len(args) > 1 else "none"
            case_arg = args[2] if len(args) > 2 else "none"

            current_word = Noun(word_input)
            result = current_word.original_word

            if plural_arg == "true":
                result = current_word.to_plural()
                current_word = Noun(result)

            if poss_arg not in ["none", "", "false"]:
                person_map = {
                    "my": (1, False),
                    "your": (2, False),
                    "his": (3, False),
                    "her": (3, False),
                    "our": (1, True),
                    "your_pl": (2, True),
                    "their": (3, False)
                }

                if poss_arg in person_map:
                    person, is_pl = person_map[poss_arg]
                    result = current_word.add_possession(person, is_plural_owner=is_pl)
                    current_word = Noun(result)
                else:
                    print(Fore.YELLOW + f"Неизвестный аргумент принадлежности '{poss_arg}'")

            if case_arg not in ["none", "", "false"]:
                valid_cases = ["of", "to", "acc", "in", "from"]
                
                if case_arg in valid_cases:
                    result = current_word.add_case(case_arg)
                    current_word = Noun(result)
                else:
                    print(Fore.YELLOW + f"Неизвестный падеж '{case_arg}'")

            print(Fore.GREEN + f"\nГотовое слово: {result}\n")
            input("Нажмите любую клавишу чтобы продолжить...")
            ClearConsole()

        elif pos == "verb":
            word_input = input("Введите глагол (инфинитив, например: язарга, килергә): ").strip()
            
            print("\nВведите аргументы через запятую: [отрицание], [время], [лицо]")
            print("Пример: false, present, i")
            args_input = input(Fore.CYAN + "> ").strip()

            args = [arg.strip().lower() for arg in args_input.split(",")]
 
            neg_arg = args[0] if len(args) > 0 else "none"
            tense_arg = args[1] if len(args) > 1 else "none"
            person_arg = args[2] if len(args) > 2 else "none"

            current_verb = Verb(word_input)

            if neg_arg == "true":
                current_verb.make_negative()

            if tense_arg not in ["none", "", "false"] and person_arg not in ["none", "", "false"]:
                person_map = {
                    "i": (1, False),
                    "you": (2, False),
                    "he": (3, False),
                    "she": (3, False),
                    "we": (1, True),
                    "you_pl": (2, True),
                    "they": (3, True)
                }

                if person_arg in person_map:
                    person, is_pl = person_map[person_arg]
                    result = current_verb.add_tense(tense_arg, person, is_plural=is_pl)
                else:
                    print(Fore.YELLOW + f"Неизвестное лицо '{person_arg}'")
                    result = current_verb.stem
            else:
                result = current_verb.stem
                if current_verb.original_word.istitle():
                    result = result.capitalize()

            print(Fore.GREEN + f"\nГотовое слово: {result}")
            input("Нажмите любую клавишу чтобы продолжить...")
            ClearConsole()

        elif pos == "numeral":
            word_input = input("Введите числительное: ").strip()
            
            print("\nВведите аргументы через запятую: [разряд]")
            print("Пример: distributive")
            args_input = input(Fore.CYAN + "> ").strip()

            args = [arg.strip().lower() for arg in args_input.split(",")]
 
            category_arg = args[0] if len(args) > 0 else "none"

            current_numeral = Numeral(word_input)

            result = current_numeral.original_word

            if category_arg:
                category_map = ["ordinal", "collective", "distributive"]

                if category_arg in category_map:
                    print(category_arg)
                    result = current_numeral.set_category(category_arg)


            print(Fore.GREEN + f"\nГотовое слово: {result}")
            input("Нажмите любую клавишу чтобы продолжить...")
            ClearConsole()
        else:
            print(Fore.RED + "Неизвестная часть речи. Попробуйте снова.\n")