import pytest
import os
import json
import csv
from src.file_manager import JSONFileManager, CSVFileManager

# --- Тесты для JSONFileManager ---

def test_json_file_manager_add_vacancy(json_file_manager):
    """Тест добавления вакансии в JSON-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy"

def test_json_file_manager_add_duplicate_vacancy(json_file_manager):
    """Тест добавления дублирующейся вакансии в JSON-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    json_file_manager.add_vacancy(vacancy)
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1  # Убеждаемся, что дубликат не добавлен

def test_json_file_manager_get_vacancies(json_file_manager):
    """Тест получения вакансий из JSON-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    json_file_manager.add_vacancy(vacancy1)
    json_file_manager.add_vacancy(vacancy2)
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 2
    assert vacancies[0]["title"] == "Test Vacancy 1"
    assert vacancies[1]["title"] == "Test Vacancy 2"

def test_json_file_manager_delete_vacancy(json_file_manager):
    """Тест удаления вакансии из JSON-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    json_file_manager.add_vacancy(vacancy1)
    json_file_manager.add_vacancy(vacancy2)
    json_file_manager.delete_vacancy("test_url_1")
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy 2"

def test_json_file_manager_delete_nonexistent_vacancy(json_file_manager):
    """Тест удаления несуществующей вакансии из JSON-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    json_file_manager.delete_vacancy("nonexistent_url")
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1

def test_json_file_manager_clear_file(json_file_manager):
    """Тест очистки JSON-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    json_file_manager.clear_file()
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 0

def test_json_file_manager_file_not_found(json_file_manager):
    """Тест обработки FileNotFoundError в JSONFileManager."""
    # Удаляем файл, чтобы вызвать FileNotFoundError
    if os.path.exists(json_file_manager._JSONFileManager__filename):
        os.remove(json_file_manager._JSONFileManager__filename)

    vacancies = json_file_manager.get_vacancies()
    assert vacancies == []

def test_json_file_manager_json_decode_error(json_file_manager):
    """Тест обработки JSONDecodeError в JSONFileManager."""
    # Создаем файл с некорректным JSON
    with open(json_file_manager._JSONFileManager__filename, 'w', encoding='utf-8') as f:
        f.write("invalid json")

    vacancies = json_file_manager.get_vacancies()
    assert vacancies == []

# --- Тесты для CSVFileManager ---

def test_csv_file_manager_add_vacancy(csv_file_manager):
    """Тест добавления вакансии в CSV-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy"

def test_csv_file_manager_add_duplicate_vacancy(csv_file_manager):
    """Тест добавления дублирующейся вакансии в CSV-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    csv_file_manager.add_vacancy(vacancy)
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1  # Убеждаемся, что дубликат не добавлен

def test_csv_file_manager_get_vacancies(csv_file_manager):
    """Тест получения вакансий из CSV-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    csv_file_manager.add_vacancy(vacancy1)
    csv_file_manager.add_vacancy(vacancy2)
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 2
    assert vacancies[0]["title"] == "Test Vacancy 1"
    assert vacancies[1]["title"] == "Test Vacancy 2"

def test_csv_file_manager_delete_vacancy(csv_file_manager):
    """Тест удаления вакансии из CSV-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    csv_file_manager.add_vacancy(vacancy1)
    csv_file_manager.add_vacancy(vacancy2)
    csv_file_manager.delete_vacancy("test_url_1")
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy 2"

def test_csv_file_manager_delete_nonexistent_vacancy(csv_file_manager):
    """Тест удаления несуществующей вакансии из CSV-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    csv_file_manager.delete_vacancy("nonexistent_url")
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1

def test_csv_file_manager_clear_file(csv_file_manager):
    """Тест очистки CSV-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    csv_file_manager.clear_file()
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 0

def test_csv_file_manager_file_not_found(csv_file_manager):
    """Тест обработки FileNotFoundError в CSVFileManager."""
    # Удаляем файл, чтобы вызвать FileNotFoundError
    if os.path.exists(csv_file_manager._CSVFileManager__filename):
        os.remove(csv_file_manager._CSVFileManager__filename)

    vacancies = csv_file_manager.get_vacancies()
    assert vacancies == []

# --- Параметризованные тесты ---

@pytest.mark.parametrize(
    "filename, file_manager_class",
    [
        ("test_vacancies.json", JSONFileManager),
        ("test_vacancies.csv", CSVFileManager),
    ],
)
def test_file_manager_creation(tmpdir, filename, file_manager_class):
    """Тест создания объектов FileManager."""
    file_path = tmpdir.join(filename)
    file_manager = file_manager_class(file_path)
    assert isinstance(file_manager, (JSONFileManager, CSVFileManager))