class Building:
    def __init__(self, number_of_floors, building_type):
        self.numberOfFloors = number_of_floors
        self.buildingType = building_type

    def __eq__(self, other):
        return self.numberOfFloors == other.numberOfFloors and self.buildingType == other.buildingType


building1 = Building(5, "Жилой дом")
building2 = Building(5, "Офисное здание")

print(building1 == building2)
