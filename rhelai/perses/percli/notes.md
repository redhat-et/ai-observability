podman cp perses:/bin/percli /tmp/percli
chmod +x /tmp/percli
chown cloud-user:cloud-user /tmp/percli
exit
mv /tmp/percli ~/.local/bin/
which percli
percli login http://localhost:8080
percli apply -f project.json
percli apply -f prom-global-datasource.yaml
percli project rhelai

TODO:
* create Global Tempo datasource

percli apply -f dashboards/gpu-usage.json
percli apply -f dashboards/vllm-performance-overview.json
percli apply -f dashboards/pcp-host-overview.json

