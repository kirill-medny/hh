from src.api_client import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_manager import JSONFileManager
from typing import List, Dict, Optional

def get_vacancies_from_hh(search_query: str, num_pages: int = 1) -> List[Vacancy]:
    """
    Получает вакансии с hh.ru и возвращает список объектов Vacancy.

    Args:
        search_query: Поисковый запрос.
        num_pages: Количество страниц для поиска (по умолчанию 1).

    Returns:
        Список объектов Vacancy, найденных на hh.ru.
    """
    hh_api = HeadHunterAPI()
    vacancies: List[Vacancy] = []
    for page in range(num_pages):
        data = hh_api.get_vacancies(search_query, page)
        if not data or 'items' not in data:
            continue # Пропускаем страницы без данных
        for item in data['items']:
            vacancy = create_vacancy_from_hh_item(item)
            if vacancy:
                vacancies.append(vacancy)
    return vacancies

def create_vacancy_from_hh_item(item: Dict) -> Optional[Vacancy]:
    """
    Создает объект Vacancy из элемента, полученного от API hh.ru.

    Args:
        item: Элемент вакансии в формате JSON от hh.ru.

    Returns:
        Объект Vacancy или None, если не удалось создать.
    """
    try:
        salary_from = item['salary']['from'] if item['salary'] and item['salary']['from'] else 0
        salary_to = item['salary']['to'] if item['salary'] and item['salary']['to'] else 0
    except (TypeError, KeyError):
        salary_from = 0
        salary_to = 0

    try:
        description = item['snippet']['requirement'] or item['snippet']['responsibility'] or ""
    except (TypeError, KeyError):
        description = ""

    try:
        vacancy = Vacancy(
            title=item['name'],
            url=item['alternate_url'],
            salary_from=salary_from,
            salary_to=salary_to,
            description=description
        )
        return vacancy
    except KeyError:
        return None #Возвращаем None, если не удалось создать Vacancy

def display_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Выводит информацию о вакансиях в консоль в удобочитаемом формате.

    Args:
        vacancies: Список объектов Vacancy для отображения.
    """
    if not vacancies:
        print("Нет вакансий для отображения.")
        return

    for vacancy in vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary_from} - {vacancy.salary_to}")
        print(f"Описание: {vacancy.description}")
        print("-" * 20)

def save_vacancies_to_file(vacancies: List[Vacancy], filename: str) -> None:
    """
    Сохраняет список вакансий в JSON-файл.
    """
    file_manager = JSONFileManager(filename)
    for vacancy in vacancies:
        file_manager.add_vacancy(dict(vacancy)) # Используем dict(vacancy)
    print(f"Сохранено {len(vacancies)} вакансий в {filename}")

def load_vacancies_from_file(filename: str) -> List[Vacancy]:
    """
    Загружает список вакансий из JSON-файла и преобразует его в объекты Vacancy.

    Args:
        filename: Имя файла для загрузки.

    Returns:
        Список объектов Vacancy, загруженных из файла.
    """
    file_manager = JSONFileManager(filename)
    vacancy_data = file_manager.get_vacancies()
    vacancies = []
    for data in vacancy_data:
        vacancy = Vacancy(**data) # Создаем Vacancy объект из словаря
        vacancies.append(vacancy)
    return vacancies


def interact_with_user():
    """
    Функция для взаимодействия с пользователем через консоль.
    Организует поиск, фильтрацию и отображение вакансий.
    """
    search_query = input("Введите поисковый запрос: ")
    num_pages = int(input("Сколько страниц поискать? "))
    vacancies = get_vacancies_from_hh(search_query, num_pages)

    if not vacancies:
        print("Нет вакансий, соответствующих запросу.")
        return

    filename = "data/vacancies.json"
    save_vacancies_to_file(vacancies, filename)

    # Получаем топ N вакансий по зарплате
    try:
        n = int(input("Введите количество топ вакансий по зарплате, которые хотите увидеть: "))
        top_vacancies = sorted(vacancies, reverse=True)[:n]  # Сортировка по убыванию
        print("\nТоп вакансии по зарплате:")
        display_vacancies(top_vacancies) #Используем display_vacancies для вывода
    except ValueError:
        print("Некорректный ввод для количества вакансий.")

    # Получаем вакансии с ключевым словом в описании
    keyword = input("Введите ключевое слово для поиска в описании: ")
    keyword_vacancies = [
        vacancy for vacancy in vacancies if keyword.description and keyword.description.lower().find(keyword.lower()) != -1
    ]
    print(f"\nВакансии с ключевым словом '{keyword}':")
    display_vacancies(keyword_vacancies)  #Используем display_vacancies для вывода

# Пример использования (можно удалить после реализации main.py)
if __name__ == '__main__':
    interact_with_user()