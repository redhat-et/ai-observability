## Run Llama-Stack Server with vLLM (no Ollama)

**Note** vLLM doesn't run on MacOS, this is x86_64 specific

### Start vLLM Server with Llama-3.1-8B-Instruct

Follow [this](../../vllm/README.md) to download `meta-llama/Llama-3.1-8B-Instruct` and serve it with `vLLM`. 

### Start Llama-stack server

**TODO** Containerize this - the remote-vllm llamastack image is broken AFAICT

```bash
git clone git@github.com:meta-llama/llama-stack && cd llama-stack
conda create llamastack && conda activate llamastack

export INFERENCE_PORT=8000
export INFERENCE_MODEL=meta-llama/Llama-3.1-8B-Instruct
export LLAMA_STACK_PORT=5001
export HF_TOKEN=hf_xxxXXXX <-HF token needs to have access to meta-llama/llama-3.1 repo

cd distributions/remote-vllm
conda install pip && pip install llama-stack

# llama stack build generates ./run.yaml
llama stack build --template remote-vllm --image-type conda

# run.yaml configuration pushed to this folder has the telemetry.otel-collector endpoint added, if you use that you don't need to run the build above.
llama stack run ./run.yaml   --port $LLAMA_STACK_PORT   --env INFERENCE_MODEL=$INFERENCE_MODEL   --env VLLM_URL=http://127.0.0.1:$INFERENCE_PORT/v1
```

Llama-Stack Server should now be running. You can test if it's working by running the following in a new terminal session:

```
llama-stack-client --endpoint http://3.228.254.110:5001 inference chat-completion --message "hello, what model are you?"
```

Now you can utilize the Llama-stack server to build and run AI applications.
