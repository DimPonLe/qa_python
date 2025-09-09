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
            ("Книга1", True),
            ("", False),
            ("Книга1Книга1Книга1Книга1Книга1Книга1Книга", False),
        ],
    )
    def test_add_new_book(name, expected):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected, f"{name} {'не' if expected else ''} должна быть добавлена."

    @pytest.mark.parametrize(
        "book_name, genre, exception_type",
        [
            ("Книга1", "Фантастика", None),
            ("Невалидная Книга", "Фантастика", KeyError),
            ("Книга1", "Неверный Жанр", ValueError),
        ]
    )
    def test_set_book_genre(book_name, genre, exception_type):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        if exception_type is None:
            collector.set_book_genre(book_name, genre)
            assert collector.get_book_genre(book_name) == genre, f"Жанр '{genre}' должен быть установлен."
        else:
            try:
                collector.set_book_genre(book_name, genre)
            except exception_type:
                pass
            else:
                raise AssertionError(f"Ожидалось исключение {exception_type.__name__}")

    def test_get_book_genre():
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        assert collector.get_book_genre("Книга1") == "Фантастика", "Вернуть правильный жанр."
        
        assert collector.get_book_genre("НетТакойКниги") is None, "Отсутствие жанра должно вернуть None."

    def test_get_books_with_specific_genre():
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Фантастика")
        result = collector.get_books_with_specific_genre("Фантастика")
        expected_result = ["Книга1", "Книга2"]
        assert sorted(result) == sorted(expected_result), f"Результат {result}, ожидалось {expected_result}"

        empty_result = collector.get_books_with_specific_genre("Комедии")
        assert empty_result == [], "Список книг должен быть пустым, если нет книг выбранного жанра."

    def test_get_books_for_children():
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Ужасы")
        children_books = collector.get_books_for_children()
        expected_result = ["Книга1"]
        assert sorted(children_books) == sorted(expected_result), f"Ошибка в списке детских книг: ожидалось {expected_result}, получено {children_books}"

    def test_favorite_books():
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_book_in_favorites("Книга1")
        favorites = collector.get_list_of_favorites_books()
        assert "Книга1" in favorites, "Книга должна быть добавлена в избранное."
        
        collector.delete_book_from_favorites("Книга1")
        favorites_after_delete = collector.get_list_of_favorites_books()
        assert "Книга1" not in favorites_after_delete, "Удалённая книга не должна присутствовать в избранном."