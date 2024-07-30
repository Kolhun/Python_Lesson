import inspect


def introspection_info(obj):
    info = {}
    info['Тип объекта'] = type(obj).__name__
    info['Атрибуты объекта'] = [attr for attr in dir(obj) if
                                not callable(getattr(obj, attr)) and not attr.startswith("__")]
    info['Методы объекта'] = [method for method in dir(obj) if callable(getattr(obj, method))]
    info['Модуль'] = inspect.getmodule(obj).__name__ if inspect.getmodule(obj) else None
    return info


number_info = introspection_info(42)
print(number_info)
