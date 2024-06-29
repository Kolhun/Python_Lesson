numbers = [1, 2, 5, 7, 12, 11, 35, 4, 89, 10]

result = list(map(lambda x: x**2, filter(lambda x: x % 2 != 0, numbers)))

print(result)
