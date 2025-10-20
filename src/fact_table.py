import pandas as pd
import os

def fact_table(dim_tables, fact):
    '''
    Функция собирает таблицу фактов на основе таблиц измерений.
    '''
    
    frames = [pd.read_excel(x) for x in dim_tables]
    data = pd.read_excel(fact)

    data = data.merge(frames[0], how='inner', on='city')
    data = data.merge(frames[1], how='inner', on='employer')
    data = data.merge(frames[2], how='inner', on='experience')
    data = data.merge(frames[3], how='inner', on='work_format')
    data = data.merge(frames[4], how='inner', on='grade')
    data = data.merge(frames[5], how='inner', on='group')

    data.drop(columns=['city', 'employer', 'experience', 'work_format', 'grade', 'group'], inplace=True)

    os.mkdir(r'Z:\Repos\folder\hr_analytics\data\db_data\fact_table')

    data.to_excel(r'Z:\Repos\folder\hr_analytics\data\db_data\fact_table\fact_table.xlsx', index=False)

if __name__ == "__main__":
    lst = [
        r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\cities.xlsx',
        r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\employers.xlsx',
        r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\exp.xlsx',
        r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\format.xlsx',
        r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\grade.xlsx',
        r'Z:\Repos\folder\hr_analytics\data\db_data\dimensions\roles.xlsx'
    ]
    f = r'Z:\Repos\folder\hr_analytics\data\processed\processed.xlsx'

    fact_table(lst, f)