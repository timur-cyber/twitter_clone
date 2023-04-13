# API на Python, Flask для аналога Twitter

## Инструкция по установке

### Предварительная подготовка
1. Установить на ПК интерпретатор языка Python (версии 3.9 или новее).
2. Желательно поставить виртаульное окружение в директории проекта:
   * `python3 -m venv prod`
3. Следом, надо активировать окружение:
   * Windows `.\prod\Scripts\activate`
   * Linux/MacOS `source prod/bin/activate`
4. Установить необходимые библиотеки с помощью команды:
   * `python -m pip install -r requirements.txt`

### Настройка Базы Данных PostgreSQL

Для настройки базы данных необходимо указать название БД, имя пользователя, пароль, хост и порт в директории **.envs/** файлом **.postgres** (Пример **.postgres.example**)
```
POSTGRES_DB=db
POSTGRES_NAME=name
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=host
POSTGRES_PORT=port
```

### Миграции

Миграции БД осуществляются утилитой Alembic. По умолчанию, все миграции настроены и для запуска ничего отдельно запускать не требуется. Однако, если вы произвели изменения в Базе Данных вам придётся создать и применить миграции в ручную. 

Документация Alembic: https://alembic.sqlalchemy.org/en/latest/ 

### Настройка WSGI

Для настройки WSGI надо указать параметры своего Flask приложения в директории **.envs/** файлом **.wsgi** (Пример **.wsgi.example**)
```
FLASK_APP=APP/__init__.py
FLASK_DEBUG=1
DATABASE_URL=URL
SQL_HOST=HOST
SQL_PORT=PORT
DATABASE=DATABASE
APP_FOLDER=FOLDER
```

### Docker

Для запуска приложения рекомендуется использовать Docker. 

Подробнее: https://docs.docker.com/

Чтобы запустить проект, в терминале нужно ввести команду:
```commandline
docker-compose up
```
Чтобы запустить проект в фоновом режиме, в терминале введите команду:
```commandline
docker-compose up -d
```

## Документация
После установки и запуска проекта вся документация доступна по адресу **/apidocs/** сервера.

Всего имеется 10 функциональных запросов сервиса:
- **POST** /api/tweets - Добавить твит
- **POST** /api/medias - Добавить медиафайл
- **DELETE** /api/tweets/<id> - Удалить твит
- **POST** /api/tweets/<id>/likes - Поставить лайк
- **DELETE** /api/tweets/<id>/likes - Удалить лайк
- **POST** /api/users/<id>/follow - Подписаться на пользователя
- **DELETE** /api/users/<id>/follow - Отписаться от пользователя
- **GET** /api/tweets - Получить ленту твитов
- **GET** /api/users/me - Получить информацию о своем профиле
- **GET** /api/users/<id> - Получить информацию о чужом профиле

## Тесты
Все тесты написаны на библиотеке **pytest** (Подробнее: https://docs.pytest.org/en/7.2.x/contents.html)

### Перед началом
Перед тем как начать тестирование нужно выполнить следующие требования:
1. Создать виртаульное окружение под разработку в директории **src/**:
   * `cd src`
   * `python3 -m venv dev`
2. Следом, надо активировать окружение:
   * Windows `.\dev\Scripts\activate`
   * Linux/MacOS `source dev/bin/activate`
3. Затем надо установить библиотеки разработчика:
   * `python -m pip install -r requirements_dev.txt`
4. После этого необходимо создать локальную базу данных PostgreSQL и провести миграции через Alembic.

### Тестирование
Для тестирования приложения надо по терминалу перейти в директорию **src/**:

```
cd src
```

Затем командой запустить тесты командой:

```
pytest tests
```
Для более подробного запуска используйте команду:
```
pytest tests -vv
```
## Мониторинг приложения
Мониторинг приложения осуществляется с помощью **Prometheus** + **Grafana** 

Чтобы просмотреть визуализированную панель, необходимо настроить Grafana:
1. Пройти по адресу http://localhost:3000 и зарегистрироваться в приложении (По умолчанию **login:** admin | **password:** admin).
2. Настроить источник данных (**Prometheus**) указав адрес http://prometheus:9090
3. Импортировать конфигурацию панели Grafana **./grafana/dashboards/dashboard.json**

Подробнее: https://prometheus.io/docs/visualization/grafana/