import numpy as np
import pandas as pd
import re
import ast
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def main():
    path = input('Укажите путь к файлу: ')
    data = pd.read_csv(path)
    copy = data.copy()

    copy = copy[copy['currency'] != 'USD']
    copy = copy[copy['city'].isin([
        "Москва",
        "Санкт-Петербург",
        "Новосибирск",
        "Екатеринбург",
        "Казань",
        "Ростов-на-Дону",
        "Нижний Новгород",
        "Челябинск",
        "Омск",
        "Самара",
    ])]
    copy['name'] = np.where(copy['name'], copy['name'].str.lower(), copy['name'])

    mask = copy['name'].str.contains(r'1[СC]', flags=re.I, na=False)
    copy.loc[mask, 'name'] = 'Аналитик 1С'

    mask = (copy['name'].str.contains('fullstack', flags=re.I, na=False) | copy['name'].str.contains('full stack', flags=re.I, na=False) | copy['name'].str.contains('фуллстек', flags=re.I, na=False) |
        copy['name'].str.contains('full -stack', flags=re.I, na=False) | copy['name'].str.contains('фулстек', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Фуллстек аналитик'

    mask = (copy['name'].str.contains('системный', flags=re.I, na=False) | copy['name'].str.contains('system', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Системный аналитик'

    mask = (copy['name'].str.contains('продуктовый', flags=re.I, na=False) | copy['name'].str.contains('product', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Продуктовый аналитик'

    mask = (copy['name'].str.contains('бизнес', flags=re.I, na=False) | copy['name'].str.contains('business', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Бизнес-аналитик'

    mask = (copy['name'].str.contains('bi', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'BI-аналитик'

    mask = (copy['name'].str.contains('ml', flags=re.I, na=False) | copy['name'].str.contains('science', flags=re.I, na=False) | copy['name'].str.contains('scientist', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'ML-разработчик'

    mask = (copy['name'].str.contains('nlp', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'NLP-разработчик'

    mask = (copy['name'].str.contains('cv', flags=re.I, na=False) | copy['name'].str.contains('computer vision', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'CV-разработчик'

    mask = (copy['name'].str.contains('инженер', flags=re.I, na=False) | copy['name'].str.contains('engineer', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Инженер данных'

    mask = (copy['name'].str.contains('dwh', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'DWH-разработчик'

    mask = (copy['name'].str.contains('архитект', flags=re.I, na=False) | copy['name'].str.contains('architect', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'IT-архитектор'

    mask = (copy['name'].str.contains('консультант', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Консультант'

    mask = (copy['name'].str.contains('веб', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Веб-аналитик'

    mask = (copy['name'].str.contains('hr', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'HR-аналитик'

    mask = (copy['name'].str.contains('инженер', flags=re.I, na=False) | copy['name'].str.contains('engineer', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Инженер данных'

    mask = (copy['name'].str.contains('риск', flags=re.I, na=False) | copy['name'].str.contains('risk', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Риск-аналитик'

    exclude = {
        "Аналитик 1С", "Системный аналитик", "Бизнес-аналитик", "Аналитик данных",
        "Консультант", "Фуллстек аналитик", "HR-аналитик", "Риск-аналитик", "Веб-аналитик",
    }

    # Ищем слово 'аналитик' или 'analyst' как отдельное слово, регистронезависимо
    pat = re.compile(r'(?i)\b(аналитик|analyst|аналитики)\b')

    mask = (
        ~copy['name'].isin(exclude)
        & copy['name'].str.contains(pat, na=False)
    )

    copy.loc[mask, 'name'] = 'Аналитик'

    mask = (copy['name'].str.contains('менеджер', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Менеджер'
    mask = (copy['name'].str.contains('специалист', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Специалист'

    mask = (copy['name'].str.contains('pl', flags=re.I, na=False) | copy['name'].str.contains('sql', flags=re.I, na=False) | copy['name'].str.contains('баз данных', flags=re.I, na=False))
    copy.loc[mask, 'name'] = 'Разработчик БД'

    def salary_imputer(df):
        roles = df['role'].unique()

        for i in roles:
            df.loc[df['role'] == i, 'salary_from'] = df.loc[df['role'] == i, 'salary_from'].fillna(df.loc[df['role'] == i, 'salary_from'].median())
            df.loc[df['role'] == i, 'salary_to'] = df.loc[df['role'] == i, 'salary_to'].fillna(df.loc[df['role'] == i, 'salary_to'].median())

        return df

    new_df = salary_imputer(copy)
    new_df['currency'].fillna('RUR', inplace=True)

    def fmt_converter(s):
        s = s.strip().lower()
        s = ast.literal_eval(s)
        if s == []:
            return 'не указано'
        elif len(s) == 1:
            if s[0] == 'on_site':
                return 'в офисе'
            if s[0] == 'remote':
                return 'удалённо'
            if s[0] == 'hybrid':
                return 'гибрид'
        elif len(s) > 1:
            return 'гибрид'

    new_df['fmt'] = new_df['fmt'].apply(fmt_converter)

    new_df = new_df[new_df['fmt'] != 'выездная работа']

    new_df['experience'] = new_df['experience'].str.lower()

    def grade_col(text):
        text = text.lower().strip()
        if text == 'нет опыта':
            return 'стажёр/junior'
        elif text == 'от 1 года до 3 лет':
            return 'junior+/middle'
        elif text == 'от 3 до 6 лет':
            return 'middle+/senior'
        else:
            return 'senior+'

    new_df['grade'] = new_df['experience'].apply(grade_col)

    new_df.loc[new_df['employer'].str.contains('Газпромбанк'), 'employer'] = 'Газпромбанк'
    new_df.loc[new_df['employer'].str.contains('X5'), 'employer'] = 'X5'
    new_df.loc[new_df['employer'].str.contains('Х5'), 'employer'] = 'X5'
    new_df.loc[new_df['employer'].str.contains('Газпром') & ~new_df['employer'].str.contains('Газпромбанк'), 'employer'] = 'Газпром'

    new_df['date'] = pd.to_datetime(new_df['date'], format="ISO8601")
    new_df['date'] = pd.to_datetime(new_df['date'], format="%d-%m-%Y")
    new_df['date'] = new_df['date'].dt.date

    def parse_skills(text):
        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return []

    new_df['key_skills'] = new_df['key_skills'].apply(parse_skills)

    # Будем брать топ-5 навыков
    top_skills_group = {}

    for group, group_df in new_df.groupby('role'):
        all_skills = sum(group_df['key_skills'].to_list(), [])
        # Создаём объект счётчика
        skill_counts = Counter(all_skills)
        # CСобираем топ-скиллы
        top_skills = [skill for skill, count in skill_counts.most_common(5)]
        top_skills_group[group] = top_skills

    # Напишем функцию для заполнения пустых списков навыков по ролям
    def fill_empty_skills(row):
        if isinstance(row['key_skills'], list) and len(row['key_skills'])== 0:
            # Заполняем значениями и меняем дефолт с None на пустой список
            return top_skills_group.get(row['role'], [])
        else:
            return row['key_skills']

    new_df['key_skills'] = new_df.apply(fill_empty_skills, axis=1)

    try:
        new_df.to_csv('/content/hr_analytics/data/processed/processed.csv', index=False)
    except Exception as e:
        print(f'Ошибка загрузки: {e}')

if __name__ == "__main__":
    main()
