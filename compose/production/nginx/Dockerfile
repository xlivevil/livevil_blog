FROM nginx:1.18.0

# RUN apt-get update && apt-get install -y --allow-unauthenticated cron certbot python3-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/livevil_blog.conf /etc/nginx/conf.d/livevil_blog.conf
COPY ./compose/production/nginx/ssl/ /etc/nginx/