"""argparser

    Module takes your console args and parse them

    parsed_args - object that conteins parsed args
"""
import argparse

parser = argparse.ArgumentParser(prog="author",
                                 description="""Analize books and
                                                tell who is author.""")
subparsers = parser.add_subparsers(help='what to do', metavar="command")
parser_teach = subparsers.add_parser('teach', help='make vectors from books')
parser_teach.add_argument("path", nargs='+', help="path to corpus")
parser_teach.set_defaults(command="teach")
parser_test = subparsers.add_parser('test', help='Test model')
parser_test.add_argument("-p", nargs='+',
                         help="path to corpus, if wasn't teached",
                         default="./Books", dest="path")
parser_test.add_argument("-n", help="""test on new
                                    files from path
                                    (needed to teach first and only
                                    one path will be token)""",
                         action="store_true")
parser_test.set_defaults(command="test")
parser_author = subparsers.add_parser('author',
                                      help='define author of book(s)')
parser_author.add_argument("path", nargs='+', help="path to book(s)")
parser_author.add_argument("-r",
                           help="read books recursively",
                           action="store_true")
parser_author.add_argument("-u",
                           help="take book from web by url",
                           action="store_true")
parser_author.add_argument("-z",
                           help="read books from archive",
                           action="store_true")
parser_author.set_defaults(command="a")
parser.add_argument("-k", type=int, default=1, help="Change k in kNN")

parsed_args = parser.parse_args()
