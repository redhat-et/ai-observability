# Valkey

All commands are assumed to run as root user and haven't been tested as non-root.

## SELinux pcp_valkey module

To enable the connection between `pmproxy` and `valkey`, an SELinux module must be added.
Check out the [pcp_valkey.te](./pcp_valkey.te) file and then run as the root user:

```bash
checkmodule -M -m -o pcp_valkey.mod pcp_valkey.te
semodule_package -o pcp_valkey.pp -m pcp_valkey.mod
semodule -i pcp_valkey.pp
```

OR, use the [AVC denial log](./avc-denial.txt) to generate the module with `audit2allow` as follows:

```bash
bash-5.1# audit2allow -M pcp_valkey -i avc-denial.txt 
******************** IMPORTANT ***********************
To make this policy package active, execute:

semodule -i pcp_valkey.pp
```

## Run Valkey container as a systemd service

The unit file, [valkey.service](./valkey.service) starts a valkey podman container.

```bash
cp ./valkey.service /etc/systemd/system/valkey.service
systemctl daemon-reload
systemctl start valkey

# To start valkey container when system boots
systemctl enable valkey

# Valkey container should now be running
podman logs -f valkey
```

### Run Valkey with Podman

Valkey can be started from [this podman command](./podman-cmd)

### Valkey data will be in valkey-data podman volume
podman volume inspect valkey-data
```
