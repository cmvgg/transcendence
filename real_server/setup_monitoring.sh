#!/bin/bash

# Crear directorios necesarios
mkdir -p monitoring/grafana/provisioning/dashboards
mkdir -p monitoring/grafana/provisioning/datasources

# Crear archivo de configuración para datasources
cat > monitoring/grafana/provisioning/datasources/datasource.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF

# Crear archivo de configuración para dashboards
cat > monitoring/grafana/provisioning/dashboards/dashboard.yml << EOF
apiVersion: 1

providers:
  - name: 'Default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
      foldersFromFilesStructure: true
EOF

# Crear un dashboard simple para probar
cat > monitoring/grafana/provisioning/dashboards/postgres_dashboard.json << EOF
{
  "annotations": {
    "list": []
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "hideControls": false,
  "links": [],
  "liveNow": false,
  "panels": [
    {
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "id": 1,
      "options": {
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showThresholdLabels": false,
        "showThresholdMarkers": true
      },
      "title": "PostgreSQL Up",
      "type": "gauge",
      "targets": [
        {
          "datasource": "Prometheus",
          "expr": "up{job=\"postgres\"}",
          "refId": "A"
        }
      ]
    }
  ],
  "schemaVersion": 36,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "PostgreSQL Dashboard",
  "uid": "postgres-dashboard",
  "version": 1
}
EOF

# Crear/actualizar archivo prometheus.yml
mkdir -p monitoring/prometheus
cat > monitoring/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']
EOF

# Modificar el Dockerfile de Grafana para asegurarnos que los directorios de provisión existen
cat > monitoring/grafana/Dockerfile << EOF
FROM debian:bullseye
RUN apt-get update && \\
    apt-get install -y wget adduser libfontconfig1 musl && \\
    wget https://dl.grafana.com/enterprise/release/grafana-enterprise_11.4.0_amd64.deb && \\
    dpkg -i grafana-enterprise_11.4.0_amd64.deb

# Crear directorios de provisión
RUN mkdir -p /etc/grafana/provisioning/dashboards /etc/grafana/provisioning/datasources && \\
    chown -R grafana:grafana /etc/grafana/provisioning

# Establecer permisos
ENV GF_PATHS_PROVISIONING=/etc/grafana/provisioning

EXPOSE 3000
CMD ["/usr/sbin/grafana-server", "--homepath=/usr/share/grafana", "--config=/etc/grafana/grafana.ini"]
EOF

echo "Configuración completada"