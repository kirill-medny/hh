import pytest
from src.api_client import HeadHunterAPI, APIClient
import requests
import os
import json
import csv
from src.file_manager import JSONFileManager, CSVFileManager
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

@pytest.fixture
def hh_api():
    return HeadHunterAPI()

@pytest.fixture
def json_file_manager(tmpdir):
    """Фикстура для создания временного JSONFileManager."""
    filename = tmpdir.join("test_vacancies.json")
    file_manager = JSONFileManager(filename)
    yield file_manager
    if os.path.exists(filename):
        os.remove(filename)


@pytest.fixture
def csv_file_manager(tmpdir):
    """Фикстура для создания временного CSVFileManager."""
    filename = tmpdir.join("test_vacancies.csv")
    file_manager = CSVFileManager(filename)
    yield file_manager
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def mock_hh_api():
    """Фикстура для мокирования HeadHunterAPI."""
    with patch("src.utils.HeadHunterAPI") as MockHeadHunterAPI:
        mock_api = MockHeadHunterAPI.return_value
        yield mock_api

@pytest.fixture
def sample_hh_item():
    """Фикстура для создания sample_hh_item."""
    return {
        "name": "Python Developer",
        "alternate_url": "https://example.com/vacancy/123",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "snippet": {"requirement": "Python, Django", "responsibility": "Develop web applications"},
    }

@pytest.fixture
def sample_vacancy():
    """Фикстура для создания sample_vacancy."""
    return Vacancy(
        title="Python Developer",
        url="https://example.com/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        description="Python, Django Develop web applications",
    )