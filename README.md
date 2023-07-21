# CSV File Manager

Проект "CSV File Manager" - это простое веб-приложение на базе Flask, которое позволяет загружать, просматривать и удалять файлы в формате CSV, а также получать данные из загруженных файлов с возможностью фильтрации и сортировки.

## Установка и запуск

1. Клонируйте репозиторий:

```
git clone https://github.com/your-username/csv-file-manager.git
cd csv-file-manager
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

3. Запустите сервер Flask:

```
flask run
```


Приложение будет доступно по адресу `http://127.0.0.1:5000/`.

## Docker

Вы также можете запустить приложение в контейнере Docker. Для этого выполните команды:

```
docker build -t csv-file-manager .
docker run -p 8888:8888 csv-file-manager
```

Приложение будет доступно по адресу `http://127.0.0.1:8888/`.


## Документация по API

### Загрузка файла

#### Запрос

```
POST /upload
```

#### Параметры

- Файл для загрузки. Передается в теле запроса.

#### Ответы

- Код 200: Файл успешно загружен.
- Код 400: Не передан файл или выбран пустой файл.
- Код 401: Неавторизованный доступ.

---

### Получение списка файлов

#### Запрос

```
GET /files
```

#### Ответы

- Код 200: Список загруженных файлов получен успешно.
- Код 401: Неавторизованный доступ.

#### Пример ответа

```json
{
    "files": ["file1.csv", "file2.csv"]
}
```

---

### Получение данных из файла

#### Запрос

```
GET /data/<file_name>
```

#### Параметры

- `file_name` (строка): Имя загруженного файла.

#### Опциональные параметры

- `filter` (строка): Фильтр данных в формате `column_name=value`. Может быть передано несколько раз для применения нескольких фильтров.
- `sort` (строка): Столбцы для сортировки данных, разделенные запятой.

#### Ответы

- Код 200: Данные из файла получены успешно.
- Код 400: Ошибка разбора файла CSV.
- Код 401: Неавторизованный доступ.
- Код 404: Файл не найден.

#### Пример запроса

```
GET /data/file1.csv?filter=column1=value1&sort=column2
```

#### Пример ответа

```json
[
    {"column1": "value1", "column2": "value2"},
    {"column1": "value3", "column2": "value4"}
]
```

---

### Удаление файла

#### Запрос

```
DELETE /delete/<file_name>
```

#### Параметры

- `file_name` (строка): Имя загруженного файла.

#### Ответы

- Код 200: Файл успешно удален.
- Код 401: Неавторизованный доступ.
- Код 404: Файл не найден.

---

### Аутентификация

Для доступа к большинству эндпоинтов API требуется аутентификация. Используйте заголовок `Authorization` с базовой авторизацией в формате `Basic <base64_encoded_username:password>`.

Пример заголовка:

```
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

Используйте логин `admin` и пароль `password` для успешной аутентификации.



