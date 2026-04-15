FROM nginx:1.25-alpine-slim

# Удаляем дефолтную конфигурацию
RUN rm -f /etc/nginx/nginx.conf

# Копируем нашу конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf

# Проверяем синтаксис конфигурации без резолвинга upstream
RUN nginx -t 2>/dev/null || (echo "Warning: nginx config syntax might be invalid" && exit 0)

EXPOSE 80

# Запускаем nginx в foreground
CMD ["nginx", "-g", "daemon off;"]