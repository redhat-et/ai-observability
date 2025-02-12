# Valkey

All commands are assumed to run as root user and haven't been tested as non-root.

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
