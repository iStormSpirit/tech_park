# Сервис расчёта стоимости изделия

Микросервис для расчёта стоимости изделий на основе материалов.

## Требования:

- FastAPI
- SQLAlchemy / asyncpg
- Docker-compose (Postgres + сервис)
- Pydantic-схемы

## Структура проекта

```
project_root/
├── main.py                     # Точка входа в приложение
├── .env                        # Переменные окружения
├── env.example                 # Пример конфигурации для команды
├── docker-compose.yml          # Конфигурация контейнера
│
├── src/                        # Исходный код приложения
│   ├── api/                    # Роутеры с deps и handlers
│   ├── services/               # Слой бизнес-логики
│   ├── db/                     # Слой данных
│   │   ├── models/             # Модели базы данных
│   │   ├── repositories/       # Взаимодейсвтие с базой данных
│   │   └── session.py          # Сессии подключения к БД
│   ├── schemas/                # Pydantic модели / DTO
│   └── core/                   # Конфигурация и общие утилиты
└── tests/                      # Тесты
```

## Запуск

### С помощью Docker Compose

```bash
docker-compose up --build
```

## Документация API

После запуска сервиса доступна автоматическая документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API

### POST /calc

Рассчитывает стоимость изделия на основе материалов.

**Запрос:**
```json
{
  "materials": [
    {"name": "steel", "qty": 120, "price_rub": 54.5},
    {"name": "copper", "qty": 12.3, "price_rub": 640.0}
  ]
}
```

**Ответ:**
```json
{
  "total_cost_rub": 87067.0
}
```

**Примеры вызова:**

```bash
# С помощью curl
curl -X POST "http://localhost:8000/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "materials": [
      {"name": "steel", "qty": 120, "price_rub": 54.5},
      {"name": "copper", "qty": 12.3, "price_rub": 640.0}
    ]
  }'

# С помощью httpie
http POST http://localhost:8000/calc \
  materials:='[{"name": "steel", "qty": 120, "price_rub": 54.5}, {"name": "copper", "qty": 12.3, "price_rub": 640.0}]'
```

### SQL запрос для получения 10 последних расчётов


```sql
SELECT 
    id,
    total_cost_rub,
    created_at
FROM calc_results
ORDER BY created_at DESC
LIMIT 10;
```


### Локальный запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите PostgreSQL (или используйте Docker):
```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=techpark -p 5432:5432 postgres:15-alpine
```

3. Установите переменную окружения (опционально):
```bash
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/techpark
```

4. Запустите сервис:
```bash
uvicorn main:app
```
