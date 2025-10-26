import pandas as pd
import os

def split_data(path):
    '''
    Создаёт таблицы измерений
    
    '''

    data = pd.read_csv(path, index_col=False)

    # Роли
    roles = pd.DataFrame({
        'role_id': range(1, len(data['role'].unique()) + 1),
        'role': data['role'].unique()
    })

    # Города
    cities = pd.DataFrame({
        'city_id': range(1, len(data['city'].unique()) + 1),
        'city': data['city'].unique()
    })
    
    # Формат работы
    fmt = pd.DataFrame({
        'fmt_id': range(1, len(data['fmt'].unique()) + 1),
        'fmt': data['fmt'].unique()
    })

    # Опыт
    exp = pd.DataFrame({
        'exp_id': range(1, len(data['experience'].unique()) + 1),
        'experience': data['experience'].unique()
    })

    # Работодатели
    employers = pd.DataFrame({
        'employer_id': range(1, len(data['employer'].unique()) + 1),
        'employer': data['employer'].unique()
    })

    # Грейд
    grade = pd.DataFrame({
        'grade_id': range(1, len(data['grade'].unique()) + 1),
        'grade': data['grade'].unique()
    })

    roles.to_csv(r'Z:\Repos\hr_analytics-1\data\db_data\dim_roles.csv', index=False)
    cities.to_csv(r'Z:\Repos\hr_analytics-1\data\db_data\dim_cities.csv', index=False)
    employers.to_csv(r'Z:\Repos\hr_analytics-1\data\db_data\dim_employers.csv', index=False)
    fmt.to_csv(r'Z:\Repos\hr_analytics-1\data\db_data\dim_format.csv', index=False)
    exp.to_csv(r'Z:\Repos\hr_analytics-1\data\db_data\dim_exp.csv', index=False)
    grade.to_csv(r'Z:\Repos\hr_analytics-1\data\db_data\dim_grade.csv', index=False)

def fact_table(dim_tables, path):
    '''
    Функция собирает таблицу фактов на основе таблиц измерений.
    '''
    
    frames = [pd.read_csv(x) for x in dim_tables]
    data = pd.read_csv(path)

    data = data.merge(frames[0], how='inner', on='city')
    data = data.merge(frames[1], how='inner', on='employer')
    data = data.merge(frames[2], how='inner', on='experience')
    data = data.merge(frames[3], how='inner', on='fmt')
    data = data.merge(frames[4], how='inner', on='grade')
    data = data.merge(frames[5], how='inner', on='role')

    data.drop(columns=['city', 'employer', 'experience', 'fmt', 'grade', 'role'], inplace=True)
    data.to_csv(r'Z:\Repos\hr_analytics-1\data\db_data\fact_table.csv', index=False)

if __name__ == "__main__":
    path = r'Z:\Repos\hr_analytics-1\data\processed\processed.csv'
    split_data(path)

    lst_paths = os.listdir(r'Z:\Repos\hr_analytics-1\data\db_data')
    full_paths = []
    for item_name in lst_paths:
        full_path = os.path.join(r'Z:\Repos\hr_analytics-1\data\db_data', item_name)
        full_paths.append(full_path)
    fact_table(full_paths, path)
