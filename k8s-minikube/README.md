# Observability Stack on MiniKube

This guide provides step-by-step instructions for manually installing Prometheus, Grafana, and OpenTelemetry Collector.

> **📝 NOTE:** `llm-d` quickstart installation includes Prometheus, Grafana, and vLLM ServiceMonitor. If you've already installed `llm-d` skip to [opentelemetry operator install](#opentelemetrycollector-operator-installation) and/or [tempo trace backend install](#tempo-backend-installation-for-trace-storage).

## Prerequisites

Before starting, ensure you have:

- `kubectl` - Kubernetes command-line tool
- `helm` - Kubernetes package manager
- Access to a running Kubernetes cluster

## Prometheus & Grafana Installation Steps

> **📝 NOTE:** If running llm-d and it was deployed via the quickstart & without `--disable-metrics-collection`, prometheus & grafana are already installed. For more information about `llm-d quickstart` see [llm-d-deployer quickstart](https://github.com/llm-d/llm-d-deployer/tree/main/quickstart)

### Create Monitoring Namespace

```bash
kubectl create namespace llm-d-observability
```

### Install Prometheus & Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

#### Install Prometheus Stack

```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace llm-d-observability \
  -f ./prom-values.yaml
```
Wait for pods to be ready
```bash
# Wait for Prometheus pods
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=prometheus \
  -n llm-d-observability --timeout=300s

# Wait for Grafana pods  
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana \
  -n llm-d-observability --timeout=300s
```
 
### Accessing the Services

#### Grafana Dashboard

To access Grafana, you can use port-forwarding:

```bash
kubectl port-forward -n llm-d-observability --address 0.0.0.0 svc/prometheus-grafana 3000:80
# --address is necessary if running in cloud VM
```

Then access Grafana at `http://localhost-or-cloud-vm-ip:3000` with username:password `admin:admin`:

#### Prometheus UI

```bash
kubectl port-forward -n llm-d-observability --address 0.0.0.0 svc/prometheus-kube-prometheus-prometheus 9090:9090
# --address is necessary if running in cloud VM
```

Then access Prometheus at `http://localhost-or-cloud-vm-ip:9090`

### ServiceMonitor Integration

The installed Prometheus stack is configured to automatically discover ServiceMonitor resources across all namespaces, including those created by the LLM-D chart for metrics collection.

Key configuration settings:
- `serviceMonitorSelectorNilUsesHelmValues: false` - Enables discovery of all ServiceMonitors
- `serviceMonitorSelector: {}` - No label restrictions on ServiceMonitor selection
- `serviceMonitorNamespaceSelector: {}` - Discovery across all namespaces

#### Example: Add servicemonitor for llm-d endpoint-picker service/pod

If running llm-d, in order to collect vLLM metrics, you need a servicemonitor for the vllm services.

> **📝 NOTE:** If llm-d was deployed via the quickstart & without `--disable-metrics-collection`, the servicemonitor is already created.

```bash
kubectl apply -n llm-d ./modelservice-monitor.yaml
```

## OpenTelemetryCollector Operator Installation 

OpenTelemetry Collector is required with the [Llamastack deployment demo](./llama-stack-deploy/README.md) or any other application configured to generate OTLP telemetry.

```bash
minikube addons enable ingress
helm repo add jetstack https://charts.jetstack.io

helm install --wait \
    --namespace cert-manager \
    --create-namespace \
    --set crds.enabled=true \
    --version 1.15.1 \
    cert-manager jetstack/cert-manager

helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts

helm install --wait \
  --namespace open-telemetry \
  --create-namespace \
  --version 0.65.0 \
  --set "manager.collectorImage.repository=otel/opentelemetry-collector-contrib" \
  opentelemetry-operator open-telemetry/opentelemetry-operator

kubectl get pods -n open-telemetry
```

## Tempo Backend Installation (for Trace Storage)

This section installs **Grafana Tempo** as a backend for trace data using Helm. Tempo integrates smoothly with Grafana and the OpenTelemetry Collector to store and visualize distributed traces. We've already installed Grafana with the `kube-prometheus-stack` above, so only need to install Tempo.

### Add Grafana Helm Repository 

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
````
### Install Tempo

```bash
helm install tempo grafana/tempo \
  --namespace llm-d-observability \
  --set tempo.service.type=ClusterIP
```
This installs Tempo with default in-memory storage suitable for local and development use. For persistent or production storage, additional configuration is required.

### Add Tempo Data Source to Grafana

To connect Grafana to Tempo, open the Grafana dashboard:

```bash
kubectl port-forward -n llm-d-observability --address 0.0.0.0 svc/prometheus-grafana 3000:80
# --address is necessary if running in cloud VM
```
Then navigate to **Configuration → Data Sources → Add data source**, and:

* Select **Tempo**
* Set the URL to:

  ```
  http://tempo:3100
  ```
* Click **Save & Test**

Now your Grafana instance can query and visualize traces stored in Tempo.

### Update OpenTelemetry Collector (If any exist)

Make sure your OpenTelemetryCollector exports traces to Tempo:

```yaml
exporters:
  otlp/tempo:
    endpoint: tempo.llm-d-observability.svc.cluster.local:4317
    tls:
      insecure: true
```

Update your `traces` pipeline to include the exporter:

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [otlp/tempo]
```

✅ **You’re Done!**

You can now start running AI workloads and gathering telemetry! See [llm-d](./llm-d) and then [llama stack](./llama-stack-deploy) to get up & running!

## Uninstallation

To remove the Prometheus, Grafana, Tempo, and OpenTelemetry stack:

```bash
helm uninstall prometheus -n llm-d-observability
helm uninstall tempo -n llm-d-observability
helm uninstall cert-manager -n llm-d-observability
helm uninstall opentelemetry-operator -n llm-d-observability
```
