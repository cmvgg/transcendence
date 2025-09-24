#!/bin/bash

mkdir -p monitoring/grafana/provisioning/dashboards

curl -o monitoring/grafana/provisioning/dashboards/postgres_dashboard.json https://grafana.com/api/dashboards/9628/revisions/latest/download

sed -i 's/"datasource": "${DS_PROMETHEUS}"/"datasource": "Prometheus"/g' monitoring/grafana/provisioning/dashboards/postgres_dashboard.json
sed -i 's/"datasource": "${DS_PROMETHEUS}"/"datasource": "Prometheus"/g' monitoring/grafana/provisioning/dashboards/django_dashboard.json

echo "Dashboard de PostgreSQL configurate."
