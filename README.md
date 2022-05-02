Платформа для тестов
===============
Мы предоставляем платформу: каждый пользователь имеет возможность создавать и проходить тесты других людей.

Изначально проект задумывался как сайт, предназаченный для одного теста по истории.

Участники:
* Воробьев Михаил
* Панов Георгий

Технологический стек:
* Python 3.6
* Django 4.0+
* SQLite 3.22+

Инструкция по настройке проекта:
1. Склонировать проект
2. Установить необходимые пакты:
    ```bash
    pip install -r requirements.txt
    ```
3. Создать уникальный ключ приложения.
    ```bash
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; get_random_secret_key()"
   ```
4. Синхронизировать структуру базы данных с моделями: 
    ```bash
    python manage.py migrate
    ```
5. Запустить сайт через команду:
   ```bash
    python manage.py runserver 8000
    ```
