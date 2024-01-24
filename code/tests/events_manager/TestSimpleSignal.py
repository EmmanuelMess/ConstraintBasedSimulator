from constraint_based_simulator.events_manager.SimpleSignal import SimpleSignal


class TestSimpleSignal:
    def testBasicSignal(self) -> None:
        self.signalCalled = False

        def signalEmptyCall():
            self.signalCalled = True

        signal: SimpleSignal = SimpleSignal()
        signal.connect(signalEmptyCall)
        signal.emit()
        assert self.signalCalled
