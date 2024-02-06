from dataclasses import dataclass


@dataclass
class IndexedElement:
    """
    Special base class for elements of IndexedIterator
    """
    index: int
