## Performance Co-Pilot in RHEL AI

The easiest way to get up and running with PCP is with the `pcp-zeroconf` package. To visualize system metrics and workload metrics,
install `grafana` and `grafana-pcp` along with a `Valkey` in-memory, NoSQL key/value database.

### Installation of PCP-zeroconf and grafana

```bash
sudo rpm-ostree install pcp-zeroconf
sudo systemctl reboot
```
**TODO** maybe to start with we enable the pmcd, pmlogger, and pmproxy services so we don't have to install pcp-zeroconf? Then, work with RHELAI to
include zeroconf in the base image.

## Start Performance Co-Pilot (PCP) Services

Upon a reboot, PCP services should be running.
All that's required to view system metrics in Grafana is to run `grafana` and `valkey` datastore  with the PCP `grafana-pcp` plugin.

```bash

# start Valkey
./pcp/podman-cmd-valkey
podman logs valkey

# check that Valkey server is running and connected to pmproxy
sudo pmseries -p 6379 disk.dev.read
61261618638aa1189c1cc2220815b0cec8c66414
```

## Configure PCP Dashboards in Grafana

Now the fun part: Enable the PCP plugin in grafana, at `http://ip-addr-local-host:3000`, then add PCP-Valkey Datastore and import the listed Valkey
dashboards. You can also add the PCP-Vector Datastore to import its dashboards.

## InstructLab in RHEL AI to serve LLMs

The instructLab CLI is included in RHEL AI. This makes it easy to download and serve models. Here's how to serve `meta-llama/Llama-3.1-8B-Instruct`.
Note this is a safetensors formatted LLM, rather than a GGUF.

```bash
ilab model download --repository meta-llama/Llama-3.1-8B-Instruct --hf-token XXXxxxxx
ilab model serve --gpus=2 --backend=vllm --model-path=/var/home/cloud-user/.cache/instructlab/models/meta-llama/Llama-3.1-8B-Instruct 
```

## View vLLM metrics (TODO)
