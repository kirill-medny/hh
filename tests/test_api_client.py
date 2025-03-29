import pytest
from src.api_client import HeadHunterAPI

def test_headhunter_api_get_vacancies():
    hh_api = HeadHunterAPI()
    data = hh_api.get_vacancies("Python developer", page=0)
    assert "items" in data
    assert isinstance(data["items"], list)

# tests/test_vacancy.py
from src.vacancy import Vacancy

def test_vacancy_comparison():
    v1 = Vacancy("Junior Python Dev", "url1", 50000, 80000, "Some description")
    v2 = Vacancy("Senior Python Dev", "url2", 100000, 150000, "Another description")
    assert v2 > v1
    assert v1 < v2
    assert v1 == Vacancy("Another Junior Python Dev", "url3", 50000, 70000, "Description") #Добавил еще один объект, но с той же самой зарплатой, чтоб проверить равенство

# tests/test_file_manager.py
import pytest
import os
from src.file_manager import JSONFileManager

@pytest.fixture
def json_file_manager():
    filename = "test_vacancies.json"
    yield JSONFileManager(filename)
    if os.path.exists(filename):
        os.remove(filename)

def test_json_file_manager_add_vacancy(json_file_manager):
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy"

def test_json_file_manager_get_vacancies(json_file_manager):
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1", "salary_from": 50000}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2", "salary_from": 100000}
    json_file_manager.add_vacancy(vacancy1)
    json_file_manager.add_vacancy(vacancy2)
    filtered_vacancies = json_file_manager.get_vacancies({"salary_from": 50000})
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0]["title"] == "Test Vacancy 1"

def test_json_file_manager_delete_vacancy(json_file_manager):
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    json_file_manager.add_vacancy(vacancy1)
    json_file_manager.add_vacancy(vacancy2)
    json_file_manager.delete_vacancy("test_url_1")
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy 2"

def test_json_file_manager_clear_file(json_file_manager):
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    json_file_manager.add_vacancy(vacancy1)
    json_file_manager.clear_file()
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 0