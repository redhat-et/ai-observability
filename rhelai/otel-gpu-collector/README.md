## Opentelemetry Collector and OpenLit GPU Collector 

* Update the [otel-config.yaml](./otel-config.yaml) if necessary. If you have `vLLM` running you can uncomment the collection of
vLLM metrics. You may not need to update anything to just get up and running. You'll see the metrics & traces in the otel-collector logs.

* Update the [otel-gpu-collector.service](./otel-gpu-collector.service). You need to provide the `/PATH/TO/` in `#L33`. 

```bash
cp ./otel-gpu-collector.service /etc/systemd/system/otel-gpu-collector.service
systemctl daemon-reload
systemctl start otel-gpu-collector


bash-5.1# podman ps -a
CONTAINER ID  IMAGE                                      COMMAND               CREATED         STATUS         PORTS                   NAMES
92c05f3dea3b  ghcr.io/openlit/otel-gpu-collector:latest  python collector....  37 minutes ago  Up 37 minutes                          gpu-collector
fc9425a642b8  quay.io/sallyom/rh-otel-collector:latest   --config /etc/ote...  37 minutes ago  Up 37 minutes                          otelcol-host

# To stop containers, use
systemctl stop otel-gpu-collector
```

You should see the GPU metrics with

```bash
curl http://localhost:8888/metrics | grep gpu
```

Or, you can export to grafana, prometheus.
