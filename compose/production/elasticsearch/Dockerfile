FROM elasticsearch:5.6.16-alpine

COPY ./compose/production/elasticsearch/elasticsearch-analysis-ik-5.6.16 /usr/share/elasticsearch/plugins/elasticsearch-analysis-ik-5.6.16

USER root
COPY ./compose/production/elasticsearch/elasticsearch.yml /usr/share/elasticsearch/config/
RUN chown elasticsearch:elasticsearch /usr/share/elasticsearch/config/elasticsearch.yml

USER elasticsearch