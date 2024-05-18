FROM python:3.9

# Установите рабочую директорию
WORKDIR /workdir

# Скопируйте файлы проекта в контейнер
COPY . /workdir

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt
