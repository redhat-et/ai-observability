# Observability Stack Installation Guide (Prometheus, Grafana, OpenTelemetry Collector)

This guide provides step-by-step instructions for manually installing Prometheus, Grafana, and OpenTelemetry Collector

## Prerequisites

Before starting, ensure you have the following tools installed:

- `kubectl` - Kubernetes command-line tool
- `helm` - Kubernetes package manager
- Access to a running Kubernetes cluster

Verify cluster connectivity:
```bash
kubectl cluster-info
```

## Prometheus & Grafana Installation Steps

### 1. Create Monitoring Namespace

Create the dedicated namespace for observability components:

```bash
kubectl create namespace llm-d-observability
```

### 2. Add Prometheus Community Helm Repository

Add the official Prometheus Community Helm repository:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 3. Prepare Prometheus Values Configuration

Create a values file for Prometheus configuration. This creates a temporary file with minimal essential configurations:

```bash
cat <<EOF > /tmp/prometheus-values.yaml
grafana:
  adminPassword: admin
  service:
    type: ClusterIP
prometheus:
  service:
    type: ClusterIP
  prometheusSpec:
    serviceMonitorSelectorNilUsesHelmValues: false
    serviceMonitor: {}
    serviceMonitorNamespaceSelector: {}
    maximumStartupDurationSeconds: 300
EOF
```

**Configuration Details:**
- **Grafana**: 
  - Default admin password set to `admin` (change this in production!)
  - Service type set to `ClusterIP` (you can customize ingress separately)
- **Prometheus**:
  - Service type set to `ClusterIP`
  - ServiceMonitor discovery enabled across all namespaces
  - Extended startup timeout for reliable initialization

### 4. Install Prometheus Stack

Install the complete Prometheus stack using Helm:

```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace llm-d-observability \
  -f /tmp/prometheus-values.yaml
```

### 5. Wait for Pods to be Ready

Monitor the installation and wait for all pods to become ready:

```bash
# Wait for Prometheus pods
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=prometheus \
  -n llm-d-observability --timeout=300s

# Wait for Grafana pods  
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana \
  -n llm-d-observability --timeout=300s
```

#### Remove the temporary values file:

```bash
rm -f /tmp/prometheus-values.yaml
```

## Accessing the Services

### Grafana Dashboard

To access Grafana, you can use port-forwarding:

```bash
kubectl port-forward -n llm-d-observability svc/prometheus-grafana 3000:80
```

Then access Grafana at `http://localhost:3000` with:
- **Username**: `admin`
- **Password**: `admin`

### Prometheus UI

To access Prometheus UI:

```bash
kubectl port-forward -n llm-d-observability svc/prometheus-kube-prometheus-prometheus 9090:9090
```

Then access Prometheus at `http://localhost:9090`

## ServiceMonitor Integration

The installed Prometheus stack is configured to automatically discover ServiceMonitor resources across all namespaces, including those created by the LLM-D chart for metrics collection.

Key configuration settings:
- `serviceMonitorSelectorNilUsesHelmValues: false` - Enables discovery of all ServiceMonitors
- `serviceMonitorSelector: {}` - No label restrictions on ServiceMonitor selection
- `serviceMonitorNamespaceSelector: {}` - Discovery across all namespaces

## OpenTelemetryCollector Operator Installation 

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

k get pods -n open-telemetry
```

## Tempo Backend Installation (for Trace Storage)

This section installs **Grafana Tempo** as a backend for trace data using Helm. Tempo integrates smoothly with Grafana and the OpenTelemetry Collector to store and visualize distributed traces.

### 1. Add Grafana Helm Repository

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
````

### 2. Install Tempo

Deploy Tempo into the same observability namespace:

```bash
helm install tempo grafana/tempo \
  --namespace llm-d-observability \
  --set tempo.service.type=ClusterIP
```

This installs Tempo with default in-memory storage suitable for local and development use. For persistent or production storage, additional configuration is required.

### 3. Add Tempo Data Source to Grafana

To connect Grafana to Tempo, open the Grafana dashboard:

```bash
kubectl port-forward -n llm-d-observability svc/prometheus-grafana 3000:80
```

Then navigate to **Configuration → Data Sources → Add data source**, and:

* Select **Tempo**
* Set the URL to:

  ```
  http://tempo:3100
  ```
* Click **Save & Test**

Now your Grafana instance can query and visualize traces stored in Tempo.

### 4. Update OpenTelemetry Collector (Optional)

Make sure your OpenTelemetryCollector exports traces to Tempo:

```yaml
exporters:
  otlp:
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
      exporters: [otlp]
```


✅ **You’re Done!**
Tempo will now receive traces from your applications via OpenTelemetry, and Grafana can display them in the Explore tab.

You can now start running AI workloads and gathering telemetry! See [llama stack](./llama-stack-deploy) to get up & running!

## Uninstallation

To remove the Prometheus stack:

```bash
helm uninstall prometheus --namespace llm-d-observability
kubectl delete namespace llm-d-observability
```

To remove the OpenTelemetry stack:

```bash
helm uninstall cert-manager
helm uninstall opentelemetry-operator
```
