def test(*args):
    for arg in args:
        print(int(arg))


def factorial(n : int):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

test(3)
print(factorial(5))