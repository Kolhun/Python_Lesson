class Vehicle:
    vehicle_type = "none"


class Car(Vehicle):
    price = 1000000

    def horse_powers(self):
        return 100


class Nissan(Car):
    price = 800000
    vehicle_type = "Nissan"

    def horse_powers(self):
        return 150


nissan = Nissan()
print(nissan.vehicle_type)  # Nissan
print(nissan.price)  # 800000