from typing import List

from constraint_based_simulator.input_reader.Point import Point


class ReadInput:
    def readFile(self, path: str) -> None:
        pass

    def getStaticPoints(self) -> List[Point]:
        return self.staticPoints

    def getDynamicPoints(self) -> List[Point]:
        return self.dynamicPoints

