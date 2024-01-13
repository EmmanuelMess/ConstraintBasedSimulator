from typing_extensions import Final

from lark import Lark, ParseTree


PARSER: Final[Lark] = Lark.open('grammar.lark', rel_to=__file__)


def readFile(path: str) -> ParseTree:
    """
    Use lark to parse a simulation file and return raw lark structures
    """

    with open(path, encoding="utf-8") as file:
        return PARSER.parse(file.read())
