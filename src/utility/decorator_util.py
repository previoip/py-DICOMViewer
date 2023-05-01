def inject_decorator_to_class(decorator, cls=None):
    if cls is None:
        return lambda cls: inject_decorator_to_class(decorator, cls)

    class Decoratable(cls):
        def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)

        def __getattribute__(self, item):
            value = object.__getattribute__(self, item)
            if callable(value):
                return decorator(value)
            return value

    return Decoratable