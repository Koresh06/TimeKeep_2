#!/bin/bash
set -e

DOMAIN="24timekeep.ru"
EMAIL="korets2406@gmail.com"
NGINX_CONF="./nginx/nginx.conf"
NGINX_BACKUP="./nginx/nginx.conf.bak"

echo "==> Останавливаем все контейнеры..."
docker compose down

echo "==> Создаём временный HTTP-only конфиг..."
cp "$NGINX_CONF" "$NGINX_BACKUP"
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

echo "==> Запускаем nginx (только HTTP)..."
docker compose up -d nginx

echo "==> Ждём nginx..."
sleep 5

echo "==> Получаем сертификат Let's Encrypt..."
docker compose run --rm certbot certonly \
  --webroot \
  -w /var/www/certbot \
  --email "$EMAIL" \
  -d "$DOMAIN" \
  --agree-tos \
  --non-interactive

echo "==> Восстанавливаем HTTPS конфиг..."
mv "$NGINX_BACKUP" "$NGINX_CONF"

echo "==> Перезагружаем nginx с HTTPS конфигом..."
docker compose exec nginx nginx -s reload

echo "==> Запускаем все сервисы..."
docker compose up -d

echo ""
echo "Готово! Сайт: https://$DOMAIN"
