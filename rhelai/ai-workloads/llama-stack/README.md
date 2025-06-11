# Run Llama-Stack Server with vLLM (no Ollama)

**Note** vLLM doesn't run on MacOS, this is x86_64 specific

## Start vLLM Server with Llama-3.2-3B-Instruct

Follow [this](../../vllm/README.md) to download `meta-llama/Llama-3.2-3B-Instruct` and serve it with `vLLM`. 
This will enable function and tool-calling.

## Start Llama-stack server

### Run without podman

```bash
git clone git@github.com:meta-llama/llama-stack && cd llama-stack
conda create llamastack && conda activate llamastack

export INFERENCE_PORT=8000
export INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct
export LLAMA_STACK_PORT=8321
export HF_TOKEN=hf_xxxXXXX <-HF token needs to have access to meta-llama/llama-3.2 repo

cd distributions/remote-vllm
conda install pip && pip install llama-stack

# llama stack build generates ./run.yaml
llama stack build --template remote-vllm --image-type conda

# run.yaml configuration pushed to this folder has the telemetry.otel-collector endpoint added, if you use that you don't need to run the build above.
llama stack run ./run.yaml   --port $LLAMA_STACK_PORT   --env INFERENCE_MODEL=$INFERENCE_MODEL   --env VLLM_URL=http://127.0.0.1:$INFERENCE_PORT/v1
```

### Run with podman

```bash
podman run -it -d --name llamastack \
    --network=host \
    -v ./run.yaml:/tmp/run.yaml:Z \
    llamastack/distribution-remote-vllm --yaml-config /tmp/run.yaml --env INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct --env VLLM_URL=http://127.0.0.1:8000/v1

podman logs llamastack # <- add `-f` to follow the logs.
```

Llama-Stack Server should now be running. You can test if it's working by running the following in a new terminal session:

```
llama-stack-client --endpoint http://localhost:8321 inference chat-completion --message "hello, what model are you?"
```

Now you can utilize the Llama-stack server to build and run AI applications.

### Example Applications

Try out these example applications from [redhat-et/agent-frameworks/llamastack/scripts](https://github.com/redhat-et/agent-frameworks/tree/main/prototype/frameworks/llamastack/scripts)
