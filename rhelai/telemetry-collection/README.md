## Opentelemetry Collector and OpenLit GPU Collector 

OpenLit GPU Collector gathers GPU utilization data from AMD or NVIDIA GPUs. The OpenTelemetry Collector creates a unified way to collect 
metrics, logs, and traces from the system and can then export them to various observability backends.

* Edit the default collector [configuration file](./otel-config.yaml) as necessary.
* Update `/LOCAL/PATH/TO` in line #34 of [unit file](./telemetry-collector.service) to the absolute path to the `otel-config.yaml` 

Notice it assumes vLLM is running and generating metrics at `0.0.0.0:8000/metrics`. Add any local workloads for which to collect prometheus metrics.

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

You should now see vLLM and GPU metrics with

```bash
curl http://localhost:7777/metrics
```

Now, you can export to any observability backend.
If Grafana is already running with the PCP plugin, additional Datasources can be configured (Tempo or Jaeger tracing backends).


**NOTE** You can simply run the 2 containers with their `podman run` commands outlined in the [unit file](./telemetry-collector.service). You don't
need to run them together as a systemd service. 

