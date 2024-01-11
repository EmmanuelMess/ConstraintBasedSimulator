from typing_extensions import Callable, TypeVarTuple, Generic, Unpack

VarArgs = TypeVarTuple('VarArgs')


class Signal(Generic[Unpack[VarArgs]]):
    function: Callable

    def connect(self, function: Callable[[Unpack[VarArgs]], None]):
        self.function = function

    def signal(self, *args: Unpack[VarArgs]):
        self.function(*args)
