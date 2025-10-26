import psycopg2
import db_config
import os

# Создаём объект подключения
def db_connect():
    return psycopg2.connect(
        database=db_config.DBNAME,
        user=db_config.USER,
        password=db_config.PASSWORD,
        host=db_config.HOST,
        port=db_config.PORT,
    )

def create_tables():
    conn = None
    try:
        conn = db_connect()
        cur = conn.cursor()

        commands = (
            '''
            CREATE TABLE cities (
                city_id INT PRIMARY KEY,
                name_city VARCHAR(50) NOT NULL
            )
            ''',
            '''
            CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                name_employer VARCHAR(150) NOT NULL
            )
            ''',
            '''
            CREATE TABLE experience (
                exp_id INT PRIMARY KEY,
                exp VARCHAR(20) NOT NULL
            )
            ''',
            '''
            CREATE TABLE format (
                fmt_id INT PRIMARY KEY,
                fmt VARCHAR(15) NOT NULL
            )
            ''',
            '''
            CREATE TABLE grade (
                grade_id INT PRIMARY KEY,
                grade VARCHAR(20) NOT NULL
            )
            ''',
            '''
            CREATE TABLE roles (
                role_id INT PRIMARY KEY,
                role VARCHAR(30) NOT NULL
            )
            ''',
            '''
            CREATE TABLE vacancies (
                id BIGINT PRIMARY KEY,               
                name VARCHAR(255),                    
                salary_from NUMERIC(10,2),             
                salary_to NUMERIC(10,2),               
                currency VARCHAR(10),                 
                date DATE,                            
                key_skills TEXT,                       
                city_id BIGINT,                        
                employer_id BIGINT,                    
                exp_id INT,                            
                fmt_id INT,                            
                grade_id INT,                          
                role_id INT                            
            )
            ''',           
    )
    
        for command in commands:
            cur.execute(command)
        conn.commit()
    except (psycopg2.DatabaseError, Exception) as e:
        print(e)
    finally:
        cur.close()
        conn.close()

# Создаём курсор для загрузки данных
def insert_data():
    # Подключаемся к базе и создаём курсор
    conn = db_connect()
    cur = conn.cursor()
    
    # Отркываем csv-файлы
    lst_paths = os.listdir(r'Z:\Repos\hr_analytics-1\data\db_data')
    full_paths = []
    for item_name in lst_paths:
        full_path = os.path.join(r'Z:\Repos\hr_analytics-1\data\db_data', item_name)
        full_paths.append(full_path)

    # Список имён таблиц
    table_names = ['cities', 'employers', 'experience', 'format', 'grade', 'roles', 'vacancies']

    try:
        for i, j in zip(full_paths, table_names):
            with open(i, 'r', encoding='utf-8') as f:
                cur.copy_expert(
                    f"""COPY {j} FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',', QUOTE '"', ESCAPE "'")""", f)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
    insert_data()