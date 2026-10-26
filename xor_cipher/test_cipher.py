from main import encrypt_text

def test_text_encryption():
    text = 'i often skip lessons in the school'
    key = 'qwerty123'
    assert encrypt_text(text, key) == 'G# 24 87 10 20 0 28 95 18 64 26 30 21 82 24 28 66 65 92 31 4 69 27 26 89 69 90 86 81 4 6 26 27 22 93'

def test_decryption():
    text = 'G# 64 35 87 84 33 79 77 57 3 72 96 71 78 46 87 1 40 66 87 37 3 64 96 79 78 52 3 78 38 3 76 47 77 68 57'
    key = '!@#'
    assert encrypt_text(text, key) == 'actually i dont have a lot of money'