from constraint_based_simulator.common.Singleton import Singleton


class TestSingleton:  # pylint: disable=missing-class-docstring
    def testSimpleSingleton(self) -> None:
        class SampleSingleton(metaclass=Singleton):  # pylint: disable=missing-class-docstring
            def __init__(self) -> None:  # pylint: disable=missing-function-docstring
                self._data: int = 0

            def setData(self, newData: int) -> None:  # pylint: disable=missing-function-docstring
                self._data = newData

            def getData(self) -> int:  # pylint: disable=missing-function-docstring
                return self._data

        SampleSingleton().setData(3)

        assert SampleSingleton().getData() == 3

        SampleSingleton().setData(4)

        assert SampleSingleton().getData() == 4
