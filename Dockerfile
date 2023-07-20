# Используем базовый образ с Python
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в рабочую директорию контейнера
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Определяем переменные окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8888

# Запускаем сервер Flask
CMD ["flask", "run"]
