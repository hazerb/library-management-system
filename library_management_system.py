from utils import *
from collections import deque
from enum import Enum
from collections import defaultdict
from abc import ABC, abstractmethod

class Book:
    def __init__(self, title, author, isbn, edition):
        self.__isbn = isbn
        self.__title = title
        self.__author = author
        self.__edition = edition

    def __eq__(self, other):
        return self.__isbn == other.get_isbn()
    def __hash__(self, other):
        return hash(isbn)

    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author

    def get_isbn(self):
        return self.__isbn
    
    def get_edition(self):
        return self.__edition



class BookItem(Book):
    def __init__(self, title, author, isbn, edition, price, publication_year, placed_at=None):
        super().__init__(title, author, isbn, edition)
        self.__price = price
        self.__publication_year = publication_year
        self.__placed_at = placed_at

    def set_place(self, placed_at):
        self.__placed_at = placed_at

    def get_place(self):
        return self.__placed_at

    def get_price(self):
        return self.__price
    
    def get_publication_year(self):
        return self.__publication_year


class Rack:
    def __init__(self):
        self.__empty_book_places = deque([0 for i in range(Constants.RACK_SIZE)])
        self.__book_places = [0 for i in range(Constants.RACK_SIZE)]
    
    def put_book_item(self, book_item):
        empty_place = self.__empty_book_places.popleft()
        self.__book_places[empty_place] = book_item
        book_item.set_place(empty_place)

    def remove_book_item(self, book_item_place):
        book_item = self.__book_places[book_item_place]
        self.__book_places[book_item_place] = 0
        self.__empty_book_places.append(book_item_place)
        return book_item

    def is_full(self):
        if len(self.__empty_book_places) == 0:
            return True
        return False


class Catalog:
    def __init__(self):
        self.__book_list = set()
        self.__book_rack_places = defaultdict(set)
    
    def view_books(self):
        return self.__book_list

    def search_book(self, title):
        if title in self._ _book_rack_places:
            return self.__book_rack_places[title]

    def delete_book_item_place(self, book_item_place, book_item):
        self.__book_rack_places[book_item.get_title()].remove(book_item.get_place())

    def add_book_item_place(self, book_item):
        self.__book_rack_places[book_item.get_title()].add(book_item.get_place())
    
    def add_book(self, book):
        if book not in self.__book_list:
            self.__book_list.add(book)

class Person(ABC):
    @abstractmethod
    def __init__(self, name, surname):
        self.__name = name
        self.__surname = surname

class Librarian(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def add_book(self, library, book):
        library.add_book_to_catalog(book)

    def put_book_item_to_rack(self, library, book_item):
        rack = library.give_rack()
        if not rack.is_full():
            rack.put_book_item(book_item)
            library.add_book_item_place_to_catalog(book_item)


class Customer(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        
    def view_books(self, library):
        books = self.catalog.view_books()
        for book in books:
            print("title:" + book.get_title(), "|" ,"author:" + book.get_author())

    def get_catalog(self, library):
        self.catalog = library.give_catalog()

    def check_price(self, book_item):
        print(book_item.get_price())

    def take_book_item_from_rack(self, book_item_place):
        rack = library.give_rack()
        return rack.remove_book_item(book_item_place)

    def search_book(self, title, library):
        print(self.catalog.search_book(title))

    def lend_book(self, book_item, library):
        library.lend_book_item(self, book_item)

    def return_book(self, book_item, library):
        library.return_book_item(self, book_item)


class Library:
    def __init__(self):
        self.__catalog = Catalog()
        self.__rack = Rack()
        self.__book_lending_list = {}

    def give_catalog(self):
        return self.__catalog

    def give_rack(self):
        return self.__rack
    
    def lend_book_item(self, customer, book_item):
        self.__catalog.delete_book_item_place(book_item.get_place(), book_item)
        self.__book_lending_list[(customer, book_item)] = BookLending(customer, book_item)
    
    def return_book_item(self, customer, book_item):
        self.__book_lending_list[(customer, book_item)].change_status()

    def add_book_to_catalog(self, book):
        if not self.__rack.is_full():
            self.__catalog.add_book(book)

    def add_book_item_place_to_catalog(self, book_item):
        self.__catalog.add_book_item_place(book_item)

    def show_book_lending_list(self):
        return self.__book_lending_list

    


class LendingStatus(Enum):
    LENDED, CLOSED = 1, 2

class Constants:
    RACK_SIZE = 100

class BookLending:
    def __init__(self, customer, book_item):
        self.customer = customer
        self.book_item = book_item
        self.status = LendingStatus.LENDED

    def change_status(self):
        self.status = LendingStatus.CLOSED



library = Library()
librarian = Librarian("metin", "tekin")
customer = Customer("hazer", "babur")

moby_dick = Book("moby dick", "herman melville", "0553213113", 10)
moby_dick_item = BookItem("moby dick", "herman melville", "0553213113", 10 ,30, 2003)

librarian.add_book(library, moby_dick)
librarian.put_book_item_to_rack(library, moby_dick_item)
customer.get_catalog(library)
customer.view_books(library)
customer.search_book("moby dick", library)
book_item = customer.take_book_item_from_rack(0)
customer.lend_book(book_item, library)
lendings = library.show_book_lending_list()
print(lendings[customer, book_item].status)
customer.return_book(book_item, library)
customer.check_price(book_item)
print(lendings[customer, book_item].status)






            


    





    

        
        
