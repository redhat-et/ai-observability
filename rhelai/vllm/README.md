## Serve LLMs with vLLM & InstructLab

The instructLab CLI is included in RHEL AI. This makes it easy to download and serve models. Here's how to serve `meta-llama/Llama-3.2-8B-Instruct`.
Note this is a safetensors formatted LLM, rather than a GGUF. This model is ~16G. You'll need a Huggingface API Token for most models.

```bash
ilab model download --repository meta-llama/Llama-3.2-8B-Instruct --hf-token XXXxxxxx
ilab model serve --gpus=2 --backend=vllm --model-path=/var/home/cloud-user/.cache/instructlab/models/meta-llama/Llama-3.2-8B-Instruct 
```

## vLLM with OTLP Tracing

To enable trace generation in vLLM, the packages listed in this [Containerfile](./Containerfile) are required. `quay.io/sallyom/vllm:otlp` was built
with this Containerfile.

You can serve a Llama3 model with a vLLM podman container with tracing enabled, with [this podman cmd](./podman-cmd), by running

```bash
./podman-cmd
```

View the logs with

```bash
podman logs vllm
```

### View vLLM metrics

```bash
curl http://localhost:8000/metrics
```

### View vLLM traces

If opentelemetry-collector is running, you can view the traces in the logs by setting `verbosity: detailed` in the collector configuration.

**TODO: View with Tempo** 
