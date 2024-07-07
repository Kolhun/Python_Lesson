def sum_three(a, b, c):
    return a + b + c

def is_prime(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if is_prime_number(result):
            print("Простое")
        else:
            print("Составное")
        return result
    return wrapper

def is_prime_number(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

@is_prime
def sum_three_with_prime_check(a, b, c):
    return sum_three(a, b, c)

result = sum_three_with_prime_check(2, 3, 6)
print(result)
