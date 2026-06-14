#!/bin/bash
set -e

DOMAIN="24timekeep.ru"
EMAIL="korets2406@gmail.com"
NGINX_CONF="./nginx/nginx.conf"

echo "==> Устанавливаем certbot..."
apt-get install -y -qq certbot

echo "==> Останавливаем все контейнеры..."
docker compose down || true

echo "==> Создаём папку для ACME challenge..."
mkdir -p ./certbot/www

echo "==> Пишем временный HTTP-only конфиг nginx..."
cp "$NGINX_CONF" "${NGINX_CONF}.bak"
cat > "$NGINX_CONF" << 'EOF'
server {
    listen 80;
    server_name 24timekeep.ru;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
EOF

echo "==> Запускаем nginx через Docker (открывает порт 80)..."
docker compose up -d nginx
sleep 5

echo "==> Проверяем что nginx отвечает..."
curl -sf http://"$DOMAIN"/ > /dev/null && echo "nginx OK" || echo "WARN: nginx не ответил, продолжаем"

echo "==> Получаем сертификат (webroot через Docker nginx)..."
certbot certonly --webroot \
    --webroot-path="$(pwd)/certbot/www" \
    -d "$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive

echo "==> Восстанавливаем HTTPS конфиг..."
mv "${NGINX_CONF}.bak" "$NGINX_CONF"

echo "==> Запускаем все сервисы..."
docker compose up -d
sleep 3

echo "==> Перезагружаем nginx с HTTPS конфигом..."
docker compose exec nginx nginx -s reload

echo ""
echo "Готово! Сайт: https://$DOMAIN"
