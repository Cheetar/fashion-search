import os
import pymysql
import requests

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='', static_folder='', template_folder='')
app.config['IMAGEDB_FOLDER'] = './img'
app.config['UPLOAD_FOLDER'] = './img'

username = os.environ["MARIADB_USERNAME"]
password = os.environ["MARIADB_PASSWORD"]
host = "db"
database = os.environ["MARIADB_DATABASE"]
db = pymysql.connect(host, username, password, database)


@app.route('/album.css')
def css():
    return app.send_static_file('album.css')


@app.route('/script.js')
def js():
    return app.send_static_file('script.js')


@app.route('/')
def index():
    recents = []

    with db.cursor() as cursor:
        cursor.execute("SELECT history.path, images.img_link, images.store_link, images.price FROM history"
                       " INNER JOIN images ON history.result = images.id"
                       " WHERE history.result IS NOT NULL"
                       " ORDER BY history.id DESC"
                       " LIMIT 9")
        for data in cursor.fetchall():
            recents.append({
                'uploaded_image': url_for('uploaded_file', filename=data[0]),
                'found_image': data[1],
                'price': data[3],
                'url': data[2]
            })

    while len(recents) < 9:
        recents.append({
            'uploaded_image': 'https://cdn.discordapp.com/avatars/725830634609836033/11a830a4bff7db1dffcc80ed1ac64186.png?size=128',
            'found_image': 'https://a.allegroimg.com/s512/11ce31/a0b4b7cc472d99c06ebc6ba5512b/TOSTER-OPIEKACZ-DO-KANAPEK-SANDWICH-700W-TITANUM',
            'price': '1337.21 zł',
            'url': 'https://allegro.pl/oferta/toster-opiekacz-do-kanapek-sandwich-700w-titanum-9362262596'
        })

    return render_template('index.html', recents=recents)


@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # TODO: change to sha?

    with db.cursor() as cursor:
        cursor.execute("INSERT INTO history (id, path, result) VALUES (NULL, %s, NULL)", (filename,))
        db.commit()
        cursor.execute('SELECT LAST_INSERT_ID() from history')
        inserted_id = cursor.fetchone()[0]

    r = requests.get("http://ai:3000/find/%d" % inserted_id)
    if r.status_code != 200:
        return r.text, r.status_code
    distances = r.json()

    with db.cursor() as cursor:
        cursor.execute("UPDATE history SET result = %d WHERE id = %d", (distances[0]['id'], inserted_id))
    db.commit()

    with db.cursor() as cursor:
        cursor.execute("SELECT images.img_link, images.store_link, images.price FROM history"
                       "INNER JOIN images ON history.result = images.id"
                       "WHERE history.id = %d", (inserted_id,))
        data = cursor.fetchone()

    response = {
        'uploaded_image': url_for('uploaded_file', filename=filename),
        'found_image': data[0],
        'price': data[2],
        'url': data[1]
    }
    return jsonify(response)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
