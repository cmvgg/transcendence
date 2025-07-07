FROM docker.elastic.co/elasticsearch/elasticsearch:8.10.2

ENV xpack.security.enabled=true
ENV xpack.monitoring.enabled=true

ENV ES_JAVA_OPTS="-Xms512m -Xmx512m"
ENV discovery.type=single-node
ENV ELASTIC_PASSWORD=changeme
ENV ELASTICSEARCH_USERNAME=elastic
ENV ELASTICSEARCH_PASSWORD=changeme
ENV ELASTICSEARCH_HOST=localhost
ENV ELASTICSEARCH_PORT=9200
ENV ELASTICSEARCH_URL=http://$ELASTICSEARCH_HOST:$ELASTICSEARCH_PORT
ENV ELASTICSEARCH_SSL_VERIFICATION_MODE=none
ENV ELASTICSEARCH_SSL_ENABLED=false
ENV ELASTICSEARCH_SSL_CERT=./config/certs/elastic-certificates.p12
ENV ELASTICSEARCH_SSL_CA=./config/certs/elastic-stack-ca.p12
ENV ELASTICSEARCH_SSL_CIPHERS=TLSv1.2
ENV xpack.security.enabled=false
ENV ES_JAVA_OPTS="-Xms512m -Xmx512m"

