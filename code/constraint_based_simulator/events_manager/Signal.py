from typing_extensions import Callable, TypeVarTuple, Generic

VarArgs = TypeVarTuple('VarArgs')


class Signal(Generic[VarArgs]):
    function: Callable

    def connect(self, function: Callable[VarArgs, None]):
        self.function = function

    def signal(self, *args: VarArgs):
        self.function(*args)
