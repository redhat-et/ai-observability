# AI Workload monitoring

PCP is designed to monitor the host system performance metrics. The PMDA `openmetrics` plugin installed above allows PCP to ingest workload
(prometheus and/or OTLP) metrics as well. The `Red Hat Build of OpenTelemetry Collector` can also be deployed to collect metrics, logs, and traces from all
workloads. The Grafana server installed above can be used to visualize all telemetry locally. However, depending on your requirements, exporting data
to an external observability stack such as on OpenShift, or to an observability vendor such as Dynatrace, is also an option.
Here the various choices for building out a more complete observability solution are outlined.

* [Add workload metrics to PCP, visualize in local Grafana](./workload-monitoring/pcp-pmda-openmetrics.md)

## OpenTelemetry Collector to unify workload metrics into a single prometheus stream to be injested by PCP

With the following otel-collector configuration, various workload metrics can be combined and exported as a single stream, to be ingested by PCP

```yaml
receivers:
  prometheus:
    config:
      scrape_configs:
      - job_name: 'vllm'
        scrape_interval: 5s
        static_configs:
          - targets: ['0.0.0.0:8000']
      - job_name: 'kepler'
        scrape_interval: 5s
        static_configs:
          - targets: ['0.0.0.0:8888']
      - job_name: 'another-workload'
        scrape_interval: 5s
        static_configs:
          - targets: ['0.0.0.0:5555']

  otlp:
    protocols:
      http:
      grpc:

exporters
  prometheus:
    endpoint: 0.0.0.0:7777 #<-with this you can `curl localhost:7777/metrics` to see all metrics

service:
  pipelines:
    metrics:
      receivers: [otlp, prometheus]
      processors: [batch, memory_limiter]
      exporters: [prometheus]
```

With the openmetrics PCP plugin, a file with contents `http://127.0.0.1:7777` in `/var/lib/pcp/pmdas/openmetrics/config.d/prometheus.url`
will result in all workload metrics above being shown in Grafana with the PCP Datasource.

## OpenTelemetry Collector to unify collection of all telemetry (metrics, logs, and traces) and export to external observability stack

To export telemetry to an external observability stack or vendor, add additional exporters to configuration above, similar to

```yaml

exporters:
  otlphttp/dynatrace:
    endpoint: "https://ENVIRONMENT.live.dynatrace.com/api/v2/otlp"
    headers:
      Authorization: "Api-Token xxxx.XXXX.XXXXXX"
  otlphttp/ocp:
    endpoint: https://external-otel-collector-enpoint.org
    tls:
      insecure: false
      cert_file: /certs/server.crt
      key_file: /certs/server.key
      ca_file: /certs/ca.crt
service:
  pipelines:
    traces:
      receivers: [otlp, prometheus]
      processors: [batch, memory_limiter]
      exporters: [otlphttp/dynatrace, otlphttp/ocp, otlphttp/tempo]
    metrics:
      receivers: [otlp, prometheus]
      processors: [batch, memory_limiter]
      exporters: [prometheus, otlphttp/dynatrace, otlphttp/ocp]
```

