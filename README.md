# YaMDb API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

API для сервиса отзывов на произведения (книги, фильмы, музыку).

## 📝 Описание

Проект **YaMDb** позволяет пользователям оставлять отзывы и оценки произведениям, а также комментировать отзывы других пользователей.

## Технологии:
* Python 3.10
* Django 3.2.16
* Django REST framework 3.12.4
* djangorestframework-simplejwt 4.7.2

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

## 📄 API-документация

![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-success?logo=openapi-initiative)
![JWT Auth](https://img.shields.io/badge/Auth-JWT-orange?logo=json-web-tokens)
![Django REST](https://img.shields.io/badge/Django_REST-3.12-blue?logo=django)

# YaMDb API
запросы к API начинаются с `/api/v1/`
# Описание
Проект **YaMDb** собирает отзывы пользователей на различные произведения.
# Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).
# Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. 
- **Суперюзер Django** — обладет правами администратора (`admin`)

## Servers:
  ### /api/v1/
  

## Endpoints:

### 1. /auth/signup/

#### POST
##### Description:

Получить код подтверждения на переданный `email`.
Права доступа: **Доступно без токена.**
Использовать имя 'me' в качестве `username` запрещено.
Поля `email` и `username` должны быть уникальными.
Должна быть возможность повторного запроса кода подтверждения.


##### Parameters:

No parametrs

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |

### 2. /auth/token/

#### POST
##### Description:

Получение JWT-токена в обмен на username и confirmation code.
Права доступа: **Доступно без токена.**


##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 404 | Пользователь не найден |

### 3. /categories/

#### GET
##### Description:

Получить список всех категорий
Права доступа: **Доступно без токена**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| search | query | Поиск по названию категории | No | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

#### POST
##### Description:

Создать категорию.
Права доступа: **Администратор.**
Поле `slug` каждой категории должно быть уникальным.


##### Responses:

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 4. /categories/{slug}/

#### DELETE
##### Description:

Удалить категорию.
Права доступа: **Администратор.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| slug | path | Slug категории | Yes | string |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Категория не найдена |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 5. /genres/

#### GET
##### Description:

Получить список всех жанров.
Права доступа: **Доступно без токена**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| search | query | Поиск по названию жанра | No | string |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

#### POST
##### Description:

Добавить жанр.
Права доступа: **Администратор**.
Поле `slug` каждого жанра должно быть уникальным.


##### Responses:

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 6. /genres/{slug}/

#### DELETE
##### Description:

Удалить жанр.
Права доступа: **Администратор**.


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| slug | path | Slug жанра | Yes | string |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Жанр не найден |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 7. /titles/

#### GET
##### Description:

Получить список всех объектов.
Права доступа: **Доступно без токена**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| category | query | фильтрует по полю slug категории | No | string |
| genre | query | фильтрует по полю slug жанра | No | string |
| name | query | фильтрует по названию произведения | No | string |
| year | query | фильтрует по году | No | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

#### POST
##### Description:

Добавить новое произведение.
Права доступа: **Администратор**.
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).
При добавлении нового произведения требуется указать уже существующие категорию и жанр.


##### Parameters:

No parametrs

##### Responses:

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 8. /titles/{titles_id}/

#### GET
##### Description:

Информация о произведении
Права доступа: **Доступно без токена**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| titles_id | path | ID объекта | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Объект не найден |

#### PATCH
##### Description:

Обновить информацию о произведении
Права доступа: **Администратор**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| titles_id | path | ID объекта | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Объект не найден |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

#### DELETE
##### Description:

Удалить произведение.
Права доступа: **Администратор**.


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| titles_id | path | ID объекта | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Произведение не найдено |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 9. /titles/{title_id}/reviews/

#### GET
##### Description:

Получить список всех отзывов.
Права доступа: **Доступно без токена**.


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Произведение не найдено |

#### POST
##### Description:

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
Права доступа: **Аутентифицированные пользователи.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 404 | Произведение не найдено |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | user,moderator,admin |

### 10. /titles/{title_id}/reviews/{review_id}/

#### GET
##### Description:

Получить отзыв по id для указанного произведения.
Права доступа: **Доступно без токена.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Произведение или отзыв не найден |

#### PATCH
##### Description:

Частично обновить отзыв по id.
Права доступа: **Автор отзыва, модератор или администратор.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Произведение не найдено |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | user,moderator,admin |

#### DELETE
##### Description:

Удалить отзыв по id
Права доступа: **Автор отзыва, модератор или администратор.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Произведение или отзыв не найдены |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | user,moderator,admin |

### 11. /titles/{title_id}/reviews/{review_id}/comments/

#### GET
##### Description:

Получить список всех комментариев к отзыву по id
Права доступа: **Доступно без токена.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Не найдено произведение или отзыв |

#### POST
##### Description:

Добавить новый комментарий для отзыва.
Права доступа: **Аутентифицированные пользователи.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 404 | Не найдено произведение или отзыв |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | user,moderator,admin |

### 12. /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

#### GET
##### Description:

Получить комментарий для отзыва по id.
Права доступа: **Доступно без токена.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |
| comment_id | path | ID комментария | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Не найдено произведение, отзыв или комментарий |

#### PATCH
##### Description:

Частично обновить комментарий к отзыву по id.
Права доступа: **Автор комментария, модератор или администратор**.


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |
| comment_id | path | ID комментария | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Не найдено произведение, отзыв или комментарий |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | user,moderator,admin |

#### DELETE
##### Description:

Удалить комментарий к отзыву по id.
Права доступа: **Автор комментария, модератор или администратор**.


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |
| comment_id | path | ID комментария | Yes | integer |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Не найдено произведение, отзыв или комментарий |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | user,moderator,admin |

### 13. /users/

#### GET
##### Description:

Получить список всех пользователей.
Права доступа: **Администратор**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| search | query | Поиск по имени пользователя (username) | No | string |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt-token | read:admin |

#### POST
##### Description:

Добавить нового пользователя.
Права доступа: **Администратор**
Поля `email` и `username` должны быть уникальными.


##### Responses:

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 14. /users/{username}/

#### GET
##### Description:

Получить пользователя по username.
Права доступа: **Администратор**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| username | path | Username пользователя | Yes | string |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Пользователь не найден |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | read:admin |

#### PATCH
##### Description:

Изменить данные пользователя по username.
Права доступа: **Администратор.**
Поля `email` и `username` должны быть уникальными.


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| username | path | Username пользователя | Yes | string |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Пользователь не найден |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

#### DELETE
##### Description:

Удалить пользователя по username.
Права доступа: **Администратор.**


##### Parameters:

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| username | path | Username пользователя | Yes | string |

##### Responses:

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Пользователь не найден |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin |

### 15. /users/me/

#### GET
##### Description:

Получить данные своей учетной записи
Права доступа: **Любой авторизованный пользователь**


##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | read:admin,moderator,user |

#### PATCH
##### Description:

Изменить данные своей учетной записи
Права доступа: **Любой авторизованный пользователь**
Поля `email` и `username` должны быть уникальными.


##### Responses:

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |

##### Security:

| Security Schema | Scopes |
| --- | --- |
| jwt-token | admin,moderator,user |
