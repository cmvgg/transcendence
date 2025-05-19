FROM debian:bullseye
RUN apt-get update && \
    apt-get install -y wget adduser libfontconfig1 musl && \
    wget https://dl.grafana.com/enterprise/release/grafana-enterprise_11.4.0_amd64.deb && \
    dpkg -i grafana-enterprise_11.4.0_amd64.deb

# Crear directorios de provisión
RUN mkdir -p /etc/grafana/provisioning/dashboards /etc/grafana/provisioning/datasources && \
    chown -R grafana:grafana /etc/grafana/provisioning

# Establecer permisos
ENV GF_PATHS_PROVISIONING=/etc/grafana/provisioning

EXPOSE 3000
CMD ["/usr/sbin/grafana-server", "--homepath=/usr/share/grafana", "--config=/etc/grafana/grafana.ini"]
