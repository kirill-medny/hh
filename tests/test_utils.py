import pytest
import os
from src.utils import get_vacancies_from_hh, create_vacancy_from_hh_item, display_vacancies, save_vacancies_to_file, load_vacancies_from_file
from src.vacancy import Vacancy

@pytest.fixture
def vacancy_list():
    return [
        Vacancy("Junior Python Dev", "url1", 50000, 80000, "Some description"),
        Vacancy("Senior Python Dev", "url2", 100000, 150000, "Another description"),
        Vacancy("Middle Python Dev", "url3", 70000, 100000, "Key description")
    ]

def test_create_vacancy_from_hh_item():
    item = {
        "name": "Test Vacancy",
        "alternate_url": "test_url",
        "salary": {"from": 50000, "to": 100000},
        "snippet": {"requirement": "Requirement", "responsibility": "Responsibility"}
    }
    vacancy = create_vacancy_from_hh_item(item)
    assert vacancy.title == "Test Vacancy"
    assert vacancy.url == "test_url"
    assert vacancy.salary_from == 50000
    assert vacancy.salary_to == 100000
    assert vacancy.description == "Requirement"

def test_save_vacancies_to_file(vacancy_list):
    filename = "test_vacancies.json"
    save_vacancies_to_file(vacancy_list, filename)
    assert os.path.exists(filename)
    os.remove(filename)  # Clean up the file after the test

def test_load_vacancies_from_file(vacancy_list):
    filename = "test_vacancies.json"
    save_vacancies_to_file(vacancy_list, filename)
    loaded_vacancies = load_vacancies_from_file(filename)
    assert len(loaded_vacancies) == len(vacancy_list)
    assert all(isinstance(v, Vacancy) for v in loaded_vacancies)
    os.remove(filename)  # Clean up the file after the test

def test_get_vacancies_from_hh():
    vacancies = get_vacancies_from_hh("Python developer", 1)
    assert isinstance(vacancies, list)
    if vacancies:
        assert isinstance(vacancies[0], Vacancy)