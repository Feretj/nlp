#!/usr/bin/python
"""Mainfile of author program

    Conteins realization of console interface and meant to use only in console
"""

import argparser
from tempfile import mkdtemp
from shutil import rmtree, unpack_archive
import os
from authorlib.parser import save_book
import authorlib
tmpdir = mkdtemp()
realpath = os.path.dirname(os.path.realpath(__file__))

def teach(path_to_books):
    """
    Realization of console "teach" command
    """
    data = {}
    for p in path_to_books:
        data.update(authorlib.make_data(p))
    authorlib.save_data(data, realpath)
    print("Data saved to data.pkl")


def test(path, k, n):
    """
    Realization of console "test" command
    """
    if n:
        try:
            data = authorlib.load_data(realpath)
        except FileNotFoundError:
            print("There no binary. Maybe you need to teach first.")
            return
        data_test = authorlib.make_data(path)
        print("Quality:", str(authorlib.test_data(data, data_test)*100) + '%')

    elif "data.pkl" in next(os.walk(realpath))[2]:
        data = authorlib.load_data(realpath)
        print("Quality:", str(authorlib.test_data_itself(data)*100) + '%')
    else:
        teach(path)
        test(path, k)


def author(path, k, r, url=False):
    """
    Realization of console "author" command
    """
    try:
        data = authorlib.load_data(realpath)
    except FileNotFoundError:
        print("There no binary. Maybe you need to teach first.")
        return
    if r and url:
        print("Sorry, but we can't download web pages recursively")
    elif r:
        for p in path:
            try:
                vectors_test = authorlib.make_vectors(p)
            except:
                print("Something went wrong, while loading directory", p)
            else:
                vectors = authorlib.utils.data_to_vectors(data)
                for v in vectors_test:
                    print("Path:", v.author)
                    print("Author", authorlib.knearneighbours.knn(vectors, v, k))
    elif url:
        for url in path:
            try:
                book = open(save_book(url, tmpdir), encoding="cp1251").read()
            except:
                print("Couldn't load",'"' + url + '"')
            else:
                print("URL:", url)
                print("Author:", authorlib.determine_author(data, book))
    else:
        for p in path:
            try:
                print("Path:", p)
                print("Author:", authorlib.determine_author(data,
                      open(p, 'r', encoding="cp1251").read()))
            except IsADirectoryError:
                print('"' + p + '"', "is a directory. Maybe you forgot -r option.")
            except FileNotFoundError:
                print("No such file", '"' + p + '"')

def archive(path, k, r, url=False):
    if url:
        print("We can't read archive from web")
    elif r:
        print("We can't read archive recursively")
    else:
        for p in path:
            try:
                unpack_archive(p, tmpdir + "/archive")
            except:
                print("Path:", p, '\n', "Can't read archive")
            else:
                author([tmpdir + "/archive"], k, True, url)
                rmtree(tmpdir + "/archive")


if __name__ == "__main__":
    args = argparser.parsed_args
    if "command" not in args:
        print("usage: author [-h] [-k K] command ...")
    elif args.command == "teach":
        teach(args.path)
    elif args.command == "test":
        test(args.path, args.k, args.n)
    else:
        if args.z:
            archive(args.path, args.k, args.r, args.u)
        else:
            author(args.path, args.k, args.r, args.u)
rmtree(tmpdir, ignore_errors=True)
