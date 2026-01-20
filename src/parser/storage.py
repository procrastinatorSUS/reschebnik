from typing import List, Tuple, Any
import csv
import os
from datetime import datetime
from psycopg2.errors import UniqueViolation
from .config import fieldnames

def log_res(res: List[int|str], sftp, sql_data:Tuple[str, Any, Any]) -> None:
    tp, num, diff, photo_path, links, ans = res
    with open(os.path.abspath("src\\common\\entities\\parsed_data.csv"), newline='', mode='a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'number': num,
                         'type': tp,
                         'difficulty': diff,
                         'file_path': photo_path,
                         'file_links': links,
                         'answer': ans,
                         'date_create': datetime.now().strftime("%Y%m%d_%H%M%S")
                         })
    cur, conn = sql_data
    sql = """
        INSERT INTO tasks (id, type, difficulty, file_path, file_links, answer, data_create)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
    try:
        cur.execute(sql, (int(num), int(tp), int(diff), photo_path, links, ans, 'NOW()'))
        conn.commit()
        sftp.put(os.path.abspath(f'src\\common\\entities\\photos\\{num}.png'), photo_path)
    except UniqueViolation:
        conn.rollback()
        print('замечено повторение')


