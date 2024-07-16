import threading
import time

class Knight(threading.Thread):
    def __init__(self, name : str, power : int):
        super().__init__()
        self.name = name
        self.power = power

    def run(self):
        print(f"{self.name}, на нас напали!")
        enemies = 100
        days = 0
        while enemies > 0:
            days += 1
            print(f"{self.name} сражается {days} дней(дня)..., осталось {enemies} противников.")
            enemies -= self.power
            time.sleep(1)
        print(f"{self.name} одержал победу спустя {days} дней(дня)!")


knight1 = Knight('Sir Lancelot', 10)
knight2 = Knight("Sir Galahad", 20)

knight1.start()
knight2.start()

knight1.join()
knight2.join()

print("Битва окончена")
