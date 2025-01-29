## Setting up Performance Co-Pilot in RHEL AI

Performance Co-Pilot (PCP) is installed out-of-the-box with RHEL AI.
All that's required is to start the PCP systemd services.

**TODO**
- check to ensure all these are required
- document how to configure basic things, like how long to keep logs, sampling rate, etc

```bash
sudo su
systemctl enable pmcd --now
systemctl enable pmlogger --now
systemctl enable pmproxy --now

# check to ensure the services are started
systemctl status [service]
```

Metrics are scraped with a Prometheus receiver configured in an  OpenTelemetry Collector (OTC)
running in a podman container. From there, a Prometheus DataSource in Grafana can be used to visualize PCP metrics.

## Run OpenTelemetry Collector

**TODO** add systemd service for running container?

### Update OpenTelemetry Collector config

Edit the default collector [configuration file](otel-collector/otel-config.yaml) as necessary.

### Run OpenTelemetry Collector with podman

The following will start an opentelemetry-collector container running in the background.

```bash
mkdir otc # for file-storage extension, if configured

cd otel-collector
./podman-cmd

podman ps # should show a container otelcol-host
podman logs otelcol-host
```

### Run vLLM server or any AI workload instrumented to generate OTLP data

For this, I've created a vLLM image that has the added opentelemetry packages to generate OTLP trace data.
See the [Containerfile](./vllm/Containerfile).
By default, vLLM generates OTLP metrics.

Update the [podman-cmd](./vllm/podman-cmd) to match your vLLM requirements. For this example, we have a llama3
model downloaded. Follow these [notes](./vllm/notes) to download llama3 to use the podman-cmd as/is.

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

### Run openlit GPU Collector 

**TODO** Add more info

```bash
cd openlit-gpu-collector
./podman-cmd
```

### TODO

* Grafana or Perses visualizing

* Create quadlets/systemd services for podman containers

* Check all podman commands, remove unnecessary privileges

* Import Grafana Dashboards for vLLM, GPU metrics, and PCP

### ONLY needed for exporting to OpenShift

certs from OpenShift mTLS otel-collector

```bash
ls -al /etc/certs/opentelemetry-collector
server.crt
server.key
ca.crt
```
