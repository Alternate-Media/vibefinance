# Dockerfile for Vue Frontend (Hardened Ubuntu)

# Stage 1: Build
FROM node:20-slim as builder

WORKDIR /app

COPY package.json .
# COPY package-lock.json . # Uncomment when lock file exists

RUN npm install

COPY . .

RUN npm run build

# Stage 2: Serve
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# Copy build artifacts
COPY --from=builder /app/dist /var/www/html

# Remove default nginx config and ensure correct permissions
RUN rm -f /etc/nginx/sites-enabled/default

# Create a simple nginx config for SPA
RUN echo 'server { \
    listen 80; \
    root /var/www/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/sites-available/vibe \
    && ln -s /etc/nginx/sites-available/vibe /etc/nginx/sites-enabled/

# Create a non-root user for Nginx (optional, but standard Nginx usually runs workers as www-data)
# We stick to standard nginx user (www-data) which exists in Ubuntu

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
