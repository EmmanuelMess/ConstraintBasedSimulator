from __future__ import annotations

from typing_extensions import Callable, TypeVarTuple, Generic, Unpack

VarArgs = TypeVarTuple('VarArgs')


class Signal(Generic[Unpack[VarArgs]]):
    """
    Simple mechanism that allows abstracted invocation of callbacks. Multiple callbacks can be attached to a signal
    so that they are all called when the signal is emitted.
    """
    function: Callable | None = None

    def connect(self, function: Callable[[Unpack[VarArgs]], None]):
        """
        Add a callback to this Signal
        :param function: callback to call when emited
        """
        self.function = function

    def emit(self, *args: Unpack[VarArgs]):
        """
        Call all callbacks with the arguments passed
        :param args: arguments for the signal, must be the same type as type parameter
        """
        if self.function is not None:
            self.function(*args)
