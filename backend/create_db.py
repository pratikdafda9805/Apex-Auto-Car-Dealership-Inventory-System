import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "root")
host = os.getenv("MYSQL_HOST", "localhost")
port = int(os.getenv("MYSQL_PORT", 3306))
db_name = os.getenv("MYSQL_DB", "car_dealership")

try:
    conn = pymysql.connect(host=host, port=port, user=user, password=password)
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
    conn.close()
    print(f"Successfully created or verified database '{db_name}'.")
except Exception as e:
    print(f"Error connecting to MySQL or creating database: {e}")
