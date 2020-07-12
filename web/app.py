from flask import Flask, render_template

app = Flask(__name__, static_url_path='', static_folder='', template_folder='')


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


@app.route('/album.css')
def css():
    return app.send_static_file('album.css')


@app.route('/script.js')
def js():
    return app.send_static_file('script.js')
