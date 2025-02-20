# ai-observability
Demos and landing place for observability work related to AI 

* [RHEL AI System Performance Metrics](./rhelai/README.md)
    * [PCP](./rhelai/README.md#performance-co-pilot)
    * [Redis](./rhelai/redis-service/README.md)
    * [Grafana](./rhelai/grafana-service/README.md)

* AI Workloads
  * [vLLM](./rhelai/vllm/README.md)
  * [vLLM with OTLP Tracing](./rhelai/vllm/README.md#vllm-with-otlp-tracing)
  * vLLM Dashboards
      * [Performance-Co-Pilot Grafana Dashboard](./rhelai/vllm/vllm-pcp-grafana-dashboard.json)
      * [OpenShift Grafana Dashboard](./vllm-dashboards/vllm-grafana-openshift.json)
      * [OpenShift Perses Dashboard](./vllm-dashboards/vllm-perses-openshift.json)
  * [Llamastack Server](./rhelai/ai-workloads/llama-stack/README.md)
  * [ilab model download; ilab model serve](./rhelai/vllm/README.md#instructlab-cli-to-serve-llms-with-vllm)

* RHEL AI Workload Monitoring
  * [OpenTelemetry Collector](./rhelai/opentelemetry-collector/README.md)
  * [OpenLit GPU Collector](./rhelai/telemetry-collection/README.md)
  * [Tempo Tracing Backend and Grafana Datasource](./rhelai/tempo-service/README.md)
  * [PCP OpenMetrics Plugin](./rhelai/workload-monitoring/pcp-pmda-openmetrics.md)
