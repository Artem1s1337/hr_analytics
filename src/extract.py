import numpy as np
import pandas as pd
import requests
import time
from tqdm import tqdm

def get_vacancies(roles, cities, period=180):

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
                               'salary_from': np.nan if i.get('salary') is None else i.get('salary').get('from'),
                               'salary_to': np.nan if i.get('salary') is None else i.get('salary').get('to'),
                               'currency': np.nan if i['salary'] is None else i.get('salary').get('currency'),
                               'role': [j.get('name') for j in i.get('professional_roles')][0],
                               'city': i.get('area').get('name'),
                               'fmt': [j.get('id') for j in i.get('work_format')],
                               'experience': i.get('experience').get('name'),
                               'employer': i.get('employer').get('name'),
                               'date': i.get('published_at')
                            }
                        )
                    page += 1  # обновление страницы
                    pbar.update(1)

                    # Таймауты для избежания бана со стороны API
                    timeout = np.random.uniform(0.5, 1.0)
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

def get_skills(ids, vacancies):

    # Первоначальная настройка
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent}
    pbar = tqdm(total=len(vacancies), desc='Getting skills', colour='red', position=0)

    # Итерируемся с использованием функции zip, чтобы использовать одновременно оба списка
    session = requests.Session()
    for vacancy_id, vacancy in zip(ids, vacancies):
        url = f'https://api.hh.ru/vacancies/{vacancy_id}'

        # Проверка на ошибки и сбор дополнительных данных
        try:
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                jsn = response.json()
                key_skills = [skill.get('name') for skill in jsn.get('key_skills', [])] if jsn.get('key_skills') else np.nan
                vacancy.update({'key_skills': key_skills})
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

def main():
    # Роли в аналитике и ML
    analytics = ['165', '156', '10', '150', '164', '148']

    # Топ-10 городов России по населению
    cities = [1, 2, 3, 4, 115, 88, 104, 68, 78, 76]

    vac = get_vacancies(analytics, cities)
    ids = get_ids(vac)
    full_vac = get_skills(ids, vac)
    df = pd.DataFrame(full_vac)
    df.to_csv('vacancies.csv', index=False)
  
if __name__ == "__main__":
    main()
