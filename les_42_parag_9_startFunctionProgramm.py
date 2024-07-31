def apply_all_func(int_list, *functions):
    results = {}


    for func in functions:
        result = func(int_list)
        results[func.__name__] = result

    return results


def sum_list(lst):
    return sum(lst)


def max_list(lst):
    return max(lst)


def min_list(lst):
    return min(lst)


int_list = [1, 2, 3, 4, 5]
result = apply_all_func(int_list, sum_list, max_list, min_list)

print(result)
