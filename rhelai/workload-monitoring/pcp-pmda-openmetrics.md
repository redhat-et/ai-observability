## Add Workload Metrics Endpoints to Performance Co-Pilot

You can ingest data from additional metrics endpoints by adding files to `/etc/pcp/pmdas/openmetrics/config.d`.

For example, `vLLM` serves its metrics at `localhost:8000/metrics`. To ingest these metrics with PCP and view them in Grafana, place this file:

```bash
$ cat /var/lib/pcp/pmdas/openmetrics/config.d/vllm.url
http://127.0.0.1:8000/metrics
```

## Add all workload metrics to Performance Co-Pilot from OpenTelemetry Collector

You can send all workload metrics collected by the otel-collector to PCP using a prometheus exporter.

Add these to the opentelemetry-collector configuration and restart the otel-collector.

```yaml
exporters:
  prometheus:
    endpoint: 0.0.0.0:7777 #<-with this you can `curl localhost:7777/metrics` to see all metrics

receivers:
  prometheus:
    config:
      scrape_configs:
      - job_name: 'vllm'
        scrape_interval: 5s
        static_configs:
          - targets: ['0.0.0.0:8000']

service:
  pipelines:
    metrics:
      receivers: [otlp, prometheus]
      processors: [batch, memory_limiter]
      exporters: [prometheus, debug]
```

Then, add a url file to the pcp/pmdas/openmetrics config directory:

```bash
$ cat /var/lib/pcp/pmdas/openmetrics/config.d/prometheus.url
http://127.0.0.1:7777/metrics
```

That's it! You should now see the any metrics collected with the otel-collector in the Grafana `performancecopilot-valkey` Explorer.
