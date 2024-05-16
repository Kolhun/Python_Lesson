for i in range(3, 21):
    pairs = []
    for j in range(1, i):
        if i % (j + (i - j)) == 0:
            pairs.append((j, i - j))
    print(f"Для числа {i} возможные попарные значения: {pairs}")