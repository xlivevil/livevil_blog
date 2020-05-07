FROM nginx:1.18.0

# 替换为国内源
RUN yum update && yum install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/livevil_blog.conf /etc/nginx/conf.d/livevil_blog.conf