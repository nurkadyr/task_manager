# Task Manager API

## Описание

Это веб-приложение для управления задачами, разработанное с использованием Django и Django REST Framework. Оно включает в себя регистрацию и аутентификацию пользователей, создание, редактирование и удаление задач, назначение задач другим пользователям, отметку задач как выполненные, комментирование задач, прикрепление файлов к задачам, установку дедлайнов и напоминаний, а также фильтрацию и сортировку задач.

## Функциональность

- Регистрация и аутентификация пользователей (JWT)
- CRUD операции для задач
- Назначение задач пользователям
- Отметка задач как выполненные
- Комментирование задач
- Прикрепление файлов к задачам
- Установка дедлайнов и напоминаний
- Фильтрация и сортировка задач
- Документация API (Swagger)

## Технические требования

- Python 3.8+
- Django 3.2+
- Django REST Framework
- djangorestframework-simplejwt
- djoser
- drf-yasg
- django-filter

## Установка и запуск

### Установка зависимостей

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### Применение миграций

Примените миграции базы данных:

```bash
python manage.py migrate
```

### Создание суперпользователя

Создайте суперпользователя для доступа к админке Django:

```bash
python manage.py createsuperuser
```

### Запуск сервера

Запустите сервер разработки:

```bash
python manage.py runserver
```

## Документация API

Документация API доступна по следующим адресам:
- [Swagger](http://127.0.0.1:8000/swagger/)
- [Redoc](http://127.0.0.1:8000/redoc/)

## Примеры запросов

### Регистрация пользователя

POST `/api/auth/users/`

```json
{
    "email": "user@example.com",
    "username": "user",
    "password": "password123",
    "re_password": "password123"
}
```

### Получение JWT токена

POST `/api/auth/jwt/create/`

```json
{
    "username": "user",
    "password": "password123"
}
```

### Создание задачи

POST `/api/tasks/`

```json
{
    "title": "New Task",
    "description": "Task description",
    "assigned_to_id": 1,
    "deadline": "2024-06-30T12:00:00Z",
    "reminder": "2024-06-29T12:00:00Z"
}
```

### Обновление задачи

PUT `/api/tasks/{id}/`

```json
{
    "title": "Updated Task",
    "description": "Updated description",
    "assigned_to_id": 1,
    "completed": true,
    "deadline": "2024-06-30T12:00:00Z",
    "reminder": "2024-06-29T12:00:00Z"
}
```

### Удаление задачи

DELETE `/api/tasks/{id}/`

### Прикрепление файла к задаче

POST `/api/files/`

```json
{
    "task": 1,
    "file": "path/to/your/file"
}
```

## Тестирование

Запуск тестов:

```bash
python manage.py test
```

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности см. в файле LICENSE.
