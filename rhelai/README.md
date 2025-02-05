## Performance Co-Pilot in RHEL AI

The easiest way to get up and running with PCP is with the `pcp-zeroconf` package. To visualize system metrics and workload metrics,
install `grafana` and `grafana-pcp` along with a `Valkey` in-memory, NoSQL key/value database.

### Install PCP-zeroconf and ensure PCP services are started

```bash
sudo rpm-ostree install pcp-zeroconf
sudo systemctl reboot
```

Upon a reboot, PCP services `pmcd`, `pmlogger`, and `pmproxy` should be running.

**NOTE** The pmcd, pmlogger, and pmproxy services and rpms are installed in the RHEL AI base image. It is possible to start these 3 systemd service
to avoid installing `pcp-zeroconf`.  In future releases, `pcp-zeroconf` package will be included in the base OS image. It simplifies the
management of the PCP services and ensures they remain connected. 

### Start Valkey and Grafana

All that's required to view system metrics in Grafana is to run `valkey` and `grafana`. The `grafana-pcp` grafana plugin includes
PCP Datasources and many preconfigured dashboards for visualizing data. In this setup, these containers will be managed by user-level
systemd services. View the [valkey unit file](./valkey-service/valkey.service)
and the [grafana unit file](./grafana-service/grafana.service) to view the podman commands. Enabling these systemd services
ensures that valkey and grafana containers will start when the system boots up.

#### Start valkey and restart pmproxy service

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
