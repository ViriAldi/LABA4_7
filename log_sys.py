import geocoder
from math import sin, cos, acos, ceil


class Location:
    def __init__(self, city, postoffice):
        self.city = city
        self.postoffice = postoffice

        data = geocoder.osm(city).osm
        self.coordinates = (data['y'], data['x'])

    def distance(self, location, radius=6400):
        alt1, lon1 = self.coordinates
        alt2, lon2 = location.coordinates

        delta_lon = abs(lon1 - lon2)
        if delta_lon > 180:
            delta_lon = 360 - delta_lon

        alt1, alt2, delta_lon = alt1/57, alt2/57, delta_lon/57

        dist = ((alt1 - alt2)**2 + delta_lon**2)**0.5

        ans = dist * radius

        return ans


class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        ans = f'This is {self.name}. Its price {self.price}'
        return ans


class Vehicle:
    def __init__(self, vehicleNo, type_veh, speed, max_time=10000, location=Location('Kyiv', 1)):
        self.vehicleNo = vehicleNo
        self.scheldue = {day: 0 for day in range(1, max_time + 1)}
        self.location = location
        self.type_veh = type_veh
        self.speed = speed

    def book_vehicle(self, time1, time2):
        for day in range(time1, time2 + 1):
            self.scheldue[day] = 1

    def cancel_booking(self, time1, time2):
        for day in range(time1, time2 + 1):
            self.scheldue[day] = 0

    def is_avaliable(self, time1, time2):
        flag = all([self.scheldue[day] == 0 for day in range(time1, time2 + 1)])

        return flag


class Order:
    def __init__(self, orderID, user_name, time_now,\
        location_start, location_end, items, vehicle):
        self.orderID = orderID
        self.user_name = user_name
        self.start = location_start
        self.end = location_end
        self.items = items
        self.vehicle = vehicle
        self.time_now = time_now

    def calculateAmount(self):
        total = [elem.price for elem in self.items]

        return sum(total)

    def __str__(self):
        id_item = f"This is an order {self.orderID}. "
        locat = f"It is sent to {self.end.city} to postoffice {self.end.postoffice}. "
        user_data = f"It is sent to {self.user_name}. "

        total = self.calculateAmount()

        total = f"The price: {total}. "
        way_shipping = f"It will be shipped by {self.vehicle.type_veh}. "
        endtime = f"Order is going to be shipped in {self.endtime()} days. "

        return id_item + locat + user_data + total + way_shipping + endtime

    def endtime(self):
        start = self.time_now
        car = self.vehicle
        speed = car.speed
        loc = car.location

        duration = ceil((loc.distance(self.start) + self.start.distance(self.end)) / speed)

        return start + duration

    def assignVehicle(self, vehicle):
        start = self.time_now
        endtime = self.endtime()

        self.vehicle.book_vehicle(start, endtime)


class LogisticSystem:
    def __init__(self, vehicles, orders=[]):
        self.vehicles = vehicles
        self.orders = orders
        self.IDs = 1

    def place_order(self, time_now, location1, location2, user_name, items, waiting_time=30000):
        flag = False

        for day in range(time_now, time_now + waiting_time):
            for car in self.vehicles:
                duration = ceil((car.location.distance(location1) + location1.distance(location2)) / car.speed)
                if car.is_avaliable(day, day + duration):
                    ans1 = day
                    ans = car
                    flag = True
                    break

            if flag:
                break

        if not flag:
            return 'No way'

        order = Order(self.IDs, user_name, ans1, location1, location2, items, ans)
        order.assignVehicle(ans)
        self.orders.append(order)
        self.IDs += 1

    def track_order(self, num):
        for order in self.orders:
            if order.orderID == num:
                return order.__str__()


if __name__ == "__main__":
    plane = Vehicle(1, 'plane', 1000)
    car = Vehicle(1, 'car', 400)
    train = Vehicle(1, 'train', 500)

    DHL = LogisticSystem([plane, car, train])
    items = [Item('ak-47 kush', 1000)]

    for order in ['Lviv', 'Kharkiv', 'Moscow', 'Krakow', 'New York']:
        DHL.place_order(1, Location('Kyiv', 1), Location(order, 1), 'Nazar', items)

    for order in range(1, DHL.IDs + 1):
        print(DHL.track_order(order))
