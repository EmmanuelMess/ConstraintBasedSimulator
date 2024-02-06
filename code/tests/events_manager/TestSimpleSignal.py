from constraint_based_simulator.events_manager.SimpleSignal import SimpleSignal


class TestSimpleSignal:  # pylint: disable=missing-class-docstring
    def testBasicSignal(self) -> None:  # pylint: disable=missing-function-docstring
        self.signalCalled = False

        def signalEmptyCall() -> None:  # pylint: disable=missing-function-docstring
            self.signalCalled = True

        signal: SimpleSignal = SimpleSignal()
        signal.connect(signalEmptyCall)
        signal.emit()
        assert self.signalCalled
