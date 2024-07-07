class EvenNumbers:
    def __init__(self, start=0, end=1):
        self.start = start if start % 2 == 0 else start + 1
        self.end = end if end % 2 == 0 else end - 1
        self.current = self.start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        else:
            result = self.current
            self.current += 2
            return result

# Пример использования
en = EvenNumbers(10, 25)
for i in en:
    print(i)
