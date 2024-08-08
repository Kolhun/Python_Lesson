import unittest

# Определяем декоратор для пропуска тестов в зависимости от атрибута is_frozen
def skip_if_frozen(method):
    def wrapper(self, *args, **kwargs):
        if self.is_frozen:
            print(f"Тесты в этом кейсе заморожены: {method.__name__}")
            return
        return method(self, *args, **kwargs)
    return wrapper

# Определяем первый набор тестов
class RunnerTest(unittest.TestCase):
    is_frozen = False

    @skip_if_frozen
    def test_run(self):
        self.assertTrue(True)

    @skip_if_frozen
    def test_walk(self):
        self.assertFalse(False)

class TournamentTest(unittest.TestCase):
    is_frozen = True

    @skip_if_frozen
    def test_compete(self):
        self.assertEqual(1 + 1, 2)

    @skip_if_frozen
    def test_win(self):
        self.assertGreater(5, 3)

# Создаем TestSuite и добавляем тесты
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(RunnerTest))
suite.addTest(unittest.makeSuite(TournamentTest))

# Создаем объект TextTestRunner с verbosity=2
runner = unittest.TextTestRunner(verbosity=2)

if __name__ == '__main__':
    runner.run(suite)
