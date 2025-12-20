FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Системные зависимости + SSL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry через pip (САМЫЙ НАДЁЖНЫЙ СПОСОБ)
RUN pip install --upgrade pip && pip install poetry

# Отключаем виртуальные окружения poetry
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi --no-root


# Копируем проект
COPY . .
