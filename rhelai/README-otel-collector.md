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

If you have a Dynatrace account, you can export all telemetry to Dynatrace by uncommenting the `otlp/dynatrace` exporter in
the example opentelemetry-collector configuration file.


### TODO

* document Tempo Datasource & local Tempo backend for trace data

### If exporting to external observability backend, example files for mTLS

certs from OpenShift mTLS otel-collector

```bash
ls -al /etc/certs/opentelemetry-collector
server.crt
server.key
ca.crt
```
