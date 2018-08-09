"""
Objective:-
A sample program to calculate the charges for a movie rented by a customer for a
given duration. Movie can be categorized on category of Children, Regular,
Latest.
The output of the program should be a statement.
A customer can rent multiple movies at a time.
"""

# should be database with protected access.
movie_dict = {}


class Movies(object):
    _title = None
    _price = None
    
    @property
    def price_code(self):
        return movie_dict[self._title]
    
    @price_code.setter
    def price_code(self, price):
        self._price = price

    @property
    def movie(self):
        if self._title in movie_dict:
            return self._title
        return None

    @movie.setter
    def movie(self, title):
        self._title = title

    def set_movie_details(self):
        movie_dict[self._title] = self._price


class Rent(object):
    _days = None
    _rent = None

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, days):
        self._days = days

    @property
    def rent(self):
        return self._rent

    @rent.setter
    def rent(self, movie_object):
        self._rent = movie_object.price_code * self.days()

    # Add method to calculate charge


class Customer(object):
    _name = None
    _rented_movies = []

    @property
    def rented_movies(self):
        return self._rented_movies

    @rented_movies.setter
    def rented_movies(self, movie):
        self._rented_movies.append(movie)

    @property
    def customer_name(self):
        return self._name

    @customer_name.setter
    def customer_name(self, name):
        self._name = name

'''
Flawed Code'''