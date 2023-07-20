from flask import Flask, request, jsonify, g
import pandas as pd
import os

from pandas import read_csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Папка для загруженных файлов

USERNAME = 'admin'
PASSWORD = 'password'


def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


def authenticate():
    return jsonify({'error': 'Unauthorized access'}), 401


@app.before_request
def before_request():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    g.user = auth.username


# Создаем папку для загрузки файлов, если она не существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Загрузка файла в формате CSV
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify({'message': 'File uploaded successfully'}), 200


# Получение списка файлов с информацией о колонках
@app.route('/files', methods=['GET'])
def get_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files}), 200


# Получение данных из файла с опциональной фильтрацией и сортировкой по столбцам
@app.route('/data/<string:file_name>', methods=['GET'])
def get_data(file_name):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        df = pd.read_csv(file_path)
    except pd.errors.ParserError:
        return jsonify({'error': 'Invalid CSV format'}), 400

    # Применение опциональной фильтрации
    filters = request.args.getlist('filter')
    for f in filters:
        column, value = f.split('=')
        df = df[df[column] == value]

    # Применение опциональной сортировки
    sort_by = request.args.getlist('sort')
    df = df.sort_values(by=sort_by) if sort_by else df

    return df.to_json(orient='records'), 200


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    os.remove(file_path)
    return jsonify({"message": f"File {filename} deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
