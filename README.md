# YaMDb API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

API для сервиса отзывов на произведения (книги, фильмы, музыку).

## 📝 Описание

Проект **YaMDb** позволяет пользователям оставлять отзывы и оценки произведениям, а также комментировать отзывы других пользователей.

## Как запустить проект:

### Cоздать и активировать виртуальное окружение:

```bash
python -m venv env
```

* Если у вас Linux/macOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

```bash
python -m pip install --upgrade pip
```

### Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

### Выполнить миграции:

```bash
python manage.py migrate
```

### Запустить проект:

```bash
python manage.py runserver
```

### 🔐 Алгоритм регистрации пользователей
1. Отправка POST-запроса с `email` и `username` на `/api/v1/auth/signup/`
2. Получение кода подтверждения (`confirmation_code`) на email
3. Отправка POST-запроса с `username` и `confirmation_code` на `/api/v1/auth/token/` для получения JWT-токена
4. (Опционально) Заполнение профиля через PATCH-запрос на `/api/v1/users/me/`

## 👥 Пользовательские роли
| Роль | Права |
|------|-------|
| **Аноним** | Просмотр описаний произведений, чтение отзывов и комментариев |
| **Пользователь** (`user`) | Чтение + публикация отзывов, комментарии, оценка произведений |
| **Модератор** (`moderator`) | Права пользователя + удаление любых отзывов/комментариев |
| **Администратор** (`admin`) | Полные права на управление контентом и пользователями |
| **Суперюзер Django** | Права администратора |

## Требования
- Python 3.7+
- Django 3.2+
- DRF 3.12+
- JWT

## 📄 API-документация (ReDoc)

```html
<!DOCTYPE html>
<html>
  <head>
    <title>YaMDb API Docs</title>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
  </head>
  <body>
    <redoc spec-url="api_yamdb/static/redoc.yaml"></redoc>
  </body>
</html>
```
