import re
import os
import math
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#membuat language model 'probabilitas kandidat c muncul pada sebuah corpus dokumen.
def words(text):
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('helper/basic-word.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probabilitas `word`."
    return WORDS[word] / N

def correction(word): 
    "koreksi ejaan yang paling mendekati untuk kata yang dituju"
    return (max(candidates(word), key=P))

def candidates(word): 
    "hasilkan kemungkinan koreksi ejaan untuk kata"
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset (subkumpulan) of `words` yang muncul di kamus variabel WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "semua suntingan kata yang berjarak satu suntingan `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # print('after splits = ', splits)
    deletes    = [L + R[1:]               for L, R in splits if R]
    # print('after deletes = ', deletes)
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    # print('after transposes = ', transposes)
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    # print('after replaces = ', replaces)
    inserts    = [L + c + R               for L, R in splits for c in letters]
    # print('after inserts = ', inserts)
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "Semua suntingan yang berjarak dua suntingan dari `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# def update_words_counter(words_list):
#     WORDS.update(words_list)

# #tambah nama ke kamus peter norvig    
# def add_words_to_dict(text):
#     # Split kalimat menjadi kata-kata
#     words_list = re.findall(r'\w+', text.lower())
#     for word in words_list:
#         # Tambahkan kata ke kamus jika belum ada
#         if word not in WORDS:
#             WORDS[word] = 1
#         else:
#             WORDS[word] += 1
#     # Simpan kamus ke file teks
#     with open('helper/basic-word.txt', 'w') as file:
#         file.write('\n'.join(WORDS.keys()))