# Tempo container for tracing backend

All commands are assumed to run as root user and haven't been tested as non-root.

## Run Tempo as a Systemd Service

```bash
# Edit ./tempo.yaml to match requirements
mkdir /etc/tempo && cp ./tempo.yaml /etc/tempo/tempo.yaml
cp ./tempo.service /etc/systemd/system/tempo.service
systemctl daemon-reload
systemctl start tempo

# To start tempo container when system boots
systemctl enable tempo

# Tempo container should now be running
podman logs -f tempo
```

## Run Tempo with Podman

Tempo can be started from [this podman command](./podman-cmd).

```bash
./podman-cmd 

# Tempo container will run in the background, to view logs run
podman logs tempo

# Tempo data will be in tempo-data podman volume
podman volume inspect tempo-data
```

## Add Tempo exporter to OpenTelemetry-Collector

If you don't have an opentelemetry-collector service running, see the [telemetry-collector-service example](../telemetry-collection/README.md).
Modify the opentelemetry-collector configuration file to add a tempo exporter. 
View the [example exporter snippet](./otel-collector-exporter.yaml).
Then, restart the opentelemetry-collector container or telemetry-collector systemd service.

## View traces in Grafana

From the Grafana UI, add a new Tempo Datasource.
Configure the Tempo endpoint `http://127.0.0.1:3200`
Traces should be visible from `Explore` by choosing `Tempo` Datasource. 
