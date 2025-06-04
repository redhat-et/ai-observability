## llm-d 

`llm-d` is a Kubernetes-native distributed inference serving stack. More information can be found in the [llm-d documentation](https://llm-d.ai/)

To try out `llm-d` you can use the quickstart. With only a single GPU, there are examples to run `llm-d` that are essentially an easy way to spin up an instance of `vLLM` with little effort. 

* [llm-d Quickstart](https://github.com/llm-d/llm-d-deployer/tree/main/quickstart)
* [llm-d developer MiniKube quickstart](https://github.com/llm-d/llm-d-deployer/blob/main/quickstart/README-minikube.md)
    * [Single GPU](https://github.com/llm-d/llm-d-deployer/blob/main/quickstart/README-minikube.md#run-on-a-single-gpu) (no Prefill, Decode, KVCache, or smart routing features, essentially just vanilla vLLM)
