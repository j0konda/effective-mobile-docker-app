# Effective Mobile App

[![Docker](https://img.shields.io/badge/Docker-20.10+-blue)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://python.org)
[![Nginx](https://img.shields.io/badge/Nginx-1.25-green)](https://nginx.com)

Производственное веб-приложение с reverse proxy на nginx и бэкендом на Python. Демонстрирует best practices контейнеризации: безопасность, healthcheck'и, лимиты ресурсов и оптимизацию.

## 📋 Содержание

- [Архитектура](#архитектура)
- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
- [Проверка работы](#проверка-работы)
- [Управление приложением](#управление-приложением)
- [Структура проекта](#структура-проекта)
- [Безопасность](#безопасность)
- [Устранение проблем](#устранение-проблем)
- [Технологии](#технологии)

## 🏗 Архитектура
### Схема взаимодействия
┌─────────────┐ ┌──────────────┐ ┌─────────────────┐
│ Пользователь │ ──> │ nginx │ ──> │ Python Backend 
│ localhost:80 │ │ Reverse │ │ HTTP Server │
│ │ │ Proxy │ │ :8080 │
└─────────────┘ └──────────────┘ └─────────────────┘
↓ ↓ ↓
Браузер Принимает Возвращает
или curl запросы на "Hello from
порту 80 Effective Mobile!"


### Как это работает

1. **Пользователь** отправляет HTTP-запрос на `http://localhost` (порт 80)
2. **nginx** (контейнер `effective-mobile-nginx`) принимает запрос
3. **nginx** проксирует запрос на бэкенд-сервис через внутреннюю Docker-сеть
4. **Backend** (контейнер `effective-mobile-backend`) обрабатывает запрос
5. **Backend** возвращает ответ: `"Hello from Effective Mobile!"`
6. **nginx** передает ответ обратно пользователю

### Ключевые особенности

- ✅ Бэкенд **НЕ доступен** с хостовой машины (только внутри Docker-сети)
- ✅ nginx выступает как **единая точка входа**
- ✅ Оба сервиса изолированы в собственной Docker-сети
- ✅ Легковесные образы на основе Alpine Linux

## 📦 Требования

- **Docker Engine** 20.10 или выше
- **Docker Compose** 2.0 или выше (или плагин `docker compose`)

### Проверка установки

```
docker --version
```
```
docker compose version
```
🚀 Быстрый старт
1. Клонирование репозитория
```
git clone <repository-url>
cd effective-mobile-docker-app
```
2. Запуск приложения
```
docker compose up -d
```
3. Проверка статуса контейнеров
```
docker compose ps
```
Ожидаемый вывод:
NAME                       IMAGE                              STATUS
effective-mobile-backend   effective-mobile-docker-app-backend   Up (health: starting)
effective-mobile-nginx     effective-mobile-docker-app-nginx     Up

✅ Проверка работы
1. Проверка через curl
```
curl http://localhost
```
Ожидаемый ответ:

Hello from Effective Mobile!

2. Проверка в браузере
Откройте браузер и перейдите по адресу:

http://localhost

Вы должны увидеть текст:

Hello from Effective Mobile!

3. Проверка healthcheck бэкенда
```
curl http://localhost/health
```
Ожидаемый ответ:

{"status":"healthy","timestamp":"2026-04-15T09:55:00.645734"}

4. Проверка изоляции (бэкенд недоступен с хоста)
```
curl http://localhost:8080
```
Ожидаемый результат: 
curl: (7) Failed to connect to localhost port 8080 after 0 ms: Couldn't connect to server

5. Проверка связи внутри Docker-сети
```
docker exec effective-mobile-nginx wget -qO- http://backend:8080
```
Ожидаемый ответ:
Hello from Effective Mobile!

🛠 Управление приложением
Основные команды
Действие	               Команда
Запуск	                   docker compose up -d
Остановка	               docker compose down
Перезапуск	               docker compose restart
Просмотр статуса	       docker compose ps
Просмотр логов	           docker compose logs -f
Пересборка и запуск	       docker compose up -d --build

Работа с логами
# Все логи
```
docker compose logs -f
```
# Только бэкенд
```
docker compose logs -f backend
```
# Только nginx
```
docker compose logs -f nginx
```
# Последние 50 строк
```
docker compose logs --tail 50
```
Остановка и очистка
```
docker compose down
```
# Полная очистка (контейнеры, образы, сеть)
```
docker compose down --rmi all --volumes
```

Мониторинг ресурсов
```
docker stats effective-mobile-backend effective-mobile-nginx
```
📁 Структура проекта

effective-mobile-docker-app/
├── backend/
│   ├── Dockerfile          # Docker-образ для Python сервера
│   └── app.py              # HTTP-сервер на Python
├── nginx/
│   ├── Dockerfile          # Docker-образ для nginx
│   └── nginx.conf          # Конфигурация reverse proxy
├── docker-compose.yml      # Оркестрация контейнеров
└── README.md               # Документация

Описание файлов
backend/app.py
Python HTTP-сервер на встроенном модуле http.server. Слушает порт 8080 и отвечает на запросы:

- GET / → "Hello from Effective Mobile!"

- GET /health → JSON со статусом и временем

backend/Dockerfile
- Базовый образ: python:3.11-alpine

- Создание непривилегированного пользователя

- Healthcheck для мониторинга

- Запуск от non-root пользователя

nginx/nginx.conf
- Upstream backend для балансировки

- Proxy_pass с передачей заголовков

- -заголовки (X-Frame-Options, X-Content-Type-Options)

- Gzip сжатие

- Отключен server_tokens

docker-compose.yml
- Два сервиса: backend и nginx

- Общая сеть app-network

- Проброшен только порт 80 nginx

- Лимиты ресурсов CPU/RAM

- Автоматический перезапуск

🔒 Безопасность
Реализованные меры
Мера	                        Описание
Non-root пользователи	        Бэкенд запускается от appuser, nginx от nginx
Сетевая изоляция	            Бэкенд не публикует порты наружу
Лимиты ресурсов	                Ограничения CPU и RAM для каждого контейнера
Security-заголовки	            X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
Healthcheck'и	                Мониторинг состояния сервисов
Отключен server_tokens	        nginx не раскрывает версию
Graceful shutdown	            Обработка сигналов SIGTERM/SIGINT

Проверка безопасности

# Проверка пользователя в бэкенде
docker exec effective-mobile-backend whoami
# Вывод: appuser

# Проверка пользователя в nginx
docker exec effective-mobile-nginx whoami
# Вывод: nginx

# Проверка открытых портов бэкенда
docker port effective-mobile-backend
# Вывод: (пусто) - порты не опубликованы

Диагностика

# Проверка логов бэкенда
```
docker logs effective-mobile-backend
```
# Проверка логов nginx
```
docker logs effective-mobile-nginx
```
# Проверка сети
```
docker network ls
```
```
docker network inspect effective-mobile-docker-app_app-network
```
# Проверка healthcheck
```
docker inspect effective-mobile-backend | grep -A 10 "Health"
```
Сброс и перезапуск
# Полный сброс
```
docker compose down -v
docker system prune -f
```
# Чистый запуск
```
docker compose up -d --build
```

🛠 Технологии

Python 3.11-alpine - легковесный образ Python

Nginx 1.25-alpine - официальный образ nginx на Alpine

Docker Compose v3.8 - оркестрация контейнеров

Alpine Linux - минимальный дистрибутив Linux

📊 Производительность
Оптимизации

✅ Alpine Linux как базовый образ (минимальный размер)

✅ Многостадийная сборка Python образа

✅ Gzip сжатие в nginx

✅ Keepalive соединения

✅ Лимиты ресурсов для предотвращения DoS

✅ Буферизация в nginx
