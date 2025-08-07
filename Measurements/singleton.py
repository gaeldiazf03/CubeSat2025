from threading import Lock


def Singleton(cls):
    _instances: dict = {}
    _lock:      Lock = Lock()

    def wrapper(*args, **kwargs):
        if cls not in _instances:
            with _lock:
                if cls not in _instances:
                    _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return wrapper
