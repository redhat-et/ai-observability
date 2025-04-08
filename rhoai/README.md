# Monitor Llamastack & vLLM in OpenShift

Follow this README to configure an observability stack in OpenShift to visualize Llamastack telemetry and vLLM metrics.
First, ensure Llamastack and vLLM are configured to generate telemetry by following this [configuration guide](./run-configuration.md)


## OpenShift Observability Operators

Operators are available from OperatorHub
The following operators must be installed in order to proceed with this example.

### Operator descriptions

1. **Red Hat Build of OpenTelemetry**: The OpenTelemetry Collector (OTC) is provided from this operator.
Metrics and traces will be distributed from the OTC to various backends. Tempo is deployed and is the tracing backend.

2. **Tempo Operator**: Provides `TempoStack` Custom Resource. This is the backend for distributed tracing.
An S3-compatible storage (Minio) is paired with Tempo.

3. **Cluster Observability Operator**: This provides PodMonitor and ServiceMonitor Custom Resources which are necessary for 
user-workload monitoring's prometheus to scrape workload metrics. Also, the COO provides UIPlugins for viewing telemetry. 

3. **(optional) Grafana Operator**: Provides Grafana APIs including `GrafanaDashboard`, `Grafana`, and `GrafanaDataSource` that will be used to visualize telemetry.

## Create PodMonitor or ServiceMonitor for any AI Workload that exposes a metrics endpoint

This is how to enable collection of user-workload metrics for any workload within OpenShift. You need to create a `PodMonitor` or a `ServiceMonitor`.
The PodMonitor will ensure all metrics from pods with matching selectors will be scraped by the user-workload-monitoring Prometheus, and a ServiceMonitor will
scrape from any pod that runs under a particular service.

* [Example PodMonitor](./podmonitor-example-0.yaml)
* [Example ServiceMonitor](./servicemonitor-example.yaml)

Upon creation of either, metrics will be scraped and will be visible from the console `Observe -> Metrics` dashboards.

## Create custom resources and configurations for a central observability hub

Create the observablity hub namespace `observability-hub`. If a different namespace is created, be sure to update the resource yamls accordingly.

```bash
oc create ns observability-hub
```

### Tracing Backend (Tempo with Minio for S3 storage)

In order to view distributed tracing data from LLamastack and/or vLLM, you must deploy a tracing backend. The supported tracing backend in OpenShift
is Tempo. See the OpenShift Tempo
[documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/distributed_tracing/distributed-tracing-platform-tempo#distr-tracing-tempo-install-tempostack-web-console_dist-tracing-tempo-installing)
for further details. Tempo must be paired with a storage solution. For this example, `MinIO` is used. The necessary resources can be created by
applying the `./tempo` manifests. 

```bash
# edit storageclassName & secret as necessary
# secret and storage for testing only
oc apply --kustomize ./tempo -n observability-hub
```

### OpenTelemetryCollector deployment

OpenTelemetry Collector is used to aggregate telemetry from various workloads, process individual signals, and export
to various backends. This example will collect traces from various workloads and export all as a single
authenticated stream to the in-cluster TempoStack. For in-cluster only, opentelemetry-collector is not necessary to collect
metrics. Metrics are sent to the in-cluster user-workload-monitoring prometheus by creating the podmonitors and servicemonitors.
However, if exporting off-cluster to a 3rd party observability vendor, the collector is necessary for all signals,
and can provide a single place with which to receive telemetry from various workloads and export as a single authenticated and
secure OTLP stream.

To create a central opentelemetry-collector, update the
[otel-collector/otel-collector.yaml](./otel-collector/otel-collector.yaml) to match your requirements and then apply.

```bash
oc apply --kustomize ./otel-collector -n observability-hub
```

### OpenTelemetryCollector Sidecars deployment

You can add individual metrics endpoints to the central otel-collector in observability-hub, but
another way is to add otel-collector sidecar containers to individual deployments throughout the
cluster. Paired with an annotation on the deployment, telemetry will be exported as configured.
Any deployment with the annotation below will receive and export telemetry as configured in the
[otel-collector-vllm-sidecar.yaml](./otel-collector/otel-collector-vllm-sidecar.yaml).

The example here will add an otel-collector sidecar custom resource to the `llama-serve` namespace,
and to trigger a sidecar container, annotate any deployment's `template.metadata.annotations` with:
`sidecar.opentelemetry.io/inject: vllm-otelsidecar`

```bash
oc apply -f ./otel-collector/otel-collector-vllm-sidecar.yaml

# Then, annotate whatever vllm deployment you'd like to collect metrics from
# Or, add the annotation to the deployment's `template.metadata.annotations` from the console.
oc patch deployment <deployment-name> \
  -n <namespace> \
  --type='merge' \
  -p '{"spec":{"template":{"metadata":{"annotations":{"sidecar.opentelemetry.io/inject":"vllm-otelsidecar"}}}}}'
```

### Cluster Observability Operator Tracing UIPlugin

The Jaeger frontend feature of TempoStack is no longer supported by Red Hat. This has been replaced by the COO UIPlugin. To create the UIPlugin for
Tracing, first ensure the TempoStack described above is created. This is a prerequisite. Then, all that's necessary to view traces from
the OpenShift console at `Observe -> Traces` is to create the following [Tracing UIPlugin resource](./tracing-ui-plugin.yaml). 

```bash
oc apply ./tracing-ui-plugin.yaml
```

You should now see traces and metrics in the OpenShift console, from the `Oberve` tab. 

### Grafana 

Most users are familiar with Grafana for visualizing and analyzing telemetry. To create the Grafana resources necessary to view
Llamastack and vLLM telemetry, follow the below example.

This example will deploy a Grafana instance, and Prometheus & Tempo DataSources
The prometheus datasource is the user-workload-monitoring prometheus running in `openshift-user-workload-monitoring` namespace.
The Grafana console is configured with `username: rhel, password: rhel`

```bash
cd grafana
./deploy-grafana.sh
```
Upon success, you can explore metrics and traces from Grafana route.

#### GrafanaDashboard to visualize cluster metrics and traces

Check out [github.com/kevchu3/openshift-4-grafana](https://github.com/kevchu3/openshift4-grafana/tree/master/dashboards/crds) for a list of
dashboards to deploy on OpenShift.

Here's an example to download and deploy a GrafanaDashboard for OpenShift 4.16 cluster metrics.
The dashboard is slightly modified from https://github.com/kevchu3/openshift4-grafana/blob/master/dashboards/json_raw/cluster_metrics.ocp416.json

```bash
oc apply -n observability-hub -f cluster-metrics-dashboard/cluster-metrics.yaml 
```
