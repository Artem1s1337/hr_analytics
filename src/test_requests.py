import requests

url = 'https://api.hh.ru/vacancies'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent}
params = {
    'area': 1, # регион, город, населенный пункт: строка,
    'industry': 7, # IT-индустрия,
    'professional_role': 10, # профессиональные роли: строка или список строк,
    'per_page': 1,  # кол-во на страницу
    'currency': 'RUR',  # валюта
    'page': 0,  # номер страницы
    'only_with_salary': 'true',  # только с зарплатой
    'period': 30,  # публикации за месяц (30 дней)
    }

r = requests.get(url, headers=headers, params=params)
jsn = r.json()
