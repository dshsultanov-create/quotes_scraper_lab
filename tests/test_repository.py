from scraper import repository


def test_save_quotes_without_duplicates(tmp_path, monkeypatch):
    # Создаем путь к временной тестовой базе
    test_db = tmp_path / "test_quotes.db"

    # Временно подменяем настоящий DB_PATH
    # на путь к тестовой базе
    monkeypatch.setattr(
        repository,
        "DB_PATH",
        str(test_db),
    )

    # Создаем структуру тестовой базы
    repository.init_db()

    # Тестовые данные
    quotes = [
        {
            "quote_text": "Test database quote",
            "author_name": "Test Author",
            "author_about_url": "https://example.com/author/test",
            "tags": [
                "python",
                "sqlite",
            ],
            "page_number": 1,
        }
    ]

    # Первый раз цитата должна добавиться
    first_insert = repository.save_quotes(quotes)

    # Второй раз та же цитата не должна добавиться
    second_insert = repository.save_quotes(quotes)

    # Проверяем защиту от дублей
    assert first_insert == 1
    assert second_insert == 0

    # В базе должна остаться только одна цитата
    assert repository.get_quotes_count() == 1

    # И только один автор
    assert repository.get_authors_count() == 1

    # Читаем цитаты обратно из базы
    saved_quotes = repository.get_all_quotes()

    assert len(saved_quotes) == 1

    saved_quote = saved_quotes[0]

    # Проверяем данные цитаты
    assert saved_quote["quote_text"] == "Test database quote"

    # Проверяем, что JOIN с таблицей authors работает
    assert saved_quote["author_name"] == "Test Author"

    assert (
        saved_quote["author_about_url"]
        == "https://example.com/author/test"
    )

    # Проверяем остальные данные
    assert saved_quote["tags"] == "python, sqlite"
    assert saved_quote["page_number"] == 1


def test_save_author_details(tmp_path, monkeypatch):
    # Создаем отдельную временную базу для этого теста
    test_db = tmp_path / "test_authors.db"

    # Подменяем путь к настоящей базе
    monkeypatch.setattr(
        repository,
        "DB_PATH",
        str(test_db),
    )

    # Создаем таблицы
    repository.init_db()

    # Сохраняем цитату.
    # При этом автор автоматически появится в таблице authors.
    quotes = [
        {
            "quote_text": "Test author quote",
            "author_name": "Albert Einstein",
            "author_about_url": (
                "https://quotes.toscrape.com/author/Albert-Einstein"
            ),
            "tags": [
                "science",
            ],
            "page_number": 1,
        }
    ]

    repository.save_quotes(quotes)

    # Автор уже существует,
    # но подробные данные о нем еще не заполнены.
    authors_without_details = (
        repository.get_authors_without_details()
    )

    assert len(authors_without_details) == 1

    author_before_update = authors_without_details[0]

    assert author_before_update["author_name"] == "Albert Einstein"

    assert (
        author_before_update["author_about_url"]
        == "https://quotes.toscrape.com/author/Albert-Einstein"
    )

    # Данные, которые мы хотим добавить автору
    details = {
        "born_date": "March 14, 1879",
        "born_location": "in Ulm, Germany",
        "description": (
            "Albert Einstein was a theoretical physicist."
        ),
    }

    # Обновляем автора
    repository.save_author_details(
        "https://quotes.toscrape.com/author/Albert-Einstein",
        details,
    )

    # Читаем авторов обратно из базы
    authors = repository.get_all_authors()

    assert len(authors) == 1

    author = authors[0]

    # Проверяем основные данные
    assert author["author_name"] == "Albert Einstein"

    assert (
        author["author_about_url"]
        == "https://quotes.toscrape.com/author/Albert-Einstein"
    )

    # Проверяем новые поля
    assert author["born_date"] == "March 14, 1879"
    assert author["born_location"] == "in Ulm, Germany"

    assert (
        author["description"]
        == "Albert Einstein was a theoretical physicist."
    )

    # После заполнения born_date автор больше
    # не должен считаться необработанным.
    authors_without_details = (
        repository.get_authors_without_details()
    )

    assert len(authors_without_details) == 0