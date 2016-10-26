from flask import Flask, request, redirect, url_for, jsonify
from werkzeug import secure_filename
from tempfile import mkdtemp
from shutil import rmtree
from shutil import unpack_archive
import os, sys
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_folder)
import authorlib
from authorlib.parser import save_book

authordata = authorlib.load_data(project_folder)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return open(os.path.dirname(__file__) + '/index.html').read()

@app.route('/submitfiles', methods=['POST'])
def submitfiles():
    folder = mkdtemp()
    files = []
    for file in request.files:
        filename = secure_filename(request.files[file].filename)
        files.append((request.files[file].filename, filename))
        request.files[file].save(os.path.join(folder, filename))
    result = []
    for file in files:
        try:
            book = open(os.path.join(folder, file[1]), encoding="cp1251").read()
        except:
            result.append({"name": "Название файла: " + file[0], "result": "Поврежденный фаил или неправильная кодировка"})
        else:
            author = authorlib.determine_author(authordata, book)
            result.append({"name": "Название файла: " + file[0], "result": "Автор: " + author})
    rmtree(folder)
    return jsonify(data=result)

@app.route('/submitlink', methods=['POST'])
def submitlink():
    link = request.get_json(force=True, silent=False, cache=False)['link']
    folder = mkdtemp()
    result = []
    try:
        book = open(save_book(link, folder), encoding='cp1251').read()
    except:
        result.append({"name": "URL: " + link, "result": "Недоступная ссылка или неправильная кодировка"})
    else:
        author = authorlib.determine_author(authordata, book)
        result.append({"name": "URL: " + link, "result": "Автор: " + author})
    rmtree(folder)
    return jsonify(data=result)

@app.route('/submitarchive', methods=['POST'])
def submitarchive():
    folder = mkdtemp()
    files = []
    archive = secure_filename(request.files['0'].filename)
    request.files['0'].save(os.path.join(folder, archive))
    result = []
    try:
        unpack_archive(os.path.join(folder, archive), folder + "/archive")
    except:
        result.append({"name": "Ошибка на сервере", "result": "Поврежденный фаил архива или неправильный формат"})
    else:
        for root, dirs, files in os.walk(folder + "/archive"):
            for file in files:
                try:
                    book = open(os.path.join(root, file), encoding="cp1251").read()
                except:
                    result.append({"name": "Название файла: " + file, "result": "Поврежденный фаил или неправильная кодировка"})
                else:
                    author = authorlib.determine_author(authordata, book)
                    result.append({"name": "Название файла: " + file, "result": "Автор: " + author})
    rmtree(folder)
    return jsonify(data=result)
