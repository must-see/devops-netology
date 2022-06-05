FROM elasticsearch:7.17.4

# container creator
MAINTAINER elasticsearch

# copy the configuration file into the container
COPY elasticsearch.yml /usr/share/elasticsearch/config


RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/config
RUN mkdir /var/log/elasticsearch
RUN chown -R elasticsearch:elasticsearch /var/log/elasticsearch
RUN mkdir /var/lib/elasticsearch
RUN chown -R elasticsearch:elasticsearch /var/lib/elasticsearch
RUN mkdir /var/lib/elasticsearch/snapshots
RUN chown -R elasticsearch:elasticsearch /var/lib/elasticsearch/snapshots

# expose the default Elasticsearch port
EXPOSE 9200