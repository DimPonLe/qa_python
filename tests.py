import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    #def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        #collector = BooksCollector()

        # добавляем две книги
        #collector.add_new_book('Гордость и предубеждение и зомби')
       # collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        #assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    class TestBooksCollector:

        @pytest.mark.parametrize(
            "name, expected",
            [
                ("Книга1", True),
                ("", False),
                ("Книга1Книга1Книга1Книга1Книга1Книга1Книга", False),
            ],
        )
        def test_add_and_check_book_presence(self, collector, name, expected):
            collector.add_new_book(name)
            assert (name in collector.get_books_genre()) == expected, f"{name} {'не' if expected else ''} должна быть добавлена."

        def test_assign_and_retrieve_genre(self, collector):
            collector.add_new_book("Книга1")
            collector.set_book_genre("Книга1", "Фантастика")
            assert collector.get_book_genre("Книга1") == "Фантастика", "Жанр не был назначен корректно."

        @pytest.mark.parametrize("book_name, genre", [
            ("Книга1", "Фэнтези"),
            ("Книга2", "Научная фантастика"),
            ("Книга3", "Детектив"),
        ])
        def test_assign_genres_to_multiple_books(self, collector, book_name, genre):
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
            assert collector.get_book_genre(book_name) == genre, f"Полученный жанр ({collector.get_book_genre(book_name)}) не соответствует заданному ({genre})."

        @pytest.mark.parametrize("book_name, initial_genre, invalid_genre", [
            ("Книга1", "Фэнтези", ""),
            ("Книга2", "Научная фантастика", "!#$%^&*()"),
            ("Книга3", "Детектив", "Некорректный жанр"),
        ])
        def test_invalid_genre_change(self, collector, book_name, initial_genre, invalid_genre):
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, initial_genre)
            collector.set_book_genre(book_name, invalid_genre)
            assert collector.get_book_genre(book_name) == initial_genre, f"Некорректный жанр ('{invalid_genre}') изменил текущий жанр ('{initial_genre}')"

        def test_internal_genre_storage(self, collector):
            collector.add_new_book("Книга1")
            collector.set_book_genre("Книга1", "Фэнтези")
            internal_genres = getattr(collector, "_genres", {})
            assert len(internal_genres) > 0, "Внутренний словарь жанров должен содержать записи"
            assert internal_genres["Книга1"] == "Фэнтези", "Во внутренней структуре жанра указана неверная информация"

        def test_retrieve_books_by_genre(self, collector):
            collector.add_new_book("Книга1")
            collector.set_book_genre("Книга1", "Фантастика")
            collector.add_new_book("Книга2")
            collector.set_book_genre("Книга2", "Фантастика")
            result = collector.get_books_with_specific_genre("Фантастика")
            expected_result = ["Книга1", "Книга2"]
            assert sorted(result) == sorted(expected_result), f"Результат {result}, ожидалось {expected_result}"

        def test_empty_list_for_unknown_genre(self, collector):
            result = collector.get_books_with_specific_genre("Комедии")
            assert result == [], "Список книг должен быть пустым, если нет книг выбранного жанра."

        def test_filter_children_books(self, collector):
            collector.add_new_book("Книга1")
            collector.set_book_genre("Книга1", "Фантастика")
            collector.add_new_book("Книга2")
            collector.set_book_genre("Книга2", "Ужасы")
            children_books = collector.get_books_for_children()
            expected_result = ["Книга1"]
            assert sorted(children_books) == sorted(expected_result), f"Ошибка в списке детских книг: ожидалось {expected_result}, получено {children_books}"

        def test_add_book_to_faves(self, collector):
            collector.add_new_book("Книга1")
            collector.add_book_in_favorites("Книга1")
            favorites = collector.get_list_of_favorites_books()
            assert "Книга1" in favorites, "Книга должна быть добавлена в избранное."

        def test_remove_book_from_faves(self, collector):
            collector.add_new_book("Книга1")
            collector.add_book_in_favorites("Книга1")
            collector.delete_book_from_favorites("Книга1")
            favorites = collector.get_list_of_favorites_books()
            assert "Книга1" not in favorites, "Удалённая книга не должна присутствовать в избранном."