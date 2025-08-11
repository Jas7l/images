# Сервис обработки изображений

## Установка

### docker-compose.yml

```yaml
services:
  db:
    image: postgres:15
    container_name: my_container
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - ./pgdata:/var/lib/postgresql/data
    networks:
      - backend-network

  files:
    image: files:1.0.1
    ports:
      - "8020:8000"
    volumes:
      - ./storage:/app/storage
      - ./config.yaml:/config.yaml
    networks:
      - backend-network
    restart: always

  syncer:
    image: files:1.0.1
    command: python -m scripts.files_sync
    volumes:
      - ./storage:/app/storage
      - ./config.yaml:/config.yaml
    networks:
      - backend-network
    restart: always

  images:
    image: images:1.0.1
    ports:
      - "8030:8000"
    volumes:
      - ./tmp:/app/tmp
      - ./config.yaml:/config.yaml
    networks:
      - backend-network
    restart: always

  rabbit:
    image: rabbitmq:3-management
    hostname: rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: user
      RABBITMQ_DEFAULT_PASS: password
    networks:
      - backend-network

  task-worker:
    image: images:1.0.1
    restart: always
    command: python -m scripts.tasks_worker
    volumes:
      - ./tmp:/app/tmp
      - ./config.yaml:/config.yaml
    networks:
      - backend-network

networks:
  backend-network:
    driver: bridge
```

### config.yaml
```yaml
rabbit:
  host: rabbit
  port: 5672
  user: user
  password: password
  routing_key: image
  queue_name: image

tmp_dir: /app/tmp

logging:
  root_log_level: 0
  logstash:
    host: elk
    port: 5046
    app_extra:
      service: image-api
  modules:
    - name: urllib3.connectionpool
      log_level: 30
    - name: pika
      log_level: 30

pg:
  host: db
  port: 5432
  user: postgres
  password: postgres
  database: my_db
```

### .env
```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=my_db
```

### Запуск
```bash
make build
make run
```

## API

### Создание задачи обработки изображения

`POST /api/images`

**Запрос** `application/json`

```json5
{
    // id исходного файла в базе данных 
    "input_file_id": 1,
    // Название алгоритма
    "algorithm": "projection",
    // Параметры алгоритма
    "algorithm_params": {
        // Имя файла в хранилище после обработки
        "new_name": "reprojected_image.tif",
        // Относительный путь нового файла в хранилище
        "save_path": "/processed",
        // Целевая система координат
        "dstSRS": "EPSG:3857",
        // Новое разрешение
        "yRes": 10.0,
        "xRes": 10.0        
    },
    "input_file_path": "/app/storage/input_image.tif"
}
```
Где:
* `algorithm` - обязательно resolution/projection

* `dstSRS` - обязателен для алгоритма projection.

* `yRes` и `xRes` - обязательны для алгоритма resolution   


**Ответ** `application/json` `200 OK`

```json5
{
    "algorithm": "projection",
    "algorithm_params": {
        "dstSRS": "EPSG:4326",
        "new_name": "projection4326be1.tif",
        "save_path": ""
    },
    "created_date": "2025-08-11T08:22:38.121707",
    "input_file_id": 1,
    "output_file_id": null,
    "process_status": "new",
    "process_time": 0,
    "task_id": 251,
    "updated_date": "2025-08-11T08:22:38.121724"
}
```
**Ошибки:**
`400` — ошибки в параметрах запроса
`500` — ошибка при обработке изображения

### Получение списка всех задач

`GET /api/images`

*Ответ* `application/json` `200 OK`

```json5
[
    {
        "algorithm": "projection",
        "algorithm_params": {
            "dstSRS": "EPSG:4326",
            "new_name": "projection4326be1.tif",
            "save_path": ""
        },
        "created_date": "2025-08-11T08:22:38.121707",
        "input_file_id": 1,
        "output_file_id": 6,
        "process_status": "done",
        "process_time": 6,
        "task_id": 251,
        "updated_date": "2025-08-11T08:22:43.834541"
    }
]
```

### Получение информации о задаче

`GET /api/images/<int:task_id>`

Где:

* `task_id` — ID задачи в базе данных.

**Ответ** `application/json` `200 OK`

```json5
{
        "algorithm": "projection",
        "algorithm_params": {
            "dstSRS": "EPSG:4326",
            "new_name": "projection4326be1.tif",
            "save_path": ""
        },
        "created_date": "2025-08-11T08:22:38.121707",
        "input_file_id": 1,
        "output_file_id": 6,
        "process_status": "done",
        "process_time": 6,
        "task_id": 251,
        "updated_date": "2025-08-11T08:22:43.834541"
}
```
**Ошибки:**
`404` — задача не найдена
`500` — ошибка сервера