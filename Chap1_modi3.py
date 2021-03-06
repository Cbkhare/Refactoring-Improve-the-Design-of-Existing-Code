"""
Objective:-
A sample program to calculate the charges for a movie rented by a customer for a
given duration. Movie can be categorized on category of Children, Regular,
Latest.
The output of the program should be a statement.
A customer can rent multiple movies at a time.
"""

# should be database with protected access.
from random import randint
from abc import ABC, abstractmethod

movie_dict = {}
movie_obj_list = []
rent_obj_list = []


class Price(ABC):

    # price_code is in Movies, but basic rates as per the price_code os here
    _rates = {0: 1.5,  # Children
              1: 2,  # Regular
              2: 3  # New Release
              }

    @abstractmethod
    def price_code(self):
        pass

    @abstractmethod
    def calculate_charge(self, days):
        pass

    @abstractmethod
    def calculate_pointers(self):
        pass


class ChildrenPrice(Price):

    @property
    def price_code(self):
        return 0

    def calculate_charge(self, days):
        return self._rates.get(self.price_code) * days + 2

    @property
    def calculate_pointers(self):
        return 0


class RegularPrice(Price):

    @property
    def price_code(self):
        return 1

    def calculate_charge(self, days):
        return self._rates.get(self.price_code) * days + 3

    @property
    def calculate_pointers(self):
        return 1


class NewReleasePrice(Price):

    @property
    def price_code(self):
        return 2

    def calculate_charge(self, days):
        return self._rates.get(self.price_code) * days + 10

    @property
    def calculate_pointers(self):
        return 2


class Movies(object):
    _title = None
    _price_obj = None

    _code = {0: ChildrenPrice(),  # Children
              1: RegularPrice(),  # Regular
              2: NewReleasePrice()  # New Release
              }

    @property
    def price_code(self):
        return self._price_obj.price_code

    @price_code.setter
    def price_code(self, code):
        self._price_obj = self._code[code]

    @property
    def movie(self):
        return self._title

    @movie.setter
    def movie(self, title):
        self._title = title

    def calculate_charge(self, days):
        #return self._rates.get(self.price_code) * days
        return self._price_obj.calculate_charge(days)

    def calculate_points(self):
        return self._price_obj.calculate_pointers

    def set_movie_details(self):
        movie = self.movie
        if not movie:
            return False
        movie_dict[movie] = self.price_code


class Rent(object):
    _days = None
    _movie_rented_object = None

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, days):
        self._days = days

    @property
    def movie_rented(self):
        return self._movie_rented_object

    @movie_rented.setter
    def movie_rented(self, movie_object):
        self._movie_rented_object = movie_object

    def rent(self):
        return self._movie_rented_object.calculate_charge(self.days)

    def renting_pointer(self):
        return self._movie_rented_object.calculate_points()


class Customer(object):
    _name = None
    _rented_movies = []

    @property
    def rented_movies(self):
        return self._rented_movies

    @rented_movies.setter
    def rented_movies(self, rent_object):
        self._rented_movies.append(rent_object)

    @property
    def customer_name(self):
        return self._name

    @customer_name.setter
    def customer_name(self, name):
        self._name = name

    def get_total_rent(self):
        total_amount = 0
        for rented_movies in self._rented_movies:
            total_amount += rented_movies.rent()
        return total_amount

    def get_renting_points(self):
        renting_points = 0
        for rented_movies in self._rented_movies:
            renting_points += rented_movies.renting_pointer()
        return renting_points

    def statement(self):
        total_amount = self.get_total_rent()
        renting_points = self.get_renting_points()
        return total_amount, renting_points


if __name__ == "__main__":
    # add movies
    for i in range(10):
        M = Movies()
        M.movie = 'bazinga_' + str(i)
        M.price_code = randint(1, 10) % 2 + 1
        # print (M.movie, M.price_code)
        # M.set_movie_details()
        movie_obj_list.append(M)

    # add Rent
    for i in range(10):
        R = Rent()
        R.days = randint(1, 100)
        R.movie_rented = movie_obj_list[
            i]  # associated rent and movie object with index
        # print(R.rent)
        rent_obj_list.append(R)

    # add customer, Half rented movies for each of the customer
    C1 = Customer()
    C1.customer_name = "Customer_1"
    for i in range(0, 10, 2):
        C1.rented_movies = rent_obj_list[i]
    print("Statement for {}:".format(C1.customer_name))
    print("Total cost and renting points:", C1.statement())

    C2 = Customer()
    C2.customer_name = "Customer_2"
    for i in range(1, 10, 2):
        C2.rented_movies = rent_obj_list[i]
    print("Statement for {}:".format(C2.customer_name))
    print("Total cost and renting points:", C2.statement())
