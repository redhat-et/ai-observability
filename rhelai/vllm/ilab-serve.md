## Serve LLMs with vLLM & InstructLab

The instructLab CLI is included in RHEL AI. This makes it easy to download and serve models. Here's how to serve `meta-llama/Llama-3.2-3B-Instruct`.
Note this is a safetensors formatted LLM, rather than a GGUF. This model is ~16G. You'll need a Huggingface API Token for most models.

```bash
ilab model download --repository meta-llama/Llama-3.2-3B-Instruct --hf-token XXXxxxxx
ilab model serve --gpus=2 --backend=vllm --model-path=/var/home/cloud-user/.cache/instructlab/models/meta-llama/Llama-3.2-3B-Instruct 
```


