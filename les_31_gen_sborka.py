def create_operation(operation):
    if operation == "add":
        def add(x, y):
            return x + y
        return add
    elif operation == "subtract":
        def subtract(x, y):
            return x - y
        return subtract
    elif operation == "multiply":
        def multiply(x, y):
            return x * y
        return multiply
    elif operation == "divide":
        def divide(x, y):
            if y != 0:
                return x / y
            else:
                print("Error: Division by zero")
        return divide
    else:
        return None

add_func = create_operation("add")
result = add_func(2, 4)  # Результат: 6

divide_func = create_operation("divide")
result = divide_func(8, 4)  # Результат: 2.0

divide_by_zero_func = create_operation("divide")
result = divide_by_zero_func(6, 0)  # Результат: Error: Division by zero

square = lambda x: x ** 2


result = square(4)

class Rect:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        return self.a * self.b

rectangle = Rect(2, 4)
print("Стороны:", rectangle.a, ",", rectangle.b)
print("Площадь:", rectangle())  # Результат: 8

