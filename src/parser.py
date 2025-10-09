import numpy as np
import requests
import time
from tqdm import tqdm
import re

def get_it_roles():
    '''Возвращает специализации в IT в виде списка строк.

    В список не включён менеджмент и руководящие должности.
    '''

    # Адрес с профессиональными ролями
    url = 'https://api.hh.ru/professional_roles'
    response = requests.get(url)  # GET запрос
    jsn = response.json().get('categories')

    # Собиараем словарь IT-специализации
    it_dict = dict()
    for i in jsn:
        if i.get('id') == '11':
            it_dict.update(i)

    # Собираем роли без менеждмента и техподдержки
    it_roles = [i.get('id') for i in it_dict.get('roles') if  i.get('id') not in ['12', '36', '73', '155', '104', '157', '107', '125', '121']]
    return it_roles  # возвращаем список

    # id ролей только в аналитике
    # analytics = ['165', '156', '10', '150', '164', '148']

def get_vacancies(period=30, cities=['1', '2', '3', '4', '88'], roles=get_it_roles()):
    '''
    Отбирает вакансии без описания и ключевых навыков.

    Параметры:
    - period - период публикации в днях, по умолчанию 30
    - города - топ-5 по населению в РФ: Москва, СПб, Екат, НСК, Казань
    - роли - список из предыдущей функции
    '''

    # Первоначальная настройка
    url = 'https://api.hh.ru/vacancies'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent}
    page = 0
    vacancies = []

    # Прогресс-бар
    pbar = tqdm(total=19, desc='Parsing', colour='green', position=0)
    session = requests.Session()

    # Цикл для отбора
    while page <= 19:
        params = {
            'area': cities,
            'industry': 7,
            'professional_role': roles,
            'per_page': 100,
            'currency': 'RUR',
            'only_with_salary': 'true',
            'page': page,
            'period': period,
            }
        # Проверка на ошибки запроса и сбор данных
        try:
            response = session.get(url, params=params, headers=headers)
            if response.status_code == 200:
                jsn = response.json().get('items')

                if len(jsn) > 0:
                    for i in jsn:
                        vacancies.append(
                            {
                               'id': i.get('id'),
                               'name': i.get('name'),
                               'group': [j.get('name') for j in i.get('professional_roles')][0],
                               'city': i.get('area').get('name'),
                               'salary_from': np.nan if i.get('salary') is None else i.get('salary').get('from'),
                               'salary_to': np.nan if i.get('salary') is None else i.get('salary').get('to'),
                               'employer': i.get('employer').get('name'),
                               'work_format': [j.get('id') for j in i.get('work_format')],
                               'experience': i.get('experience').get('name')
                            }
                        )
                    page += 1  # обновление страницы
                    pbar.update(1)

                    # Таймауты для избежания бана со стороны API
                    timeout = np.random.uniform(0.5, 2.0)
                    time.sleep(timeout)
                else:
                    break
            else:
                print(response.status_code)
                break

        except requests.ConnectionError as cr:
            print(f'Ошибка подключения: {cr}')
        except requests.RequestException as re:
            print(f'Ошибка запроса: {re}')

    # Закрытие сессии и возврат списка
    pbar.close()
    session.close()
    return vacancies

def get_ids(lst):
    '''Собирает id вакансий из списка словарей в отдельный список.'''

    ids = []
    for i in lst:
        ids.append(i['id'])
    return ids

def get_descriptions(ids, vacancies):
    '''
    Возвращает вакансии с добавленными навыками и описанием.

    Параметры:
    - ids - id вакансий
    - vacancies - список словарей с вакансиями для обновления
    '''

    # Первоначальная настройка
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent}
    pbar = tqdm(total=len(vacancies), desc='Getting descriptions', colour='red', position=0)

    # Итерируемся с использованием функции zip, чтобы использовать одновременно оба списка
    session = requests.Session()
    for vacancy_id, vacancy in zip(ids, vacancies):
        url = f'https://api.hh.ru/vacancies/{vacancy_id}'

        # Проверка на ошибки и сбор дополнительных данных
        try:
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                jsn = response.json()
                key_skills = [skill.get('name') for skill in jsn.get('key_skills', [])] if jsn.get('key_skills') else []

                # Очистка описания от HTML-тэгов
                description_raw = jsn.get('description') or ''
                description_clean = re.sub(r'<[^>]+>', '', description_raw)
                vacancy.update({'key_skills': key_skills, 'description': description_clean})
            else:
                print(response.status_code)
                continue
        except requests.RequestException as req:
            print(f'Ошибка запроса: {req}')
        except requests.ConnectionError as cr:
            print(f'Ошибка подключения: {cr}')
        finally:
            # Логгирование и таймауты
            pbar.update(1)
            time.sleep(np.random.uniform(0.5, 2.0))

    # Закрытие сессии и возврат списка
    pbar.close()
    session.close()
    return vacancies
