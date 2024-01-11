class SingletonMeta(type):
    """
    Metaclass for implementing the Singleton design pattern.

    This metaclass ensures that only one instance of a class is created and
    provides a global point of access to that instance.

    Usage:
    class MyClass(metaclass=SingletonMeta):
        # class definition

    Note:
    This metaclass should be used as the metaclass of the class that needs to
    be a singleton.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]