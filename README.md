# Проект микросервисов на базе FastAPI

## Обзор
Данный проект включает разработку двух микросервисов с использованием FastAPI:
1. **TODO-сервис**: Сервис для управления задачами, поддерживающий операции CRUD.
2. **Сервис сокращения URL**: Сервис для создания сокращенных ссылок, редиректа на исходные URL и получения статистики по ссылкам.

Оба сервиса контейнеризированы с использованием Docker и используют SQLite для хранения данных.

---

## Особенности

### TODO-сервис
- **Эндпоинты:**
  - `POST /items`: Создание новой задачи.
  - `GET /items`: Получение списка всех задач.
  - `GET /items/{item_id}`: Получение задачи по её идентификатору.
  - `PUT /items/{item_id}`: Обновление задачи по идентификатору.
  - `DELETE /items/{item_id}`: Удаление задачи по идентификатору.
- Данные сохраняются в SQLite с использованием именованных томов Docker.

### Сервис сокращения URL
- **Эндпоинты:**
  - `POST /shorten`: Создание сокращенного URL на основе полного URL.
  - `GET /{short_id}`: Редирект на исходный URL по сокращенному идентификатору.
  - `GET /stats/{short_id}`: Получение статистики по сокращенному URL.
- Данные также сохраняются в SQLite.

---

## Локальная установка и запуск

### Предварительные требования
- Python версии 3.9 и выше
- SQLite
- Docker (опционально, для контейнеризации)

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <repository_url>
   cd fastapi-project
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сервисы:
   - **TODO-сервис:**
     ```bash
     uvicorn todo_app.main:app --reload --port 8000
     ```
   - **Сервис сокращения URL:**
     ```bash
     uvicorn shorturl_app.main:app --reload --port 8001
     ```

4. Доступ к API-документации:
   - TODO-сервис: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Сервис сокращения URL: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## Запуск с использованием Docker

### Сборка Docker-образов
1. Соберите образ Docker для TODO-сервиса:
   ```bash
   docker build -t todo-service ./todo_app
   ```

2. Соберите образ Docker для сервиса сокращения URL:
   ```bash
   docker build -t shorturl-service ./shorturl_app
   ```

### Запуск контейнеров Docker
1. Запустите TODO-сервис:
   ```bash
   docker run -d -p 8000:80 -v todo_data:/app/data todo-service
   ```

2. Запустите сервис сокращения URL:
   ```bash
   docker run -d -p 8001:80 -v shorturl_data:/app/data shorturl-service
   ```

---

## Тестирование сервисов

### Использование Swagger UI
- TODO-сервис: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Сервис сокращения URL: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

### Использование curl
- **TODO-сервис:**
  - Создание задачи:
    ```bash
    curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d '{"title": "Пример задачи", "description": "Описание", "completed": false}'
    ```
  - Получение всех задач:
    ```bash
    curl -X GET "http://127.0.0.1:8000/items"
    ```
- **Сервис сокращения URL:**
  - Создание сокращенного URL:
    ```bash
    curl -X POST "http://127.0.0.1:8001/shorten" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
    ```
  - Получение статистики:
    ```bash
    curl -X GET "http://127.0.0.1:8001/stats/<short_id>"
    ```

---

## Развертывание в Docker Hub

1. Войдите в Docker Hub:
   ```bash
   docker login
   ```

2. Отметьте образы Docker тегами:
   - TODO-сервис:
     ```bash
     docker tag todo-service:latest <docker_hub_username>/todo-service:latest
     ```
   - Сервис сокращения URL:
     ```bash
     docker tag shorturl-service:latest <docker_hub_username>/shorturl-service:latest
     ```

3. Опубликуйте образы в Docker Hub:
   - TODO-сервис:
     ```bash
     docker push <docker_hub_username>/todo-service:latest
     ```
   - Сервис сокращения URL:
     ```bash
     docker push <docker_hub_username>/shorturl-service:latest
     ```

---

## Ссылки на Docker Hub
- TODO-сервис: [Docker Hub Link](https://hub.docker.com/r/<docker_hub_username>/todo-service)
- Сервис сокращения URL: [Docker Hub Link](https://hub.docker.com/r/<docker_hub_username>/shorturl-service)

---

## Лицензия
Данный проект распространяется под лицензией MIT.

