upstream fast-api {
    server fast-api-app:8000;
}

server {
    listen 80;
    server_name 194.67.68.231 flopp.ru;
    location / {
        proxy_pass http://fast-api;
    }
    location /static/ {
        alias /app/static/;
    }
}