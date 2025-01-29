### Download a model to serve with vLLM

I used ramalama because it's really easy. I chose a model that I know vLLM supports in GGUF format.
vLLM is designed to work with safetensors model format and has limited support for GGUF formatted models.

```bash
git clone https://github.com/containers/ramalama.git
cd ramalama
python -m venv venv
source venv/bin/activate
pip install ramalama
cp venv/bin/ramalama ~/.local/bin/.
deactivate
which ramalama # ensure it's there
ramalama pull huggingface://bartowski/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf
```

You should now have this on your filesystem:

```bash
$ ls -al ~/.local/share/ramalama/models/huggingface/bartowski/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q5_K_M.gguf
```

You can serve this model with vLLM
