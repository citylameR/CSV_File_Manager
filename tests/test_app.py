import pytest
import json
import base64
from app import app
import csv


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def read_test_user_credentials():
    # Читаем учетные данные пользователей из файла test_user.csv
    credentials = {}
    with open('test_user.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            credentials[row['username']] = row['password']
    return credentials


def test_upload_file(client):
    # Проверяем загрузку файла
    # Создаем строку с авторизационными данными 'admin:password'
    credentials = base64.b64encode(b'admin:password').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}

    response = client.post('/upload', data={'file': (open('test.csv', 'rb'), 'test.csv')}, headers=headers)
    assert response.status_code == 200
    assert b'File uploaded successfully' in response.data


def test_get_files(client):
    # Проверяем получение списка файлов
    # Создаем строку с авторизационными данными 'admin:password'
    credentials = base64.b64encode(b'admin:password').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}

    response = client.get('/files', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data['files'], list)
    assert 'test.csv' in data['files']


def test_get_data(client):
    # Проверяем получение данных из файла
    # Создаем строку с авторизационными данными 'admin:password'
    credentials = base64.b64encode(b'admin:password').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}

    client.post('/upload', data={'file': (open('test.csv', 'rb'), 'test.csv')})
    response = client.get('/data/test.csv', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_data_with_filter_and_sort(client):
    credentials = base64.b64encode(b'admin:password').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}
    # Проверяем получение данных из файла с фильтрацией и сортировкой
    client.post('/upload', data={'file': (open('test.csv', 'rb'), 'test.csv')})

    # Применяем фильтр и сортировку
    response = client.get('/data/test.csv?filter=column1=value1&sort=column2', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_delete_file(client):
    # Проверяем удаление файла
    # Создаем строку с авторизационными данными 'admin:password'
    credentials = base64.b64encode(b'admin:password').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}

    client.post('/upload', data={'file': (open('uploads/test.csv', 'rb'), 'test.csv')})

    response = client.delete('/delete/test.csv', headers=headers)
    assert response.status_code == 200
    assert b'File test.csv deleted successfully' in response.data


if __name__ == '__main__':
    pytest.run()
