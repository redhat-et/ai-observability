# Remote vLLM Llama Stack with OpenTelemetry Tracing on minikube

This directory contains everything needed to build and deploy a Llama Stack distribution for remote vLLM with OpenTelemetry tracing enabled to minikube.
The setup sends traces to Grafana Tempo for observability.

## 🎯 What's Included

 **OTEL-enabled configuration** - Pre-configured to send traces to Grafana Tempo
- **Kubernetes deployment** - Ready-to-deploy to minikube with OTEL collector
- **Complete build and deployment automation** - Single script deployment
- **OTEL Collector Operator integration**

## 📋 Prerequisites

- **running minikube or Kubernetes cluster** - Local Kubernetes cluster
- **vLLM endpoint** - vLLM endpoint accessible
- **kubectl** - Kubernetes CLI
- **Podman** (or Docker) - For building containers
- **OTEL Collector Operator** - Must be installed in your cluster. See [minikube-k8s observability stack](../README.md)
- **Tempo Backend for Trace storage** - Must be installed in your cluster. See [minikube-k8s observability stack](../README.md)


## 🚀 Quick Deployment of Llama Stack with remote vLLM to minikube

It is assumed that miniKube is running with OpenTelemetry Operator and there is an accessible vLLM endpoint.
The model configured is `meta-llama/Llama-3.2-3b`

## 🔧 Configuration

### Environment Variables in Deployment

Edit [llama-stack-deploy/k8s/deployment.yaml](./llama-stack-deploy/k8s/deployment.yaml) environment variables

```yaml
        - name: VLLM_URL
          value: "http://llm-d-inference-gateway.llm-d.svc.cluster.local:80/v1"
        - name: INFERENCE_MODEL
          value: "meta-llama/Llama-3.2-3B-Instruct"  # Update this to your model
        - name: VLLM_MAX_TOKENS
          value: "4096"
        - name: VLLM_API_TOKEN
          value: "fake"
        - name: VLLM_TLS_VERIFY
          value: "true"
        - name: TELEMETRY_SINKS
          value: "console,sqlite,otel_trace"
        - name: OTEL_TRACE_ENDPOINT
          #value: "http://localhost:4318/v1/traces"
          value: "http://tracing-collector-collector.llm-d-monitoring.svc.cluster.local:4318/v1/traces"
        - name: OTEL_SERVICE_NAME
          value: "llama-stack"
```

### Optional API Keys

If you want to use external APIs, create a secret:

```bash
# Copy the template and fill in your keys
cp k8s/secret-template.yaml k8s/secret.yaml
# Edit k8s/secret.yaml with your actual API keys
kubectl apply -f llama-stack-deploy/k8s/secret.yaml
```

## 🚀 Deploy!

```bash
kubectl create namespace llama-stack
kubectl apply -k llama-stack-deploy/k8s
```

## 🔍 Accessing the Service

After deployment, you can access Llama Stack at:

```bash
# Get the minikube IP and service port
MINIKUBE_IP=$(minikube ip)
NODE_PORT=$(kubectl get svc llamastack -n llama-stack -o jsonpath='{.spec.ports[0].nodePort}')
echo "http://${MINIKUBE_IP}:${NODE_PORT}"
curl "http://${MINIKUBE_IP}:${NODE_PORT}/v1/providers"
curl ""http://${MINIKUBE_IP}:${NODE_PORT}/v1/models"
```

Example chat completion (minikube ip 192.168.49.2, nodePort 30321)

```bash
curl http://192.168.49.2:30321/v1/inference/chat-completion \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "meta-llama/Llama-3.2-3b-Instruct",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

With `llama-stack-client`

```bash
llama-stack-client configure --endpoint http://192.168.49.2:30321
llama-stack-client models list
llama-stack-client inference chat-completion --message "Hello, how are you?"
```

## 📊 Viewing Traces

Traces are sent to your Grafana Tempo instance at `http://tempo.llm-d-monitoring.svc.cluster.local:3100`. You can view them in Grafana using the Tempo datasource.

### Cleaning Up

```bash
# Delete all resources
kubectl delete -k llama-stack-deployk8s

# Or delete just the namespace (removes everything)
kubectl delete namespace llama-stack
```

## 🤝 Support

For issues related to:
- **Llama Stack**: Check the [official repository](https://github.com/meta-llama/llama-stack)
- **OpenTelemetry**: Refer to [OTEL documentation](https://opentelemetry.io/docs/)
- **OTEL Collector Operator**: See [Operator documentation](https://github.com/open-telemetry/opentelemetry-operator)
- **Grafana Tempo**: See [Tempo documentation](https://grafana.com/docs/tempo/)
