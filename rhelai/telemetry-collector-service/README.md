## Opentelemetry Collector and OpenLit GPU Collector 

OpenLit GPU Collector gathers GPU utilization data from AMD or NVIDIA GPUs. The OpenTelemetry Collector creates a unified way to collect 
metrics, logs, and traces from the system and can then export them to various observability backends.

Edit the default collector [configuration file](./otel-config.yaml) as necessary.
Notice it assumes vLLM is running and generating metrics at `0.0.0.0:8000/metrics`. Add any local workloads for which to collect prometheus metrics.
Update the `/LOCAL/PATH/TO` references.

```bash
mkdir /LOCAL/PATH/TO/otc # for file-storage extension, if configured
```

```bash
cp ./telemetry-collector.service /etc/systemd/system/telemetry-collector.service
systemctl daemon-reload
systemctl start telemetry-collector


bash-5.1# podman ps -a
CONTAINER ID  IMAGE                                      COMMAND               CREATED         STATUS         PORTS                   NAMES
92c05f3dea3b  ghcr.io/openlit/otel-gpu-collector:latest  python collector....  37 minutes ago  Up 37 minutes                          gpu-collector
fc9425a642b8  quay.io/sallyom/rh-otel-collector:latest   --config /etc/ote...  37 minutes ago  Up 37 minutes                          otel-collector

# To stop containers, use
systemctl stop telemetry-collector
```

You should see all metrics (vLLM, GPU, PCP) with

```bash
curl http://localhost:8888/metrics
```

Now, you can export to any observability backend. To run a local observability backend with prometheus, tempo, and perses,
start [telemetry-viewer service](../telemetry-viewer/README.md).
