import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

@pytest.fixture
def add_book_1(collector):
    collector.add_new_book("Книга1")
    return collector

@pytest.fixture
def filled_collector(collector, add_book_1):
    add_book_1.set_book_genre("Книга1", "Мультфильмы")
    collector.add_new_book("Книга2")
    collector.set_book_genre("Книга2", "Ужасы")
    collector.add_new_book("Книга3")
    collector.set_book_genre("Книга3", "Мультфильмы")
    collector.add_new_book("Книга4")
    collector.set_book_genre("Книга4", "Комедии")
    return collector

@pytest.fixture
def only_adult_books(collector):
    collector.add_new_book("Книга4")
    collector.set_book_genre("Книга4", "Ужасы")
    collector.add_new_book("Книга5")
    collector.set_book_genre("Книга5", "Детективы")
    return collector