FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y wget adduser libfontconfig1 musl && \
    wget https://dl.grafana.com/enterprise/release/grafana-enterprise_11.4.0_amd64.deb && \
    dpkg -i grafana-enterprise_11.4.0_amd64.deb

EXPOSE 3000

CMD ["/usr/sbin/grafana-server", "--homepath=/usr/share/grafana", "--config=/etc/grafana/grafana.ini"]
