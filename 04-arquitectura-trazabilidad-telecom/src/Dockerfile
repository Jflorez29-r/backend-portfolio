FROM php:8.4-apache

# Instalar cliente de PostgreSQL, librerías del sistema y dependencias de PHP
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libzip-dev \
    libpng-dev \
    libonig-dev \
    zip \
    unzip \
    git \
    && docker-php-ext-install pdo pdo_pgsql zip bcmath gd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Habilitar módulo mod_rewrite de Apache para enrutamiento de Laravel
RUN a2enmod rewrite

# Directorio de trabajo
WORKDIR /var/www/html

# Copiar el código fuente
COPY . .

# Ajustar el DocumentRoot de Apache para apuntar a /public de Laravel
ENV APACHE_DOCUMENT_ROOT /var/www/html/public
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Instalar dependencias de composer (usando --no-scripts para evitar fallos de artisan en la construcción)
RUN composer install --no-dev --optimize-autoloader --no-interaction --no-scripts

# Ajustar permisos para storage y cache de Laravel
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Copiar el script de entrada y darle permisos de ejecución
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir el punto de entrada
ENTRYPOINT ["docker-entrypoint.sh"]
