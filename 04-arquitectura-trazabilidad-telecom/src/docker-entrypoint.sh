#!/bin/sh

echo "Ejecutando migraciones de base de datos..."
php artisan migrate --force

echo "Generando enlace simbólico del storage..."
php artisan storage:link --force

echo "Optimizando configuración y enrutamiento de Laravel para producción..."
php artisan config:cache
php artisan route:cache
php artisan view:cache

echo "Iniciando servidor Apache en primer plano..."
exec apache2-foreground
