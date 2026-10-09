# Quotes Scraper Lab

Учебный Python-проект для изучения полного цикла разработки небольшого веб-приложения.

## Возможности

- Парсинг цитат с Quotes to Scrape
- Работа с пагинацией
- Парсинг страниц авторов
- Хранение данных в SQLite
- Защита от дубликатов
- Интерфейс на Streamlit
- Экспорт данных в Google Sheets
- Автоматический полный workflow
- Тесты с pytest
- Проверка кода с Ruff

## Структура проекта

```text
quotes_scraper_lab/
├── app.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── scraper/
│   ├── __init__.py
│   ├── config.py
│   ├── fetch.py
│   ├── parse.py
│   ├── repository.py
│   ├── service.py
│   ├── sheets_sync.py
│   └── workflow.py
├── tests/
└── data/