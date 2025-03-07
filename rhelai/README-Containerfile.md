## Build RHELAI Containerfile with PCP Nvidia PMDA

**This is only necessary until these images land in the released version of rhelai**


To install the pcp-pmda-nvidia-gpu, you'll need to add the public nvidia repo file. 
You need this repo to install `nvidia-driver-devel` package that provides a symlink
`libnvidia-ml.so -> /usr/lib64/libnvidia-ml.so.1` required for the plugin to properly run.


Place `cuda-rhel9.repo` and `Containerfile` in the same directory on your running rhelai system

```bash
# cat cuda-rhel9.repo

[cuda-rhel9]
name=CUDA RHEL 9
baseurl=https://developer.download.nvidia.com/compute/cuda/repos/rhel9/$basearch
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA-CUDA-9

```

Now build a new Containerfile from the existing one. You can find the existing image by running

```bash
rpm-ostree status
```

```bash
# cat Containerfile

FROM registry.redhat.io/rhelai/bootc-rhel9:version #<-update this to match your OS image

COPY cuda-rhel9.repo /etc/yum.repos.d/cuda-rhel9.repo
RUN dnf install -y --nogpgcheck pcp-zeroconf pcp-pmda-nvidia-gpu nvidia-driver-devel
```

Now build the image and switch the system over

```bash
sudo su
podman build -t rhelai:new .

# upon successful build
bootc switch --transport containers-storage rhelai:new
reboot
```

You should now have PCP started with openmetrics and nvidia PMDAs


Add [redis service](./redis-service/redis.service) and [grafana-pcp service](./grafana-service/grafana.service)
to visualize the PCP metrics with the Performance Co-Pilot Datasource. 
