import paramiko
import psycopg2
from typing import Callable

from config import config

db = config.db


def connect_with_database(f: Callable):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            dbname=db.DB_HOST,
            user=db.DB_USER,
            password=db.DB_PASSWORD,
            host=db.DB_HOST,
            port=db.DB_PORT
        )
        cur = conn.cursor()

        print('соединение с сервером установлено')

        key = paramiko.Ed25519Key.from_private_key_file(db.SSH_KEY_PATH, db.SSH_KEY_PASSPHRASE)
        transport = paramiko.Transport((db.SSH_HOST, db.SSH_PORT))
        transport.connect(username=db.SSH_USERNAME, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print('sftp соединение установлено')
        ssh = paramiko.SSHClient()
        ssh._transport = transport

        try:
            f((sftp, ssh), (cur, conn))
        finally:
            try:
                sftp.close()
            except Exception:
                pass
            try:
                ssh.close()
            except Exception:
                pass
            try:
                transport.close()
            except Exception:
                pass
            try:
                cur.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

    return wrapper

