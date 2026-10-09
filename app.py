import streamlit as st

from scraper.repository import (
    get_all_authors,
    get_all_quotes,
    get_authors_count,
    get_quotes_count,
    init_db,
)
from scraper.service import (
    enrich_authors,
    scrape_all_pages_and_save,
    scrape_first_page_and_save,
)
from scraper.sheets_sync import export_all_to_google_sheets
from scraper.workflow import run_full_workflow

st.set_page_config(
    page_title="Quotes Scraper Lab",
    layout="wide",
)

st.title("Quotes Scraper Lab")
st.write("Учебное приложение для парсинга Quotes to Scrape")

init_db()

st.subheader("Full workflow")

st.write(
    "Запустить полный процесс: "
    "парсинг цитат → данные авторов → экспорт в Google Sheets."
)

if st.button(
    "Run full workflow",
    type="primary",
):
    try:
        with st.spinner("Выполняю полный workflow..."):
            result = run_full_workflow()

        st.success("Полный workflow успешно завершён.")

        st.write(
            f"Страниц обработано: {result['pages_processed']}"
        )

        st.write(
            f"Цитат найдено: {result['quotes_found']}"
        )

        st.write(
            f"Новых цитат добавлено: {result['quotes_inserted']}"
        )

        st.write(
            f"Авторов обогащено: {result['authors_enriched']}"
        )

        st.write(
            f"Цитат экспортировано: {result['quotes_exported']}"
        )

        st.write(
            f"Авторов экспортировано: {result['authors_exported']}"
        )

    except Exception as error:
        st.error(f"Ошибка workflow: {error}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Scrape first page"):
        try:
            result = scrape_first_page_and_save()

            st.success(
                f"Готово. "
                f"Обработано страниц: {result['pages_processed']}. "
                f"Найдено цитат: {result['quotes_found']}. "
                f"Добавлено новых: {result['quotes_inserted']}."
            )

        except Exception as error:
            st.error(f"Ошибка при парсинге: {error}")


with col2:
    if st.button("Scrape all pages"):
        try:
            with st.spinner("Парсинг всех страниц..."):
                result = scrape_all_pages_and_save()

            st.success(
                f"Готово. "
                f"Обработано страниц: {result['pages_processed']}. "
                f"Найдено цитат: {result['quotes_found']}. "
                f"Добавлено новых: {result['quotes_inserted']}."
            )

        except Exception as error:
            st.error(f"Ошибка при парсинге: {error}")


with col3:
    if st.button("Enrich authors"):
        try:
            with st.spinner("Загружаю данные авторов..."):
                result = enrich_authors()

            st.success(
                f"Готово. "
                f"Найдено авторов без деталей: {result['authors_found']}. "
                f"Обогащено авторов: {result['authors_enriched']}."
            )

        except Exception as error:
            st.error(f"Ошибка при обработке авторов: {error}")


with col4:
    total_quotes = get_quotes_count()
    total_authors = get_authors_count()

    st.metric(
        label="Quotes",
        value=total_quotes,
    )

    st.metric(
        label="Authors",
        value=total_authors,
    )
st.divider()

st.subheader("Google Sheets")

if st.button("Export to Google Sheets"):
    try:
        with st.spinner("Экспортирую данные в Google Sheets..."):
            result = export_all_to_google_sheets()

        st.success(
            f"Экспорт завершён. "
            f"Цитат экспортировано: {result['quotes_exported']}. "
            f"Авторов экспортировано: {result['authors_exported']}."
        )

    except Exception as error:
        st.error(f"Ошибка экспорта: {error}")

st.subheader("Saved quotes")

quotes = get_all_quotes()

if quotes:
    st.dataframe(
        quotes,
        use_container_width=True,
    )
else:
    st.info("В базе пока нет данных.")

st.subheader("Authors")

authors = get_all_authors()

if authors:
    st.dataframe(
        authors,
        use_container_width=True,
    )
else:
    st.info("В базе пока нет авторов.")
    