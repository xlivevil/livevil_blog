FROM nginx:1.18.0

RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/livevil_blog.conf /etc/nginx/conf.d/livevil_blog.conf
