
import os
import time
import pymysql

def open_connection():
    username = "dbuser"
    password = 'dbuser' #os.environ["MARIADB_ROOT_PASSWORD"]
    host = "db"
    database = "testdb"
    return pymysql.connect(host, username, password, database)

def init_schema(db):
    cursor = db.cursor()
    try:
        cursor.execute("""
CREATE TABLE images (
    id INTEGER NOT NULL PRIMARY KEY,
    image_path VARCHAR(1000) NOT NULL,
    price INTEGER NOT NULL,
    store_link VARCHAR(2000) NOT NULL,
    vec LONGTEXT NOT NULL
);
""")
    except:
        pass


def main():
    time.sleep(5)
    db = open_connection()
    init_schema(db)

if __name__ == "__main__":
    main()
