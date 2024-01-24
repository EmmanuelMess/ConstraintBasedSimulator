from typing_extensions import Final

from constraint_based_simulator.events_manager.Signal import Signal


class TestSignal:
    def testArgumentedSignal(self):
        SEND_VALUE: Final[int] = 8
        self.signalCalled = False

        def signalCallWithParam(x: int):
            self.signalCalled = True
            assert x == SEND_VALUE

        signal: Signal[int] = Signal[int]()
        signal.connect(signalCallWithParam)
        signal.emit(SEND_VALUE)
        assert self.signalCalled
