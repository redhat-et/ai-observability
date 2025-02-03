## Start Performance Co-Pilot (PCP) Services

RHEL AI includes PCP services. All that's required to use PCP is to start or enable the systemd services.
For this you need to run as sudo user.

```bash
systemctl start pmcd
systemctl start pmlogger
systemctl start pmproxy

# check to ensure the services are started
systemctl status [service]
```

See [PCP setup](./pcp/README.md) for more information. 

Metrics are scraped with a Prometheus receiver configured in an OpenTelemetry Collector (OTC)
running in a podman container.

## Run AI workload instrumented to generate OTLP data and/or Prometheus metrics

For this, I've created a vLLM image that has the added opentelemetry packages to generate OTLP trace data.
See the [Containerfile](./vllm/Containerfile).
By default, vLLM generates OTLP metrics.

Update the [podman-cmd](./vllm/podman-cmd) to match your vLLM requirements.
model downloaded. Follow these [notes](./vllm/README.md) to download llama3 to use the podman-cmd as/is.

```bash
cd vllm
./podman-cmd

podman ps # should show a container vllm
podman logs vllm
```

Generate traffic with vLLM by either using it in an application or with this [curl command](./vllm/curl-vllm)

```bash
./curl-vllm
```

## Telemetry Collector service

OpenTelemetry collector and OpenLit GPU collector can be started together with [telemetry-collector.service](./telemetry-collector-service/README.md).
This service runs the otel-collector and gpu-collector podman containers.

## Telemetry Viewer service

You can add an exporter in the opentelemetry configuration to export all telemetry to any observability backend.
To view data locally, you can start the [telemetry-viewer.service](./telemetry-viewer-service/README.md).
The `telemetry-viewer.service` will start local prometheus, tempo, and perses podman containers. Perses is a grafana-like
visualization tool with a CLI for managing resources such as projects, datasources, dashboards. Many grafana dashboards can be migrated to perses.

If you have a Dynatrace account, you can also export all telemetry to Dynatrace by uncommenting the `otlp/dynatrace` exporter in
the example opentelemetry-collector configuration file.

### TODO

* create Global Tempo datasource & local Tempo backend for trace data

* Create quadlets/systemd services/compose files for podman containers

* Check all podman commands, remove unnecessary privileges


### If exporting to external observability backend, example files for mTLS

certs from OpenShift mTLS otel-collector

```bash
ls -al /etc/certs/opentelemetry-collector
server.crt
server.key
ca.crt
```
