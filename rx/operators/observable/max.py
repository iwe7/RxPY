from rx.core import ObservableBase
from rx.internal.basic import identity

from .min import first_only


def max(source, comparer=None) -> ObservableBase: #  pylint: disable=W0622
    """Returns the maximum value in an observable sequence according to the
    specified comparer.

    Example
    res = source.max()
    res = source.max(lambda x, y:  x.value - y.value)

    Keyword arguments:
    comparer -- {Function} [Optional] Comparer used to compare elements.

    Returns {Observable} An observable sequence containing a single element
    with the maximum element in the source sequence.
    """

    return source.max_by(identity, comparer).map(lambda x: first_only(x))
