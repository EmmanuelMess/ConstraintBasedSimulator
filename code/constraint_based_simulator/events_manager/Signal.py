from __future__ import annotations

from typing_extensions import Callable, TypeVarTuple, Generic, Unpack, List

VarArgs = TypeVarTuple('VarArgs')


class Signal(Generic[Unpack[VarArgs]]):
    """
    Simple mechanism that allows abstracted invocation of callbacks. Multiple callbacks can be attached to a signal
    so that they are all called when the signal is emitted.
    """

    def __init__(self):
        self.functions: List[Callable[..., None]] = []
        """
        Simple mechanism that allows abstracted invocation of callbacks. Multiple callbacks can be attached to a signal
        so that they are all called when the signal is emitted.
        """

    def connect(self, function: Callable[..., None]):
        """
        Add a callback to this Signal
        :param function: callback to call when emited
        """
        self.functions.append(function)

    def emit(self, *args: Unpack[VarArgs]):
        """
        Call all callbacks with the arguments passed
        :param args: arguments for the signal, must be the same type as type parameter
        """
        for function in self.functions:
            if args:
                function(*args)
            else:
                function()
