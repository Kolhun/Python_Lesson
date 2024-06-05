class Car:
    price = 1000000

    def horse_powers(self):
        return 100


class Nissan(Car):
    price = 800000

    def horse_powers(self):
        return 150


class Kia(Car):
    price = 600000

    def horse_powers(self):
        return 120

car = Car()
nissan = Nissan()
kia = Kia()

print(car.price)
print(car.horse_powers())

print(nissan.price)
print(nissan.horse_powers())

print(kia.price)
print(kia.horse_powers())  