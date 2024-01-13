from typing_extensions import Callable, TypeVarTuple, Generic, Unpack

VarArgs = TypeVarTuple('VarArgs')


class Signal(Generic[Unpack[VarArgs]]):
    """
    Simple mechanism that allows abstracted invocation of callbacks. Multiple callbacks can be attached to a signal
    so that they are all called when the signal is emitted.
    """
    function: Callable

    def connect(self, function: Callable[[Unpack[VarArgs]], None]):
        """
        Add a callback to this Signal
        :param function: callback to call when emited
        """
        self.function = function

    def signal(self, *args: Unpack[VarArgs]):  # TODO change to emit
        """
        Call all callbacks with the arguments passed
        :param args: arguments for the signal, must be the same type as type parameter
        """
        self.function(*args)
