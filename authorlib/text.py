"""Text analyzer

    This module helps to make vector from text

"""
import re
import string
import pickle
import pymorphy2
import os
from heapq import nlargest

stopwords = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + "/stopwords.pkl", 'rb'))
normal_forms = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + "/normalforms.pkl", 'rb'))
morph = pymorphy2.MorphAnalyzer()

def dict_nlargest(d, n):
    return dict(nlargest(n, d.items(), key=lambda x: x[1]))

def normalized_words(text):
    """Normalized words

    Takes text and return words of it in normal form and without stopwords
    """
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub('', text)
    tokens = text.split()
    words = []
    for word in tokens:
        word_l = word.lower()
        if word_l not in stopwords:
            if word_l not in normal_forms:
                normal_forms[word_l] = morph.parse(word_l)[0].normal_form
            words.append(normal_forms[word_l])
    return words


def freqs(words, n=2000):
    """Frequency

        Returns top n words and grams frequency
    """
    l = len(words)
    if l < 3:
        return {}, {}, {}
    uni = {}
    bi = {}
    tri = {}
    uni[words[0]] = 1/l
    uni[words[1]] = 1/l
    bi[' '.join(words[0: 2])] = 1/(l - 1)
    for i  in range(2, l):
        a, b, c = words[i], ' '.join(words[i - 1: i + 1]), ' '.join(words[i - 2: i + 1])
        uni[a] = uni.get(a, 0) + 1/l
        bi[b] = bi.get(b, 0) + 1/(l - 1)
        tri[c] = tri.get(c, 0) + 1/(l - 2)
    return dict_nlargest(uni, n), dict_nlargest(bi, n), dict_nlargest(tri, n)


class text_vector:
    """Vector of text

    Vector of text that conteins top 2000 frequencies of
    words, bigramms and trigramms
    """
    def __init__(self, text):
        words = normalized_words(text)
        self.unigramms, self.bigramms, self.trigramms = freqs(words)
        self.author = ""
