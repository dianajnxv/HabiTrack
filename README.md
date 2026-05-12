# HabiTrack

Вебсервіс для створення та редагування корисних звичок із використанням мотиваційних інструментів. Дозволяє користувачам ефективно формувати звички, відстежувати їх виконання та підтримувати мотивацію завдяки зручному інтерфейсу та естетичному оформленню.

## Інструкція з запуску

1. Клонування репозиторію:

git clone https://github.com/dianajnxv/HabiTrack

2. Перехід у каталог проєкту:

cd HABITRACK_SH

3. Створення та активація віртуального середовища:

* Для Linux/macOS:

python3 -m venv venv
source venv/bin/activate

* Для Windows:

python -m venv venv
venv\Scripts\activate

4. Встановлення залежностей:

pip install -r requirements.txt

## Налаштування бази даних PostgreSQL через Docker

1. Переконайтеся, що у вас встановлений Docker.

2. Запустіть контейнер з PostgreSQL командою:

docker run --name postgres_habitflow -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=HabitFlow -p 5432:5432 -d postgres

3. Відредагуйте файл `settings.py` у Django, щоб підключитися до цієї бази:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'HabitFlow',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4. Після запуску контейнера виконайте міграції та запустіть сервер:

pip install psycopg2-binary
python manage.py migrate
python manage.py runserver

5. Відкрийте у браузері:
http://127.0.0.1:8000/