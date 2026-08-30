# Tatar Morphological Generator

A robust Python-based tool designed to automatically generate correct grammatical forms for Tatar nouns and verbs. The system natively handles the complexities of Tatar morphonology, including the **Law of Vowel Harmony (Vowel Synharmonism)** and **consonant alternation rules**.

## ✨ Features

- **Automated Vowel Harmony:** Dynamically detects whether a word is front-vocalic (soft) or back-vocalic (hard) to apply the correct allomorphs.
- **Noun Morphology Support:**
  - Pluralization using correct suffixes (`-лар/-ләр`, `-нар/-нәр`) based on phonetic environment.
  - Full declension across 5 oblique cases (Genitive, Accusative, Dative/Directive, Locative, Ablative).
  - Possessive suffixation for all persons and numbers, featuring automatic stem mutations (e.g., `п -> б`, `к -> г`).
- **Verb Morphology Support:**
  - Smart stem extraction from standard infinitive endings (`-арга/-әргә`, `-ырга/-ергә`, `-рга/-ргә`).
  - Negative form generation (`-ма/-мә`).
  - Comprehensive tense conjugation (Past, Present, Definite Future, Indefinite Future) mapped to all personal pronouns.
- **Interactive CLI:** An intuitive, color-coded command-line interface powered by `colorama`.

## 🛠 Installation & Usage

### Prerequisites
Make sure you have Python 3.6+ installed. 

### Setup
1. Clone the repository or download the `tatar_gen.py` file.
2. Install the required dependency for console styling:
   ```bash
   pip install colorama
   ```

### Execution
Run the script directly from your terminal:
```bash
python tatar_gen.py
```

## 🚀 Usage Examples

Once launched, the interactive CLI will guide you to select a Part of Speech (`noun` or `verb`) and pass configurations via a comma-separated string.

### Noun Conjugation
Argument format: `[plural], [possessive], [case]`

* **Example 1 (Book):**
  - Input: `Китап`
  - Arguments: `true, my, in` *(Plural, My, Locative case)*
  - Output: `Китапларымда`

* **Example 2 (Kazan):**
  - Input: `Казан`
  - Arguments: `false, none, from` *(Singular, No possessive, Ablative case)*
  - Output: `Казаннан`

> **Supported Cases:** `of` (Genitive), `acc` (Accusative), `to` (Dative), `in` (Locative), `from` (Ablative).  
> **Supported Possessives:** `my`, `your`, `his`/`her`, `our`, `your_pl`, `their`.

### Verb Conjugation
Argument format: `[negative], [tense], [person]`

* **Example 1 (To write):**
  - Input: `язарга`
  - Arguments: `false, present, i` *(Present tense, 1st person singular)*
  - Output: `Язам`

* **Example 2 (To come):**
  - Input: `килергә`
  - Arguments: `true, past, we` *(Negative, Past tense, 1st person plural)*
  - Output: `Килелмәдек`

> **Supported Tenses:** `past`, `present`, `fut_def` (Definite Future), `fut_indef` (Indefinite Future).  
> **Supported Persons:** `i`, `you`, `he`/`she`, `we`, `you_pl`, `they`.

## 📈 Roadmap

- [ ] Implement the `numeral` part of speech module.
- [ ] Expand the verb database to support exceptional vowel stem extractions.
- [ ] Add unit tests for complex phonetic edge-cases.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
