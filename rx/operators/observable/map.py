from typing import Callable, Any

from rx import Observable, Observer, AnonymousObservable
from rx.core import Disposable


def map(mapper: Callable[[Any], Any], source: Observable) -> Observable:
    """Project each element of an observable sequence into a new form.

    1 - source.map(lambda value: value * value)

    Keyword arguments:
    mapper -- A transform function to apply to each source element; the
        second parameter of the function represents the index of the
        source element.

    Returns an observable sequence whose elements are the result of
    invoking the transform function on each element of the source.
    """

    def subscribe(observer: Observer) -> Disposable:
        def on_next(value):
            try:
                result = mapper(value)
            except Exception as err:  # pylint: disable=W0703
                observer.on_error(err)
            else:
                observer.on_next(result)

        return source.subscribe_callbacks(on_next, observer.on_error, observer.on_completed)
    return AnonymousObservable(subscribe)


def map_indexed(selector: Callable[[Any, int], Any], source: Observable) -> Observable:
    """Project each element of an observable sequence into a new form
    by incorporating the element's index.

    1 - source.map(lambda value, index: value * value + index)

    Keyword arguments:
    selector -- A transform function to apply to each source element;
        the second parameter of the function represents the index of the
        source element.

    Returns an observable sequence whose elements are the result of
    invoking the transform function on each element of the source.
    """

    def subscribe(observer: Observer) -> Disposable:
        count = 0

        def on_next(value):
            nonlocal count

            try:
                result = selector(value, count)
            except Exception as err:  # By design. pylint: disable=W0703
                observer.on_error(err)
            else:
                count += 1
                observer.on_next(result)

        return source.subscribe_callbacks(on_next, observer.on_error, observer.on_completed)
    return AnonymousObservable(subscribe)
