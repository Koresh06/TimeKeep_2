#!/bin/bash
set -e

DOMAIN="24timekeep.ru"
EMAIL="korets2406@gmail.com"

echo "==> Устанавливаем certbot..."
apt-get install -y -qq certbot

echo "==> Останавливаем все контейнеры (освобождаем порт 80)..."
docker compose down || true

echo "==> Получаем сертификат (standalone — certbot сам держит порт 80)..."
certbot certonly --standalone \
    -d "$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive

echo "==> Запускаем все сервисы..."
mkdir -p ./certbot/www
docker compose up -d

echo ""
echo "Готово! Сайт: https://$DOMAIN"
