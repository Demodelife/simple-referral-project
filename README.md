# Простой реферальный API проект
Проект API с пользовательскими функциями авторизации.

## Основные внешние библиотеки
* django = "4.2.4"
* djangorestframework = "3.14.0"
* drf-spectacular = "0.26.4"
* django-debug-toolbar = "4.2.0"
* python-dotenv = "1.0.0"
* gunicorn = "21.2.0"

## Установка
1. Клонируйте все содержимое репозитория в свою рабочую директорию.
2. Установите все библиотеки (для установки poetry - `pip install poetry`):
    * `poetry install`
3. Создайте файл `.env` и заполните там переменные окружения из файла `.env.template`:
    * `DJANGO_LOGLEVEL=`
    * `DJANGO_SECRET_KEY=`
    * `DJANGO_DEBUG=`
    * `DJANGO_ALLOWED_HOSTS=`

Запуск локально:
1. Запустите миграции:
   * `python manage.py migrate`
   * `python manage.py runserver`
2. Перейдите по предложенному URL-адресу в консоли `127.0.0.1:8000`.

Запуск через docker-compose:
1. Выполните сборку образа:
    * `docker compose build app`
2. Запустите контейнеры:
    * `docker compose up app`

## Реализованные методы

1. `GET /api/users/login/` Метод возвращает список пользователей.
   ### Пример запроса 200 OK
    * `GET /api/users/login/`
   ### Ответ
    * Успешно прошедший запрос возвращает список всех пользователей(для удобства тестирования), статус `200 OK`:
   ```
    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "count": 0,
        "next": null,
        "previous": null,
            {
            "phone": "+11111111111",
            "invite_code": "DU00kb",
            "guests": []
            },
            {
            "phone": "+22222222222",
            "invite_code": "4qRi66",
            "guests": []
            }
    }
   ```
2. `POST /api/users/login/` Метод для входа в систему по номеру телефона (если уже зарегистрирован) или регистрации.
   ### Пример запроса 200 OK
    * `POST /api/users/login/`, `Phone Number = +33333333333`
    * -> `POST api/users/login/confirm/3/`
    * -> `POST /api/users/login/confirm/3/sending_code/`
    * -> `GET /api/users/3/`
   ### Ответ
    * Успешно прошедший запрос переадресует на страницу ввода кода(фиктивно) 
    * и на страницу профиля пользователя после подтверждения, статус `200 OK`:
   ```
    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "my_profile": {
            "phone": "+33333333333",
            "invite_code": "VwCZvK",
            "guests": []
        },
        "logout": "http://127.0.0.1:8000/api/users/logout/"
   ```
3. `GET /api/users/logout/` Метод для входа в систему по номеру телефона (если уже зарегистрирован) или регистрации.
   ### Пример запроса 200 OK
    * `GET /api/users/logout/`
   ### Ответ
    * Успешно прошедший запрос переадресует на страницу с сообщением о выходе из системы, статус `200 OK`:
   ```
    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "message": "You are logged out.",
        "login": "http://127.0.0.1:8000/api/users/login/"
    }
   ```
4. `GET /api/users/1/` Метод для деталей профиля.
   ### Пример запроса 200 OK
    * `GET /api/users/1/`
   ### Ответ
    * Успешно прошедший запрос выводит детали пользователя(как и после входа в систему), статус `200 OK`:
   ```
    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "my_profile": {
            "phone": "+11111111111",
            "invite_code": "DU00kb",
            "guests": []
        },
        "logout": "http://127.0.0.1:8000/api/users/logout/"
    }
   ```
5. `POST /api/users/1/` Метод поиска по `invite_code` другого пользователя.
   ### Пример запроса 200 OK
    * `POST /api/users/1/`, `Invite Code = 4qRi66`
   ### Ответ
    * Успешно прошедший запрос выводит детали текущего и найденного пользователей, статус `200 OK`:
   ```
    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "my_profile": {
            "phone": "+11111111111",
            "invite_code": "DU00kb",
            "guests": []
        },
        "found_profile": {
            "phone": "+22222222222",
            "invite_code": "4qRi66",
            "guests": [
                "+11111111111"
            ]
        },
        "logout": "http://127.0.0.1:8000/api/users/logout/"
    }
   ```
   
## Дополнительная информация
* У пользователей, чью страницу посетили по инвайт-коду, 
появляется информация посещения(номера телефонов гостей страницы).
* В теле некоторых запросов есть ссылки для входа и выхода из системы:
  * `"login": "http://127.0.0.1:8000/api/users/login/" `
  * `"logout": "http://127.0.0.1:8000/api/users/logout/"`
* Redoc-документация API:
  * `http://127.0.0.1:8000/api/schema/redoc/`

## Работа с административной панелью Django
1. Создать суперпользователя:
   * `python manage.py createsuperuser`
2. Зайти в административную панель http://127.0.0.1:8000/admin/ зарегистрированным суперпользователем.

# Simple Referral Project API
API project with custom authorization functions.

## Main External Libraries
* django = "4.2.4"
* djangorestframework = "3.14.0"
* drf-spectacular = "0.26.4"
* django-debug-toolbar = "4.2.0"
* python-dotenv = "1.0.0"
* gunicorn = "21.2.0"

## Installation
1. Clone all the contents of the repository to your working directory.
2. Install all libraries (to install poetry - `pip install poetry`):
     * `poetry install`
3. Create a `.env` file and fill in the environment variables there from the `.env.template` file:
     * `DJANGO_LOGLEVEL=`
     * `DJANGO_SECRET_KEY=`
     * `DJANGO_DEBUG=`
     * `DJANGO_ALLOWED_HOSTS=`

Run locally:
1. Run the migrations:
    * `python manage.py migrate`
    * `python manage.py runserver`
2. Navigate to the suggested URL in the console `127.0.0.1:8000`.

Running via docker-compose:
1. Build the image:
     * `docker compose build app`
2. Run containers:
     * `docker compose up app`

## Implemented Methods

1. `GET /api/users/login/` The method returns a list of users.
    ### Request example 200 OK
     * `GET /api/users/login/`
    ### Answer
     * A successful request returns a list of all users (for testing convenience), status `200 OK`:
    ```
     HTTP 200 OK
     Allow: GET, POST, HEAD, OPTIONS
     Content-Type: application/json
     Vary:Accept
    
     {
         count: 0
         "next": null
         "previous": null
             {
             "phone": "+11111111111",
             "invite_code": "DU00kb",
             "guests": []
             },
             {
             "phone": "+22222222222",
             "invite_code": "4qRi66",
             "guests": []
             }
     }
    ```
2. `POST /api/users/login/` Method for logging in by phone number (if already registered) or registration.
    ### Request example 200 OK
     * `POST /api/users/login/`, `Phone Number = +33333333333`
     * -> `POST api/users/login/confirm/3/`
     * -> `POST /api/users/login/confirm/3/sending_code/`
     * -> `GET /api/users/3/`
    ### Answer
     * A successful request redirects to the code entry page (fictitious)
     * and to the user profile page after confirmation, status `200 OK`:
    ```
     HTTP 200 OK
     Allow: GET, POST, HEAD, OPTIONS
     Content-Type: application/json
     Vary:Accept
    
     {
         "my_profile": {
             "phone": "+33333333333",
             "invite_code": "VwCZvK",
             "guests": []
         },
         "logout": "http://127.0.0.1:8000/api/users/logout/"
    ```
3. `GET /api/users/logout/` Method for logging in by phone number (if already registered) or registration.
    ### Request example 200 OK
     * `GET /api/users/logout/`
    ### Answer
     * A successful request redirects to a page with a logout message, status `200 OK`:
    ```
     HTTP 200 OK
     Allow: GET, HEAD, OPTIONS
     Content-Type: application/json
     Vary:Accept
    
     {
         "message": "You are logged out.",
         "login": "http://127.0.0.1:8000/api/users/login/"
     }
    ```
4. `GET /api/users/1/` Method for profile details.
    ### Request example 200 OK
     * `GET /api/users/1/`
    ### Answer
     * A successful request displays the user's details (same as after login), status `200 OK`:
    ```
     HTTP 200 OK
     Allow: GET, POST, HEAD, OPTIONS
     Content-Type: application/json
     Vary:Accept
    
     {
         "my_profile": {
             "phone": "+11111111111",
             "invite_code": "DU00kb",
             "guests": []
         },
         "logout": "http://127.0.0.1:8000/api/users/logout/"
     }
    ```
5. `POST /api/users/1/` Method for searching by `invite_code` of another user.
    ### Request example 200 OK
     * `POST /api/users/1/`, `Invite Code = 4qRi66`
    ### Answer
     * A successful request displays the details of the current and found users, the status is `200 OK`:
    ```
     HTTP 200 OK
     Allow: GET, POST, HEAD, OPTIONS
     Content-Type: application/json
     Vary:Accept
    
     {
         "my_profile": {
             "phone": "+11111111111",
             "invite_code": "DU00kb",
             "guests": []
         },
         "found_profile": {
             "phone": "+22222222222",
             "invite_code": "4qRi66",
             "guests": [
                 "+11111111111"
             ]
         },
         "logout": "http://127.0.0.1:8000/api/users/logout/"
     }
    ```
   
## Additional Information
* For users whose page was visited by an invite code,
visit information appears (phone numbers of page guests).
* In the body of some requests there are links to enter and exit the system:
   * `"login": "http://127.0.0.1:8000/api/users/login/" `
   * `"logout": "http://127.0.0.1:8000/api/users/logout/"`
* API redoc documentation:
   * `http://127.0.0.1:8000/api/schema/redoc/`

## Working with the Django admin panel
1. Create a superuser:
    * `python manage.py createsuperuser`
2. Log in to the administrative panel http://127.0.0.1:8000/admin/ as a registered superuser.