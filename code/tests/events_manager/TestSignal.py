from typing_extensions import Final

from constraint_based_simulator.events_manager.Signal import Signal


class TestSignal:  # pylint: disable=missing-class-docstring
    def testArgumentedSignal(self) -> None:  # pylint: disable=missing-function-docstring
        SEND_VALUE: Final[int] = 8
        self.signalCalled = False

        def signalCallWithParam(x: int) -> None:  # pylint: disable=missing-function-docstring
            self.signalCalled = True
            assert x == SEND_VALUE

        signal: Signal[int] = Signal[int]()
        signal.connect(signalCallWithParam)
        signal.emit(SEND_VALUE)
        assert self.signalCalled
