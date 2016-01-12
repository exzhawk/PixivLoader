import os

from flask import Flask, send_from_directory, send_file

app = Flask(__name__)


@app.route('/')
def index_page():
    return send_file(os.path.join(app.static_folder, "index.html"))


@app.route('/<path:path>')
def static_html(path):
    return send_from_directory(app.static_folder, path)


if __name__ == '__main__':
    app.debug = True
    app.run()
