class House:
    def __init__(self, name, number_of_floors):
        self.name = name
        self.number_of_floors = number_of_floors

    def go_to(self, new_floor):
        if new_floor > self.number_of_floors:
            print(f"Ошибка: {self.name} имеет всего {self.number_of_floors} этажей.")
        else:
            print(f"Вы переместились на {new_floor} этаж в здании {self.name}.")


my_house = House("Мой дом", 5)


my_house.go_to(3)