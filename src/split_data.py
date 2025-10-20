import pandas as pd
import os


def dim_tables(path):
    '''
    Функция создаёт таблицы измерений из обработанных данных.
    
    '''
    data = pd.read_excel(path)

    # Роли
    roles = pd.DataFrame({
        'role_id': range(1, len(data['group'].unique()) + 1),
        'group': data['group'].unique()
    })

    # Города
    cities = pd.DataFrame({
        'city_id': range(1, len(data['city'].unique()) + 1),
        'city': data['city'].unique()
    })

    # Работодатели
    employers = pd.DataFrame({
        'employer_id': range(1, len(data['employer'].unique()) + 1),
        'employer': data['employer'].unique()
    })

    # Формат работы
    work_fmt = pd.DataFrame({
        'fmt_id': range(1, len(data['work_format'].unique()) + 1),
        'work_format': data['work_format'].unique()
    })

    # Опыт
    exp = pd.DataFrame({
        'exp_id': range(1, len(data['experience'].unique()) + 1),
        'experience': data['experience'].unique()
    })

    # Грейд
    grade = pd.DataFrame({
        'grade_id': range(1, len(data['grade'].unique()) + 1),
        'grade': data['grade'].unique()
    })

    os.mkdir(r'Z:\\Repos\\folder\\hr_analytics\\data\\db_data\\dimensions\\')

    # Сохраняем в Excel-файлы (используем raw-строки для Windows путей)
    roles.to_excel(r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\roles.xlsx', index=False)
    cities.to_excel(r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\cities.xlsx', index=False)
    employers.to_excel(r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\employers.xlsx', index=False)
    work_fmt.to_excel(r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\format.xlsx', index=False)
    exp.to_excel(r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\exp.xlsx', index=False)
    grade.to_excel(r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\grade.xlsx', index=False)

if __name__ == "__main__":
    path = r'Z:\Repos\folder\hr_analytics\data\processed\processed.xlsx'
    dim_tables(path)