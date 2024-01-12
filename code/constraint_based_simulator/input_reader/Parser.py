from typing_extensions import Final

from lark import Lark, tree


class Parser:

    def readFile(self, path: str):
        parser = Lark.open('grammar.lark', rel_to=__file__)

        with open(path) as file:
            print(parser.parse(file.read()))
