import pytest
from unittest.mock import patch, MagicMock
from src.utils import (
    get_vacancies_from_hh,
    create_vacancy_from_hh_item,
    display_vacancies,
    save_vacancies_to_file,
    load_vacancies_from_file,
)
from src.vacancy import Vacancy
from src.file_manager import JSONFileManager

def test_get_vacancies_from_hh_success(mock_hh_api, sample_hh_item, sample_vacancy):
    """Тест успешного получения вакансий из hh.ru."""
    mock_hh_api.get_vacancies.return_value = {"items": [sample_hh_item]}
    vacancies = get_vacancies_from_hh("Python", "113", num_pages=1) # Добавлен area_id
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"

def test_get_vacancies_from_hh_no_data(mock_hh_api):
    """Тест получения вакансий из hh.ru, когда нет данных."""
    mock_hh_api.get_vacancies.return_value = None
    vacancies = get_vacancies_from_hh("Python", "113", num_pages=1)  # Добавлен area_id
    assert len(vacancies) == 0

def test_get_vacancies_from_hh_empty_items(mock_hh_api):
    """Тест получения вакансий из hh.ru, когда items пустой."""
    mock_hh_api.get_vacancies.return_value = {"items": []}
    vacancies = get_vacancies_from_hh("Python", "113", num_pages=1) # Добавлен area_id
    assert len(vacancies) == 0

def test_get_vacancies_from_hh_multiple_pages(mock_hh_api, sample_hh_item, sample_vacancy):
    """Тест получения вакансий из hh.ru с нескольких страниц."""
    mock_hh_api.get_vacancies.side_effect = [
        {"items": [sample_hh_item]},
        {"items": [sample_hh_item]},
    ]
    vacancies = get_vacancies_from_hh("Python", "113", num_pages=2)  # Добавлен area_id
    assert len(vacancies) == 2
    assert all(isinstance(v, Vacancy) for v in vacancies)

def test_create_vacancy_from_hh_item_success(sample_hh_item, sample_vacancy):
    """Тест успешного создания объекта Vacancy из элемента hh.ru."""
    vacancy = create_vacancy_from_hh_item(sample_hh_item)
    assert isinstance(vacancy, Vacancy)
    assert vacancy.title == "Python Developer"

def test_create_vacancy_from_hh_item_missing_salary(sample_hh_item):
    """Тест создания объекта Vacancy, когда отсутствует информация о зарплате."""
    del sample_hh_item["salary"]
    vacancy = create_vacancy_from_hh_item(sample_hh_item)
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0

def test_create_vacancy_from_hh_item_missing_snippet(sample_hh_item):
    """Тест создания объекта Vacancy, когда отсутствует snippet."""
    del sample_hh_item["snippet"]
    vacancy = create_vacancy_from_hh_item(sample_hh_item)
    assert vacancy.description == ""

def test_create_vacancy_from_hh_item_key_error(sample_hh_item):
    """Тест создания объекта Vacancy, когда отсутствует ключевое поле."""
    del sample_hh_item["name"]
    vacancy = create_vacancy_from_hh_item(sample_hh_item)
    assert vacancy is None

def test_display_vacancies_empty_list(capsys):
    """Тест отображения вакансий, когда список пуст."""
    display_vacancies([])
    captured = capsys.readouterr()
    assert "Нет вакансий для отображения." in captured.out

def test_display_vacancies_success(capsys, sample_vacancy):
    """Тест успешного отображения вакансий."""
    display_vacancies([sample_vacancy])
    captured = capsys.readouterr()
    assert "Название: Python Developer" in captured.out
    assert "Ссылка: https://example.com/vacancy/123" in captured.out
    assert "Зарплата: 100000 - 150000" in captured.out
    assert "Описание: Python, Django Develop web applications" in captured.out

@patch("src.utils.JSONFileManager.add_vacancy")
def test_save_vacancies_to_file_success(mock_add_vacancy, sample_vacancy, capsys, tmpdir):
    """Тест успешного сохранения вакансий в файл."""
    filename = tmpdir.join("test_vacancies.json")
    save_vacancies_to_file([sample_vacancy], filename)
    mock_add_vacancy.assert_called_once()
    captured = capsys.readouterr()
    assert f"Сохранено 1 вакансий в {filename}" in captured.out

@patch("src.utils.JSONFileManager.get_vacancies")
def test_load_vacancies_from_file_success(mock_get_vacancies, sample_vacancy):
    """Тест успешной загрузки вакансий из файла."""
    mock_get_vacancies.return_value = [dict(sample_vacancy)]
    vacancies = load_vacancies_from_file("test_vacancies.json")
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"

def test_load_vacancies_from_file_empty_file(tmpdir):
    """Тест загрузки вакансий из пустого файла."""
    filename = tmpdir.join("test_vacancies.json")
    filename.write("[]")
    vacancies = load_vacancies_from_file(filename)
    assert len(vacancies) == 0

# --- Параметризованные тесты ---

@pytest.mark.parametrize(
    "num_pages, expected_vacancy_count",
    [
        (1, 1),
        (2, 2),
        (0, 0),
    ],
)
def test_get_vacancies_from_hh_parameterized(mock_hh_api, sample_hh_item, num_pages, expected_vacancy_count):
    """Параметризованный тест для get_vacancies_from_hh."""
    mock_hh_api.get_vacancies.return_value = {"items": [sample_hh_item]}
    vacancies = get_vacancies_from_hh("Python", "113", num_pages=num_pages) # Добавлен area_id
    assert len(vacancies) == expected_vacancy_count