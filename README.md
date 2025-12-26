# DRFLessons

Backend-сервис для управления курсами и уроками

---

## 🚀 Запуск проекта

1. Клонировать репозиторий:
    ```bash
    git clone https://github.com/KirillKovardakov/Habbits.git
    cd Habbits
    ```

2. Настроить `.env` (пример в `.env.example`):
    ```bash
    DJANGO_SECRET_KEY=your_secret
    TELEGRAM_BOT_TOKEN=123456:ABC-def...
    REDIS_URL=redis://127.0.0.1:6379
    ```
3. Создать и запустить контейнеры через терминал:
    ```
    docker-compose up -d --build
    ```

-d запускает контейнеры в фоне.

Все сервисы будут автоматически созданы и подключены друг к другу.

## Проверка работоспособности сервисов

### Docker

Введите команду ```docker-compose ps``` чтобы увидеть запущенные контейнера.
Или же ```docker-compose ps -a```, чтобы увидеть также не запущенные и их статус (Exited(0) - контейнер запустился и
сразу завершился, Exited(1) - не запустился из-за ошибок)

### Backend

Проверьте, что сервис доступен по адресу:

http://localhost:8000

### PostgreSQL

Подключение через клиент по данным из .env.

### Redis

Проверьте соединение через redis-cli или через backend.

### Celery

Стартует вместе с backend. Логи можно посмотреть командой:

```docker-compose logs -f celery```

### Celery Beat

Логирует задачи периодического выполнения. Логи можно смотреть через:

```docker-compose logs -f selery_beat```

Остановка и удаление контейнеров
docker-compose down

Используйте флаг -v, чтобы удалить тома с базой данных:

```docker-compose down -v```

## Deployment

1. Настроить сервер (Ubuntu 22.04)
2. Установить Docker и docker-compose
3. Добавить `.env`
4. Запустить:
   docker-compose up -d --build

## CI/CD

- При каждом push:
    - запускаются тесты
    - при успехе — деплой на сервер

# НАСТРОЙКА УДАЛЁННОГО СЕРВЕРА

Подготовка сервера (Ubuntu 22.04)

На сервере:

```sudo apt update && sudo apt upgrade -y```

### базовые пакеты

```
sudo apt install -y \
  git curl ufw \
  ca-certificates \
  gnupg lsb-release
  ```

## Безопасность (обязательно)

# firewall

```
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## SSH-доступ по ключам

На локальной машине:

```ssh-keygen -t ed25519```

На сервере:

```
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
```

## .env (шаблон в репозитории!)
В репозитории:

commit-ить нужно .env.example, не .env

DEBUG=0
SECRET_KEY=changeme
ALLOWED_HOSTS=your_server_ip

DBNAME=postgres
DBUSER=postgres
DBPASSWORD=postgres
DBHOST=db
DBPORT=5432

REDIS_HOST=redis
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=2525


На сервере создаёшь реальный .env.