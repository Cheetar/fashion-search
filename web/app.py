import os
import time

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='', static_folder='', template_folder='')
app.config['UPLOAD_FOLDER'] = './img'


@app.route('/album.css')
def css():
    return app.send_static_file('album.css')


@app.route('/script.js')
def js():
    return app.send_static_file('script.js')


@app.route('/')
def index():
    recents = []
    for i in range(9):
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
    time.sleep(5)
    response = {
        'uploaded_image': url_for('uploaded_file', filename=filename),
        'found_image': 'https://a.allegroimg.com/s512/11ce31/a0b4b7cc472d99c06ebc6ba5512b/TOSTER-OPIEKACZ-DO-KANAPEK-SANDWICH-700W-TITANUM',
        'price': '1337.21 zł',
        'url': 'https://allegro.pl/oferta/toster-opiekacz-do-kanapek-sandwich-700w-titanum-9362262596'
    }
    return jsonify(response)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
