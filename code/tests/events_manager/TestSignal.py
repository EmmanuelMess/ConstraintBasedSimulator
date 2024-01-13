from typing_extensions import Final

from constraint_based_simulator.events_manager.Signal import Signal


class TestSignal:
    def testBasicSignal(self):
        self.signalCalled = False

        def signalDummyCall():
            self.signalCalled = True

        signal: Signal = Signal()
        signal.connect(signalDummyCall)
        signal.emit()
        assert self.signalCalled

    def testArgumentedSignal(self):
        SEND_VALUE: Final[int] = 8
        self.signalCalled = False

        def signalDummyCall(x: int):
            self.signalCalled = True
            assert x == SEND_VALUE

        signal: Signal[int] = Signal()
        signal.connect(signalDummyCall)
        signal.emit(SEND_VALUE)
        assert self.signalCalled
