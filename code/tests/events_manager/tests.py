import unittest

from typing_extensions import Final

from constraint_based_simulator.events_manager.Signal import Signal


class SignalTest(unittest.TestCase):
    def testBasicSignal(self):
        self.signalCalled = False

        def signalDummyCall():
            self.signalCalled = True

        signal: Signal = Signal()
        signal.connect(signalDummyCall)
        signal.signal()
        self.assertTrue(self.signalCalled)

    def testArgumentedSignal(self):
        SEND_VALUE: Final[int] = 8
        self.signalCalled = False

        def signalDummyCall(x: int):
            self.signalCalled = True
            self.assertEqual(x, SEND_VALUE)

        signal: Signal[int] = Signal()
        signal.connect(signalDummyCall)
        signal.signal(SEND_VALUE)
        self.assertTrue(self.signalCalled)


if __name__ == '__main__':
    unittest.main()
