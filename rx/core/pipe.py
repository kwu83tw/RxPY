from typing import Callable
from functools import reduce
from .observablebase import ObservableBase


def pipe(*operators: Callable[[ObservableBase], ObservableBase]) -> Callable[[ObservableBase], ObservableBase]:
    """Compose multiple operators left to right.

    Composes zero or more operators into a functional composition. The
    operators are composed to left to right. A composition of zero
    operators gives back the source.

    Examples:
        >>> pipe()(source) == source
        >>> pipe(f)(source) == f(source)
        >>> pipe(f, g)(source) == g(f(source))
        >>> pipe(f, g, h)(source) == h(g(f(source)))
    ...

    Returns:
        The composed observable.
    """

    def compose(source: ObservableBase) -> ObservableBase:
        ret = reduce(lambda ops, op: lambda fn: fn(ops(op)),
                     operators,
                     lambda fn: fn(source))
        return ret(lambda x: x)
    return compose
