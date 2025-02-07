# Serve `meta-llama/Llama-3.1-8B-Instruct` with vLLM

## Run vLLM with Podman (x86_64 only)

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

### View vLLM traces

If opentelemetry-collector is running with a tracing backend and exporting to a visualization backend, you can view the traces there.

You can see the traces in the collector logs by setting `verbosity: detailed` in the collector configuration.

**TODO: View with Tempo** 

## Download and Serve with Instructlab

If not running Llamastack and you only care about serving vLLM, you can use RHEL AI's out-of-the-box `ilab` CLI
See [here](./ilab-serve.md)
