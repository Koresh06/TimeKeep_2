#!/bin/bash
set -e

DOMAIN="24timekeep.ru"
EMAIL="korets2406@gmail.com"

echo "==> Устанавливаем certbot на хост..."
apt-get install -y -qq certbot

echo "==> Останавливаем все контейнеры..."
docker compose down || true

echo "==> Создаём папку для ACME challenge..."
mkdir -p ./certbot/www

echo "==> Запускаем временный nginx для ACME challenge..."
docker run --rm -d \
    --name nginx_temp \
    -p 80:80 \
    -v "$(pwd)/certbot/www:/usr/share/nginx/html" \
    nginx:alpine

sleep 3

echo "==> Получаем сертификат Let's Encrypt..."
certbot certonly --webroot \
    --webroot-path="$(pwd)/certbot/www" \
    -d "$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive

docker stop nginx_temp || true

echo "==> Запускаем все сервисы..."
docker compose up -d

echo ""
echo "Готово! Сайт: https://$DOMAIN"
