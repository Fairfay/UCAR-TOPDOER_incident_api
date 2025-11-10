# API-сервис для учёта инцидентов

Маленький API-сервис для учёта инцидентов. Операторы и системы присылают сообщения о проблемах в Telegram, и это позволяет не терять их в чатах.

## Что было реализовано по ТЗ

### Требования по технологиям
- [x] **Python** - используется Python 3.12+
- [x] **Веб-фреймворк** - Django 5.2+ с Django REST Framework
- [x] **База данных** - PostgreSQL (поддерживается SQLite для разработки)

### Дополнительные технологии и ваозможности
- [x] Подключено сканирование уязвимостей для безопасной разработки (safety)
- [x] Ошибки приведены к единому виду (drf-standardized-errors)
- [x] Подключены JWT (joser)
- [x] Настроено отслеживание дублирующих запросов(n+1, django-querycount)
- [x] Настроено логирование в файл
- [x] Настроено отслеживание важных ошибок в телеграм для немедленного реагирования (привязан к определенному telegram_id - настройка в .env.template)
- [x] Настроен индекс по статусу
- [x] Настроен Docker
- [x] Настроен Makefile
- [x] Настроен Gunicorn
- [x] Настроены CORS
- [x] Установлен Poetry
- [x] Настроен скрипт запуска
- [x] Настроена django Admin
- [x] Прокомментированы важные аспекты кода
- [x] Добавлен deploy template nginx
- [x] Пагинация результатов
- [x] Swagger/OpenAPI документация
- [x] Health check эндпоинты

### Функциональность

**Модель инцидента:**
- `id` - уникальный идентификатор (автоматически генерируется)
- `description` - текст/описание инцидента
- `status` - статус инцидента (open, in_progress, resolved, closed)
- `source` - источник инцидента (operator, monitoring, partner)
- `created_at` - время создания (автоматически)
- `updated_at` - время последнего обновления (автоматически)

**Реализованные эндпоинты:**
1. [x] **Создать инцидент** - `POST /api/v1/incidents/`
2. [x] **Получить список инцидентов (с фильтром по статусу)** - `GET /api/v1/incidents/?status={status}`
3. [x] **Обновить статус инцидента по id** - `PATCH /api/v1/incidents/{id}/`
   - Возвращает 404, если инцидент не найден

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone git@github.com:Fairfay/UCAR-TOPDOER_incident_api.git
```
2. Создайте и заполните .env по примеру .env.template

3. Запустите проект:
```bash
docker compose up --build
```
Для прода, заполните .env.prod и запустите:
```bash
docker compose -f docker-compose.prod.yml up --build
```
4. Создайте суперпользователя для доступа к API и админке
```bash
docker exec -it <container_name> bash
python manage.py createsuperuser
```
5. Пройдите по пути http://127.0.0.1:8000/api/v1/schema/swagger-ui/#/

6. Аутентификация, все эндпоинты API требуют аутентификации через JWT токен.

Получите JWT токен через эндпоинт:
```bash
curl -X POST http://127.0.0.1:8000/api/identity/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```
**Ответ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
Используйте access токен в заголовке Authorization:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```


### Документация API
Swagger документация доступна по адресу: http://127.0.0.1:8000/api/v1/schema/swagger-ui/
ReDoc документация доступна по адресу: http://127.0.0.1:8000/api/schema/redoc/

## API Эндпоинты(краткое описание)
### Базовый URL
```
http://127.0.0.1:8000/api/v1/
```

### 1. Создать инцидент

**POST** `/api/v1/incidents/`

**Тело запроса:**
```json
{
  "description": "Самокат номер 875643 не в сети",
  "status": "open",
  "source": "operator"
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "description": "Самокат номер 875643 не в сети",
  "status": "open",
  "source": "operator",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 2. Получить список инцидентов

**GET** `/api/v1/incidents/`

**Query параметры:**
- `status` - фильтр по статусу (open, in_progress, resolved, closed)

**Ответ (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "description": "Самокат не в сети",
      "status": "open",
      "source": "operator",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "description": "Точка не отвечает",
      "status": "in_progress",
      "source": "monitoring",
      "created_at": "2024-01-15T09:15:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### 3. Получить инцидент по ID

**GET** `/api/v1/incidents/{id}/`

**Ответ (200 OK):**
```json
{
  "id": 1,
  "description": "Самокат не в сети",
  "status": "open",
  "source": "operator",,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Если не найден (404 Not Found):**
```json
{
  "type": "client_error",
  "errors": [
    {
      "code": "404 not_found",
      "detail": "Not found.",
      "attr": null
    }
  ]
}
```

### 4. Обновить статус инцидента

**PATCH** `/api/v1/incidents/{id}/`

**Тело запроса:**
Можно обновить только статус (частичное обновление) или несколько полей одновременно:
```json
{
  "status": "in_progress",
  "description": "Обновлённое описание"
}
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "description": "Самокат не в сети",
  "status": "in_progress",
  "source": "operator",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Если не найден (404 Not Found):**
```json
{
  "type": "client_error",
  "errors": [
    {
      "code": "404 not_found",
      "detail": "Not found.",
      "attr": null
    }
  ]
}
```

## Статусы инцидентов

- `open` - Открыт
- `in_progress` - В работе
- `resolved` - Решён
- `closed` - Закрыт

## Источники инцидентов

- `operator` - Оператор
- `monitoring` - Мониторинг
- `partner` - Партнёр

## Админ-панель

Админ-панель Django доступна по адресу: http://127.0.0.1:8000/api/admin/

## Тестирование API

Вы можете использовать curl, Postman или Swagger(http://127.0.0.1:8000/api/v1/schema/swagger-ui/#/).

Получить telegram_id можно в 
```bash
@userinfobot
```
Получить токен бота можно в
```bash
@BotFather
```

Дополнительные команды можно посмотреть в Makefile