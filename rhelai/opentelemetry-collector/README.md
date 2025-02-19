## Opentelemetry Collector 

The OpenTelemetry Collector creates a unified way to collect 
metrics, logs, and traces from the system and can then export them to various observability backends.
Paired with Performance Co-Pilot (PCP) in RHEL, any workload metrics can be received by the otel-collector and
exported with a single stream to be ingested by PCP's pmproxy service connected to Redis or Valkey.

* Edit the default collector [configuration file](./otel-config.yaml) as necessary.
* Copy the configuration file to `/etc/opentelemetry-collector` directory, like so:

OpenTelemetry Collector does not require root privilege, but here we're running as the root user to simplify and
run all systemd services as root. You may want to run as non-root and as a regular user systemd service.

```bash
mkdir /etc/opentelemetry-collector
cp ./otel-config.yaml /etc/opentelemetry-collector/
```

Notice it assumes vLLM is running and generating metrics at `0.0.0.0:8000/metrics`.
Add any local workloads for which to collect prometheus metrics. Another example of a workload that will be be collected by
otel-collector is [openlit-gpu-collector](../telemetry-collection/openlit-gpu-collector/podman-cmd). If you start that podman command
you'll see gpu metrics along with vLLM metrics.

```bash
cp ./opentelemetry-collector.service /etc/systemd/system/opentelemetry-collector.service
systemctl daemon-reload
systemctl start opentelemetry-collector

# To view container logs, use
podman logs opentelemetry-collector

# To stop containers, use
systemctl stop opentelemetry-collector
```

You should now see vLLM metrics or any metrics you've added to the opentelemtry-collector configuration, with

```bash
curl http://localhost:7777/metrics
```

Now, you can export to any observability backend.
If Grafana is already running with the PCP plugin, additional Datasources can be configured (Tempo or Jaeger tracing backends).


**NOTE** You can simply run the otel-collector `podman run` command outlined in the [unit file](./opentelemetry-collector.service).
You don't need to run them together as a systemd service, but if you `systemctl enable opentelemetry-collector`, the container will
be running with any system boot. 

