import unittest


class Runner:
    def __init__(self, name):
        self.name = name
        self.distance = 0

    def run(self):
        self.distance += 10

    def walk(self):
        self.distance += 5

    def __str__(self):
        return self.name


class RunnerTest(unittest.TestCase):
    def test_walk(self):
        _walk = Runner("Test runner")
        for i in range(10):
            _walk.walk()
        self.assertEqual(_walk.distance, 50)

    def test_run(self):
        _run = Runner("Test runner")
        for i in range(10):
            _run.run()
        self.assertEqual(_run.distance, 100)

    def test_challenge(self):
        runner1 = Runner("Test runner")
        runner2 = Runner("Test runner2")
        for i in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)


if __name__ == "__main__":
    unittest.main()
