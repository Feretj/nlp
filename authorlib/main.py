from . import knearneighbours
from . import text
from . import utils
from os.path import join
import os
import pickle

realpath = os.path.dirname(os.path.realpath(__file__))

def make_data(path):
    """Make text vectors from folder"""
    data = {}
    authors = next(os.walk(path))[1]
    for author in authors:
        for root, dirs, files in os.walk(join(path, author)):
            data[author] = []
            for f in files:
                print("Reading", '"' + join(root, f) + '"')
                book = open(join(root, f), encoding="cp1251").read()
                v = text.text_vector(book)
                v.author = author
                data[author].append(v)
    return data

def save_data(data, path=realpath):
    pickle.dump(data, open(path + "/data.pkl", 'wb'))

def load_data(path=realpath):
    return pickle.load(open(path + "/data.pkl", 'rb'))

def test_data_itself(data, percent_test=70, k=1, u=2.002183406113537, b=1.2890829694323145, t=0.1890829694323144):
    pt = percent_test/100
    vectors = []
    vectors_test = []
    for author in data:
        l = int(len(data[author])*pt)
        vectors.extend(data[author][:l])
        vectors_test.extend(data[author][l:])
    right = 0
    for v in vectors_test:
        right += knearneighbours.knn(vectors, v, k, u, b, t) == v.author
    return right/len(vectors_test)

def test_data(data, data_test, k=1, u=2.002183406113537, b=1.2890829694323145, t=0.1890829694323144):
    vectors = utils.data_to_vectors(data)
    vectors_test = utils.data_to_vectors(data_test)
    right = 0
    for v in vectors_test:
        right += knearneighbours.knn(vectors, v, k, u, b, t) == v.author
    return right/len(vectors_test)

def gradient_descent(data, k=1):
    u_old = 0
    b_old = 0
    t_old = 0
    u = 2
    b = 1.3
    t = 0.2
    gamma = 0.1
    precision = 0.01
    while abs(u - u_old) > precision and abs(b - b_old) > precision and abs(t - t_old) > precision:
        q = test_data_itself(data, k=k, u=u, b=b, t=t)
        if abs(u - u_old) > precision:
            u_old = u
            u = u + gamma*(test_data_itself(data, k=k, u=(u + 0.2), b=b, t=t) - q)/0.2
        if abs(b - b_old) > precision:
            b_old = b
            b = b + gamma*(test_data_itself(data, k=k, u=u, b=(b + 0.2), t=t) - q)/0.2
        if abs(t - t_old) > precision:
            t_old = t
            t = t + gamma*(test_data_itself(data, k=k, u=u, b=b, t=(t + 0.2)) - q)/0.2

    return (u, b, t)

def make_vectors(path):
    vectors = []
    for root, dirs, files in os.walk(path):
        for f in files:
            print("Reading", '"' + join(root, f) + '"')
            book = open(join(root, f), encoding="cp1251").read()
            v = text.text_vector(book)
            v.author = join(root, f)
            vectors.append(v)
    return vectors

def determine_author(data, book, k=1, u=2.002183406113537, b=1.2890829694323145, t=0.1890829694323144):
    vectors = utils.data_to_vectors(data)
    return knearneighbours.knn(vectors, text.text_vector(book), k)
