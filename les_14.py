def func_start(**list_first):
    for key, value in list_first.items():
        print(key, value)


list_ = {"a": 1, "b": 2}
func_start(**list_)
