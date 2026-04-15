# Многостадийная сборка для минимального размера
FROM python:3.11-alpine AS builder

WORKDIR /build

# Копируем только необходимые файлы
COPY app.py .

# Финальный образ
FROM python:3.11-alpine

# Создаем непривилегированного пользователя
RUN addgroup -g 1000 -S appgroup && \
    adduser -u 1000 -S appuser -G appgroup

WORKDIR /app

# Копируем приложение из builder
COPY --from=builder --chown=appuser:appgroup /build/app.py .

# Делаем скрипт исполняемым
RUN chmod +x app.py

# Переключаемся на непривилегированного пользователя
USER appuser

# Документируем порт
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Запуск приложения
CMD ["python", "-u", "app.py"]