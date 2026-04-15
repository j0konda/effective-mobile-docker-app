FROM nginx:1.25-alpine

# Удаляем дефолтную конфигурацию
RUN rm /etc/nginx/nginx.conf

# Копируем нашу конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf

# Создаем пользователя nginx (если его нет)
RUN adduser -D -u 101 -g 'nginx' nginx 2>/dev/null || true

# Меняем владельца конфигурационных файлов
RUN chown -R nginx:nginx /etc/nginx/ && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Переключаемся на пользователя nginx
USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]