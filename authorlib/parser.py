#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import urllib.request as url
from urllib.error import HTTPError
from html.parser import HTMLParser
from urllib.request import urlopen
from gzip import decompress

class Parser(HTMLParser):
    """Parser for retrieving text of page."""

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ''

    def handle_data(self, data):
        data = data.strip()
        self.text += data

    def parse(self, page):
        """Return text of article."""

        self.feed(page)
        return self.text


def load(link):
    try:
        response = urlopen(link)
    except HTTPError:
        return None
    else:
        if 'Content-Encoding' in response.headers:
            return decompress(response.read()).decode(response.headers.get_content_charset())
        else:
            return response.read().decode(response.headers.get_content_charset())


def get_text(page):
    """Return text of page."""
    return Parser().parse(page)

def save_book(url, path):
    open(path + "/book", 'w', encoding="cp1251").write(get_text(load(url)))
    return path + "/book"

if __name__ == '__main__':
    main()
