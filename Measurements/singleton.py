def Singleton(cls):
    instancia = dict()

    def wrapper(*args, **kwargs):
        if cls not in instancia:
            instancia[cls] = cls(*args, **kwargs)
        return instancia[cls]

    return wrapper
