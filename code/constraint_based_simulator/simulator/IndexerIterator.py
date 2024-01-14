from typing import List, TypeVar

from constraint_based_simulator.simulator.IndexedElement import IndexedElement


T = TypeVar('T', bound=IndexedElement)


class IndexerIterator(List[T]):
    def __init__(self, baseIterable: List[T]):
        super().__init__(baseIterable)

        for index, element in enumerate(self):
            element.index = index
