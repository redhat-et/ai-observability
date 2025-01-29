## Everything needed in RHEL AI

```bash
systemctl start pcp
systemctl start pmlogger
systemctl start pmproxy

cd vllm
./podman-cmd-llama3

cd otel-collector
./podman-cmd

cd openlit-gpu-collector
./podman-cmd
```

### TODO

* Grafana or Perses visualizing

* Create quadlets/systemd services for podman containers

### ONLY needed for exporting to OpenShift

certs from OpenShift mTLS otel-collector

```bash
ls -al /etc/certs/opentelemetry-collector
server.crt
server.key
ca.crt
```
