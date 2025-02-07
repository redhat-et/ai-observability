## Performance Co-Pilot (PCP) in RHEL AI

PCP is a suite of tools, services, and libraries for monitoring, visualizing, storing, and analyzing system-level performance measurements.
PCP is the standard monitoring tool for RHEL systems, and as such is included in RHEL AI.

The easiest way to get up and running with PCP is with the `pcp-zeroconf` package. To visualize system metrics and workload metrics,
install `grafana` and `grafana-pcp` along with a `Valkey` in-memory, NoSQL key/value database. Also, `pcp-pmda-openmetrics` allows for
PCP to ingest prometheus and/or OTLP workload metrics.

### Install PCP-zeroconf and ensure PCP services are started

```bash
sudo rpm-ostree install pcp-zeroconf pcp-pmda-openmetrics
sudo systemctl reboot

# after reboot
cd /var/lib/pcp/pmdas/openmetrics
./Install
```

Upon a reboot, PCP services `pmcd`, `pmlogger`, and `pmproxy` should be running.

**NOTE** The pmcd, pmlogger, and pmproxy services and rpms are installed in the RHEL AI base image. It is possible to start these 3 systemd service
to avoid installing `pcp-zeroconf`.  In future releases, `pcp-zeroconf` package will be included in the base OS image. It simplifies the
management of the PCP services and ensures they remain connected. Most likely, `pcp-pmda-openmetrics` will also be included in the base OS image. 

### Start Valkey and Grafana

All that's required to view system metrics in RHEL AI is to run `Valkey` and `Grafana`.
To keep the number of packages required to install minimal, Valkey and Grafana run with podman managed by systemd.
In future releases of RHEL AI, Valkey & Grafana rpms could be added to the base OS image. This would avoid needing place the below systemd unit files. 
View the [valkey unit file](./valkey-service/valkey.service) and the [grafana unit file](./grafana-service/grafana.service)
to view the podman commands. Enabling these systemd services ensures that valkey and grafana containers will start when the system boots up.

The `grafana-pcp` grafana plugin installed above includes PCP Datasources and many preconfigured Grafana Dashboards for visualizing data.

#### Start valkey and restart pmproxy service

Valkey will be started as a user-level systemd service.

```bash
mkdir -p ~/.config/systemd/user && cp ./valkey-service/valkey.service ~/.config/systemd/user/valkey.service
systemctl --user daemon-reload
systemctl --enable valkey.service --now

# check that valkey is up and running and ready to connect with pmproxy
systemctl --user status valkey
podman logs valkey
podman volume inspect valkey-data #<-podman volume with valkey data will persist service restarts

# restart pmproxy to connect to valkey
sudo systemctl restart pmproxy

# check that pmproxy and valkey are connected by receiving a non-empty response to the below command.
sudo pmseries -p 6379 disk.dev.read
61261618638aa1189c1cc2220815b0cec8c66414
```

#### Start Grafana 

Grafana will be started as a user-level systemd service.

```bash
cp ./grafana-service/grafana.service ~/.config/systemd/user/grafana.service
systemctl --user daemon-reload
systemctl --user --enable grafana.service --now

# check that grafana is running
systemctl --user status grafana
podman logs grafana
podman volume inspect grafana-data #<-podman volume with grafana-data will persist service restarts
```

### Configure PCP Dashboards in Grafana

Grafana is accessible at `http://ip-addr-local-host:3000`. From the Grafana UI, enable the PCP plugin.
After the PCP plugin is added, use the `Add new Datasource` button to search for `PCP-*` Datasources.
Add the PCP-Valkey Datasourse and and from there, import the listed Valkey
dashboards. Similarly, the PCP-Vector Datasource can be added and its dashboards imported.

## AI Workload monitoring

PCP is designed to monitor the host system performance metrics. The PMDA `openmetrics` plugin installed above allows PCP to ingest workload
(prometheus and/or OTLP) metrics as well. The `Red Hat Build of OpenTelemetry Collector` can also be deployed to collect metrics, logs, and traces from all
workloads. The Grafana server installed above can be used to visualize all telemetry locally. However, depending on your requirements, exporting data
to an external observability stack such as on OpenShift, or to an observability vendor such as Dynatrace, is also an option.
Here the various choices for building out a more complete observability solution are outlined.

### Add Workload Metrics to PCP, Visualize in Local Grafana

TODO

### OpenTelemetry Collector to unify all local workloads metrics into a single prometheus stream to be injested by PCP

TODO

### OpenTelemetry Collector to unify collection of all telemetry (metrics, logs, and traces) and export to external observability stack

TODO

#### Export Telemetry to OpenShift

TODO

#### Export Telemetry to Dynatrace (or any other observability vendor)

TODO

