FROM centos:7.5.1804

RUN yum -y update &&  yum -y install epel-release && yum -y install redis && yum -y install net-tools

EXPOSE 6379

#修改绑定IP地址
RUN sed -i -e 's@bind 127.0.0.1@bind 0.0.0.0@g' /etc/redis.conf
#关闭保护模式
RUN sed -i -e 's@protected-mode yes@protected-mode no@g' /etc/redis.conf
#设置密码
RUN echo "requirepass ser2etg#!ss" >> /etc/redis.conf


#启动
ENTRYPOINT [ "/usr/bin/redis-server","/etc/redis.conf"]
CMD []