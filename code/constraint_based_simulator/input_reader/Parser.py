from typing_extensions import Final

from lark import Lark, ParseTree


class Parser:
    """
    This class uses lark to parse a simulation file and return raw lark structures
    """

    PARSER: Final[Lark] = Lark.open('grammar.lark', rel_to=__file__)

    @staticmethod
    def readFile(path: str) -> ParseTree:
        with open(path, encoding="utf-8") as file:
            return Parser.PARSER.parse(file.read())
