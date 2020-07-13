
import os
import time
import pymysql
import requests
import hashlib
from bs4 import BeautifulSoup
from mimetypes import guess_extension

def open_connection():
    username = os.environ["MARIADB_USERNAME"]
    password = os.environ["MARIADB_PASSWORD"]
    host = "db"
    database = os.environ["MARIADB_DATABASE"]
    return pymysql.connect(host, username, password, database)



def init_schema(db):
    cursor = db.cursor()
    try:
        cursor.execute("""
CREATE TABLE images (
    id INTEGER NOT NULL AUTO_INCREMENT,
    image_path VARCHAR(1000),
    price INTEGER,
    store_link VARCHAR(2000),
    vec LONGTEXT,
    PRIMARY KEY(id)
);
""")
    except pymysql.err.InternalError as e:
        print(e)
    try:
        cursor.execute("""
CREATE TABLE history (
    id INTEGER NOT NULL AUTO_INCREMENT,
    searched_image INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(searched_image) REFERENCES images(id)
);
""")
    except pymysql.err.InternalError as e:
        print(e)

def add_img_to_db(db, path, link, price):
    cursor = db.cursor()
    cursor.execute("INSERT INTO images (id, image_path, price, store_link, vec) VALUES (NULL, %s, %s, %s, NULL)", (path, str(price), link))
    db.commit()

class Allani:
    def __init__(self, db):
        self.db = db
        self.url = "https://allani.pl/wyszukaj/sukienki?page={}"

    def download_page(self, page_nr: int):
        url = self.url.format(page_nr)
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'html.parser')
        return soup

    def download_img(self, link):
        try:
            response = requests.get(link)
        except:
            return None
        file_extension = guess_extension(response.headers['Content-Type'].partition(';')[0].strip())
        with open("/app/img/" + hashlib.sha256(response.content).hexdigest() + file_extension, 'wb') as f:
            f.write(response.content)
        print(" Downloaded: {}".format(link))
        time.sleep(0.5)

    def format_price(self, price):
        return int(price.replace("zł", "").replace(".", ""))

    def scrape(self):
        print("__ SCRAPING __")
        page_nr = 0
        links, prices = self.parse_page(self.download_page(page_nr))
        while links:
            for (link, price) in zip(links, prices):
                path = self.download_img(link)
                add_img_to_db(self.db, path, link, self.format_price(price))
            page_nr += 1
            links, prices = self.parse_page(self.download_page(page_nr))


    def parse_page(self, page):
        links = []
        prices = []
        for entry in page.find_all(class_="tile--product-r__content"):
            prices.append(entry.find_all(class_='product-prices')[0].findChild().contents[0])
            links.append(entry.find_all(class_='tile--product-r__image-container__image')[0].get("src"))
        return links, prices


def main():
    print(os.listdir("/app/img"))
    time.sleep(5)
    db = open_connection()
    init_schema(db)
    Allani(db).scrape()
if __name__ == "__main__":
    main()
