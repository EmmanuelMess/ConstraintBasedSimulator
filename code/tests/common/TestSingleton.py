from constraint_based_simulator.common.Singleton import Singleton


class TestSingleton:
    def testSimpleSingleton(self):
        class SampleSingleton(metaclass=Singleton):
            def __init__(self):
                self._data: int = 0

            def setData(self, newData: int):
                self._data = newData

            def getData(self) -> int:
                return self._data

        SampleSingleton().setData(3)

        assert SampleSingleton().getData() == 3

        SampleSingleton().setData(4)

        assert SampleSingleton().getData() == 4
