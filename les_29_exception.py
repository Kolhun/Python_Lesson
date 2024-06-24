class InvalidDataException(Exception):
    pass

class ProcessingException(Exception):
    pass

def generate_exceptions(argument):
    if argument == 1:
        raise InvalidDataException("Неверные данные!")
    elif argument == 2:
        raise ProcessingException("Ошибка обработки!")

try:
    generate_exceptions(1)
except InvalidDataException as e:
    print(f"Ошибка: {e}")

try:
    generate_exceptions(2)
except ProcessingException as e:
    print(f"Ошибка: {e}")
