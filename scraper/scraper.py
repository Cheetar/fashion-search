
import os
import time
import pymysql
import requests
from bs4 import BeautifulSoup

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
    except pymysql.err.InternalError as e:
        print(e)
    try:
        cursor.execute("""
CREATE TABLE history (
    id INTEGER NOT NULL,
    searched_image INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(searched_image) REFERENCES images(id)
);
""")
    except pymysql.err.InternalError as e:
        print(e)


def download_page(page_number: int):
    url = "https://allani.pl/wyszukaj/sukienki?page={}".format(page_number)
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    return soup

def get_images(page):
    links = []
    for img in page.find_all(class_="tile--product-r__image-container__image"):
        links.append(img.get("src"))
    return links

def main():
    time.sleep(5)
    db = open_connection()
    init_schema(db)

if __name__ == "__main__":
    main()
