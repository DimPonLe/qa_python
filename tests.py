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

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("", False),
            (" ", False),
            ("К", True),
            ("Книга1", True),
            ("Книга1Книга1Книга1Книга1Книга1Книга1Книга", False),
            ("Книга1Книга1Книга1Книга1Книга1Книга1Книга1", False)
            (None, False),
            (12345, False),
        ]
    )
    def test_add_and_check_book_presence(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected, f"{name} {'не' if expected else ''} должна быть добавлена."

    def test_add_new_book_two_similar_book_not_change_dictionary(self, add_book_1):
        add_book_1.add_new_book("Книга1")
        add_book_1.add_new_book("Книга1")
        assert len(add_book_1.get_books_genre()) == 1, "В словаре одинаковые книги!"

    def test_add_new_book_ten_different_book_change_dictionary(self, collector):
        stack_books = [
                "Книга1",
                "Книга2",
                "Книга3",
                "Книга4",
                "Книга5",
                "Книга6",
                "Книга7",
                "Книга8",
                "Книга9",
                "Книга10",
        ]
        for books in stack_books:
            collector.add_new_book(books)

        assert len(collector.get_books_genre()) == 10, f"В словаре оказалось {len(collector.get_books_genre())} книг вместо 10"

    def test_set_book_genre_valid_genre_set_genre(self, add_book_1):
        add_book_1.set_book_genre("Книга1", "Ужасы")
        assert add_book_1.get_book_genre("Книга1") == "Ужасы", "Жанр не установлен корректно"

    def test_set_book_genre_invalid_genre_not_set_genre(self, add_book_1):
        add_book_1.set_book_genre("Книга1", "Повесть") 
        assert add_book_1.get_book_genre("Книга1") != "Повесть", "Неверный жанр сохранился в коллекции"

    def test_set_book_genre_add_book_with_genre_not_change_dictionary(self, collector):
        collector.set_book_genre("Книга1", "Фантастика") 
        assert collector.get_book_genre("Книга1") not in collector.get_books_genre(), "Создалась книга при установке жанра"

    def test_set_book_genre_not_book_in_dictionary_not_set_genre_nonexistent_in_dictionary_book(self, collector):
        collector.add_new_book("Книга1")
        assert collector.get_book_genre("Книга2") is None

    def test_get_book_genre_empty_title_not_set_genre_empty_book(self, collector):
        collector.add_new_book("")
        assert collector.get_book_genre("") is None

    def test_get_book_genre_none_value_not_change_dictionary(self, collector):
        collector.add_new_book(None)
        assert collector.get_book_genre(None) is None

    def test_set_book_genre_genre_cartoons_replace_genre(self, add_book_1):
        add_book_1.set_book_genre("Книга1", "Детективы")
        add_book_1.set_book_genre("Книга1", "Мультфильмы")
        assert add_book_1.get_book_genre("Книга1") == "Мультфильмы"

    def test_get_books_with_specific_genre_existing_genre_show_filled_book(filled_collector):
        result = filled_collector.get_books_with_specific_genre("Мультфильмы")
        assert sorted(result) == ["Книга1", "Книга3"], "Получены неверные книги жанра мультфильмы"

    @pytest.mark.parametrize(
        "genre, expected_result",
        [
            ("Комедия", []),
            ("Повести", []),
            ("", []),
            (None, []),
            (123, [])
        ]
    ) 
    def test_get_books_with_specific_genre_other_empty_invalid_genres(self, genre, expected_result, filled_collector):
        assert filled_collector.get_books_with_specific_genre(genre) == expected_result, f"Возврат неверного списка книг для жанра '{genre}'"

    def test_get_books_genre_empty_collection(self, collector):
        assert collector.get_books_genre() == {}, "Возвращён неверный словарь для пустой коллекции"

    def test_get_books_genre_filled_collection(collector, filled_collector):
        expected_dict = {
            "Книга1": "Мультфильмы",
            "Книга2": "Ужасы"
        }
        result = filled_collector.get_books_genre()
        assert result == expected_dict, "Возвращённый словарь отличается от ожидаемого"

    def test_get_books_for_children_child_genres(filled_collector):
        child_books = filled_collector.get_books_for_children()
        assert sorted(child_books) == ["Книга1", "Книга3"], "Возвращён неверный список детских книг"

    def test_get_books_for_children_only_adult_books_empty_list(only_adult_books):
        child_books = only_adult_books.get_books_for_children()
        assert child_books == [], "Возвращён неверный список детских книг"

    def test_get_books_for_children_empty_collection_empty_list(collector):
        child_books = collector.get_books_for_children()
        assert child_books == [], "Возвращён неверный список детских книг"
        

    def test_add_book_in_favorites_add_book_in_list(filled_collector):
        filled_collector.add_book_in_favorites("Книга1")
        favorite_books = filled_collector.get_list_of_favorites_books()
        assert "Книга1" in favorite_books, "Книга не добавилась в избранное"

    def test_add_same_book_twice_in_favorites(filled_collector):
        filled_collector.add_book_in_favorites("Книга1")
        filled_collector.add_book_in_favorites("Книга1")
        favorite_books = filled_collector.get_list_of_favorites_books()
        assert favorite_books.count("Книга1") == 1, "Одинаковая книга добавилась в избранное дважды"

    def test_delete_book_from_favorites_delete_book_in_list(filled_collector):
        filled_collector.add_book_in_favorites("Книга1")
        filled_collector.delete_book_from_favorites("Книга1")
        favorite_books = filled_collector.get_list_of_favorites_books()
        assert "Книга1" not in favorite_books, "Книга не удалилась из избранного"

    def test_test_delete_book_from_favorites(filled_collector):
        filled_collector.add_book_in_favorites("Книга1")
        filled_collector.delete_book_from_favorites("Книга1")
        filled_collector.delete_book_from_favorites("Книга1")
        assert "Книга1" not in filled_collector.get_list_of_favorites_books(), "Книга присутствовала в избранном после двойного удаления"

    def test_get_list_of_favorites_books_empty_list(collector):
        favorite_books = collector.get_list_of_favorites_books()
        assert favorite_books == [], "Возвращён неверный список избранных книг"

    def test_get_list_of_favorites_books_multiple_books(filled_collector):
        filled_collector.add_book_in_favorites("Книга1")
        filled_collector.add_book_in_favorites("Книга2")
        favorite_books = filled_collector.get_list_of_favorites_books()
        assert sorted(favorite_books) == ["Книга1", "Книга2"], "Возвращён неверный список избранных книг"
