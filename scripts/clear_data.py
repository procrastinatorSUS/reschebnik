import csv
import os
import shutil
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.common.database.connection import connect_with_database
from src.parser.config import fieldnames
from src.common.config import config

db = config.db

def clear_csv():
    try:
        with open(os.path.abspath("src\\common\\entities\\parsed_data.csv"), newline='', mode='w+') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            file.close()
        print('parsed_data.csv очищен')
    except Exception as e:
        print(f'ошибка при очистке parsed_data.csv: {e}')

def clear_photos_pc():
    try:
        path = os.path.abspath("src/common/entities/photos")
        shutil.rmtree(path)
        os.makedirs(path)
        print('папка photos очищена')
    except Exception as e:
        print(f'ошибка при очистке photos на стороне клиента: {e}')

def clear_table(sql_data):
    try:
        cur, conn = sql_data
        cur.execute("TRUNCATE TABLE tasks CASCADE;")
        conn.commit()
        print('таблица tasks очищена')
    except Exception as e:
        print(f'ошибка при очистке таблицы tasks: {e}')

def clear_photos_server(ssh):
    try:
        ssh.exec_command(f'rm -rf {db.SERVER_PHOTO_DIR_PATH} && mkdir {db.SERVER_PHOTO_DIR_PATH}')
        print('данные на севрере удалены')
    except Exception as e:
        print(f'ошибка при очистке заданий на стороне сервера: {e}')




@connect_with_database  
def main(server, sql_data):
    sftp, ssh = server
    clear_csv()    
    clear_photos_pc()
    clear_table(sql_data)
    clear_photos_server(ssh)




if __name__ == '__main__':
    main()