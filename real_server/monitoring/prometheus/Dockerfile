FROM debian:bullseye-slim

RUN apt-get -y update
RUN	apt-get install bash
RUN	apt-get install -y gpg
RUN	apt-get install -y dpkg
RUN	apt-get install -y apt-transport-https software-properties-common wget

RUN apt-get install -y adduser libfontconfig1 musl

RUN	wget https://github.com/prometheus/prometheus/releases/download/v3.1.0/prometheus-3.1.0.linux-amd64.tar.gz

RUN tar -xf prometheus-3.1.0.linux-amd64.tar.gz

RUN cd prometheus-3.1.0.linux-amd64

RUN apt-get -y update

EXPOSE 9090

CMD ["/prometheus-3.1.0.linux-amd64/prometheus", "--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus", "--web.listen-address=:9090"]
