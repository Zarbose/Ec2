FROM grafana/grafana-oss:9.4.3

COPY grafana/provisioning/dashboards /etc/grafana/provisioning/dashboards
COPY grafana/provisioning/datasources /etc/grafana/provisioning/datasources

# ENV GF_SECURITY_ADMIN_USER=admin
# ENV GF_SECURITY_ADMIN_PASSWORD=12345678 