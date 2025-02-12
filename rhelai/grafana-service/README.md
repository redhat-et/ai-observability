# Grafana

All commands are assumed to run as root user and haven't been tested as non-root.

## Run Grafana container as a systemd service

The unit file, [grafana.service](./grafana.service) starts a grafana podman container with PCP plugins,
as the PCP documentation suggests [here](https://grafana-pcp.readthedocs.io/en/latest/installation.html#container).
The `grafana-pcp` rpm has an issue with how it's configured to run as the `grafana` user, but running as a container works well.

```bash
cp ./grafana.service /etc/systemd/system/grafana.service
systemctl daemon-reload
systemctl start grafana

# To start grafana container when system boots
systemctl enable grafana

# Grafana container should now be running
podman logs -f grafana
```

### Run Grafana with Podman

Grafana can be started from [this podman command](https://grafana-pcp.readthedocs.io/en/latest/installation.html#container).

### Grafana data will be in grafana-data podman volume
podman volume inspect grafana-data
```
