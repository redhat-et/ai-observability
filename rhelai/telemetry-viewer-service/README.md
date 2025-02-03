## [NEED TO FINISH] Telemetry Viewer Service

POD/Systemd service:

Backends:
* prometheus container & config
* tempo container & config

Visualization
* perses container & resource dir

### Run telemetry-viewer service

```bash
sudo su
cp ./telemetry-viewer.service /etc/systemd/system/telemetry-viewer.service

systemctl daemon-reload
systemctl start telemetry-viewer
systemctl status telemetry-viewer

# Pods should now be running
podman logs prometheus
podman logs tempo
podman logs perses
```

#### Apply Perses Resources

```bash
sudo su
podman cp perses:/bin/percli /tmp/percli
chmod +x /tmp/percli
chown $USER:$USER /tmp/percli
exit
# run following as regular user
mv /tmp/percli ~/.local/bin/
which percli
percli login http://localhost:8080
percli apply -f rhelai/perses/percli/project.json
percli apply -f rhelai/perses/percli/prom-global-datasource.yaml
percli project rhelai

percli apply -f dashboards/gpu-usage.json
percli apply -f dashboards/vllm-performance-overview.json
percli apply -f dashboards/pcp-host-overview.json
```


