import os
import paramiko
import psycopg2
from typing import Callable
from dotenv import load_dotenv

load_dotenv()

def connect_with_database(f: Callable):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT'))
        )
        cur = conn.cursor()

        print('соединение с сервером установлено')

        key = paramiko.Ed25519Key.from_private_key_file(os.getenv('SSH_KEY_PATH'), os.getenv('SSH_KEY_PASSPHRASE'))
        transport = paramiko.Transport((os.getenv('SSH_HOST'), int(os.getenv('SSH_PORT'))))
        transport.connect(username=os.getenv('SSH_USERNAME'), pkey=key)
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

