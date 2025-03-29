import pytest
import os
import json
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

def test_json_file_manager_file_not_found(json_file_manager):
    # Test case when the file does not exist
    # Should return an empty list
    assert json_file_manager.get_vacancies() == []

def test_json_file_manager_empty_file(json_file_manager):
    # Test case when the file is empty but exists
    with open(json_file_manager.filename, 'w') as f:
        f.write('')  # Create an empty file
    assert json_file_manager.get_vacancies() == []

def test_json_file_manager_corrupted_file(json_file_manager):
    # Test case when the file contains corrupted JSON
    with open(json_file_manager.filename, 'w') as f:
        f.write('This is not a valid JSON')
    # Expect it to handle JSONDecodeError and return an empty list
    assert json_file_manager.get_vacancies() == []