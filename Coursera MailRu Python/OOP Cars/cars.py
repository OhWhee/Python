import csv
import os

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying
    
    def get_photo_file_ext(self):
        self.file_extension = os.path.splitext(self.photo_file_name)[1]
        return self.file_extension


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl
        try:
            self.body_width = float(self.body_whl.split("x")[1])
            self.body_height = float(self.body_whl.split("x")[2])
            self.body_length = float(self.body_whl.split("x")[0])
        except IndexError:
            self.body_width = 0
            self.body_height = 0
            self.body_length = 0

    def get_body_volume(self):
        return float(self.body_width * self.body_length * self.body_height)
        

        
class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            try:
                if row[0] == "car":
                    car_list.append(Car(brand=row[1], 
                                        photo_file_name=row[3],
                                        carrying=row[5], 
                                        passenger_seats_count=int(row[2])))
                elif row[0] == "truck":
                    car_list.append(Truck(brand=row[1], 
                                        photo_file_name=row[3],
                                        carrying=row[5], 
                                        body_whl=row[4]))
                elif row[0] == "spec_machine":
                    car_list.append(SpecMachine(brand=row[1], 
                                        photo_file_name=row[3],
                                        carrying=row[5], 
                                        extra=(row[6])))
            except IndexError:
                pass
    return car_list

car_list = get_car_list("D:\coursera_week3_cars.csv")
test_car = car_list[1]