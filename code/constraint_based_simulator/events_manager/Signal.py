from __future__ import annotations

from typing_extensions import Callable, Generic, List, ParamSpec

VarArgs = ParamSpec('VarArgs')


class Signal(Generic[VarArgs]):
    """
    Simple mechanism that allows abstracted invocation of callbacks. Multiple callbacks can be attached to a signal
    so that they are all called when the signal is emitted.
    """

    def __init__(self) -> None:
        self.functions: List[Callable[VarArgs, None]] = []
        """
        Simple mechanism that allows abstracted invocation of callbacks. Multiple callbacks can be attached to a signal
        so that they are all called when the signal is emitted.
        """

    def connect(self, function: Callable[VarArgs, None]) -> None:
        """
        Add a callback to this Signal
        :param function: callback to call when emited
        """
        self.functions.append(function)

    def emit(self, *args: VarArgs.args, **kwargs: VarArgs.kwargs) -> None:
        """
        Call all callbacks with the arguments passed
        :param args: arguments for the signal, must be the same type as type parameter
        """
        for function in self.functions:
            function(*args, **kwargs)
