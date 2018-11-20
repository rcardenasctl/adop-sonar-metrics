FROM docker.elastic.co/beats/filebeat:6.4.3

LABEL MAINTAINER="roberto cardenas <rcardenas20@gmail.com>"

ENV FILEBEAT_HOME /usr/share/filebeat
ENV APPLICATION_HOME /opt/source_collector
ENV PERIOD 30s

ADD ./filebeat/filebeat.yml ${FILEBEAT_HOME}/filebeat.yml
ADD ./sonar_collector ${APPLICATION_HOME}/source_collector

USER root
RUN chown root:filebeat ${FILEBEAT_HOME}/filebeat.yml
RUN chmod go-w /usr/share/filebeat/filebeat.yml
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
USER filebeat

ENTRYPOINT  ["/entrypoint.sh"]
CMD ["start"]