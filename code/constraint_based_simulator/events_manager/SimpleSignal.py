from __future__ import annotations

from typing_extensions import List, Callable


class SimpleSignal:
    """
    HACK for signals with no parameters. See Signal for a generic version.
    See https://stackoverflow.com/questions/77820589/type-parameter-list-cannot-be-emtpy-for-typevartuple for an
    explanation
    """

    def __init__(self) -> None:
        self.functions: List[Callable[[], None]] = []
        """
        Simple mechanism that allows abstracted invocation of callbacks. Multiple callbacks can be attached to a signal
        so that they are all called when the signal is emitted.
        """

    def connect(self, function: Callable[[], None]) -> None:
        """
        Add a callback to this SimpleSignal
        :param function: callback to call when emited
        """
        self.functions.append(function)

    def emit(self) -> None:
        """
        Call all callbacks
        """
        for function in self.functions:
            function()
