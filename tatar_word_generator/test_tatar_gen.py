from tatar_gen import Noun, Verb, Numeral

#noun tests

def test_noun_plural_hard_vowel():
    noun = Noun('китап')
    assert noun.to_plural() == 'китаплар'

def test_noun_plural_nasal():
    noun = Noun('урман')
    assert noun.to_plural() == 'урманнар'

def test_noun_cases():
    noun = Noun('китап')
    assert noun.add_case('of') == 'китапның'
    assert noun.add_case('in') == 'китапта'

# verb tests

def test_verb_stem_extraction():
    verb = Verb("язарга")
    assert verb.stem == "яз"

def test_verb_past_tense():
    verb = Verb("язарга")
    assert verb.add_tense("past", 1, is_plural=False) == "яздым"

# numeral tests

def test_numeral_ordinal():
    numeral = Numeral("өч")
    assert numeral.set_category("ordinal")