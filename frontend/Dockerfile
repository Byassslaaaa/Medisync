# Stage 1: Build React app
FROM node:20-alpine AS builder

WORKDIR /app

# Terima build arg dari docker-compose (VITE_ vars harus di-bake saat build)
ARG VITE_SERVICE_A_URL=http://localhost:4001
ENV VITE_SERVICE_A_URL=$VITE_SERVICE_A_URL

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve dengan Nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Konfigurasi Nginx untuk React Router (SPA)
RUN echo 'server { \
  listen 80; \
  location / { \
    root /usr/share/nginx/html; \
    try_files $uri $uri/ /index.html; \
  } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
