# vLLM (x86_64 only)

This example serves `meta-llama/Llama-3.1-8B-Instruct` with tool-calling and telemetry collection.
All commands are assumed to run as root user and haven't been tested as non-root.

## Run vLLM as a Systemd Service

```bash
# Edit ./vllm-env to match requirements and provide Huggingface Token
mkdir /etc/vllm && cp ./vllm-env /etc/vllm/defaults
curl -o /etc/vllm/tool_chat_template_llama3.1_json.jinja https://raw.githubusercontent.com/vllm-project/vllm/refs/heads/main/examples/tool_chat_template_llama3.1_json.jinja
cp ./vllm.service /etc/systemd/system/vllm.service
systemctl daemon-reload
systemctl start vllm

# To start vLLM container when system boots
systemctl enable vllm

# vLLM container should now be running
podman logs -f vllm

# Check that the model is loaded with
curl http://localhost:8000/v1/models
```

## Run vLLM with Podman

You can serve `meta-llama/Llama-3.1-8B-Instruct` with a vLLM podman container with [this podman cmd](./no-otel-podman-cmd), by running

```bash
./podman-cmd-no-otel

# vllm container will run in the background, to view logs run
podman logs vllm

# to view log stream
podman logs -f vllm
```

## Run vLLM with OTLP Tracing

To enable trace generation in vLLM, the packages listed in this [Containerfile](./Containerfile) are required. `quay.io/sallyom/vllm:otlp` was built
with this Containerfile.

You can serve `meta-llama/Llama-3.1-8B-Instruct` with a vLLM podman container with tracing enabled, with [this podman cmd](./podman-cmd), by running

```bash
./podman-cmd

# vllm container will run in the background, to view logs run
podman logs vllm

# to view log stream
podman logs -f vllm
```

## Monitoring vLLM

### View vLLM metrics

```bash
curl http://localhost:8000/metrics
```

If opentelemetry-collector is running with a metrics backend and exporting to a visualization backend such as Grafana, you can explore the metrics
there. 

#### [WIP] vLLM PCP Grafana Dashboard

[This dashboard](./vllm-pcp-grafana-dashboard.json) shows similar data to vLLM's
[upstream grafanadashboard](https://github.com/vllm-project/vllm/blob/main/examples/online_serving/prometheus_grafana/grafana.json).
This dashboard is a WIP and will be updated in the near future.

### View vLLM traces

If opentelemetry-collector is running with a tracing backend and exporting to a visualization backend, you can view the traces there.

You can see the traces in the collector logs by setting `verbosity: detailed` in the collector configuration.

Follow the [Tempo example](../tempo-service/README.md) to add a local `Tempo` tracing backend and `Tempo Datasource` to Grafana.

## Download and Serve with Instructlab

If not running Llamastack and you only care about serving vLLM, you can use RHEL AI's out-of-the-box `ilab` CLI
See [here](./ilab-serve.md)
