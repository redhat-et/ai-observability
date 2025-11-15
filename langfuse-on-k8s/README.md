# Langfuse on Kubernetes

Deployment guide for Langfuse LLM observability platform on Kubernetes and OpenShift clusters.

## What is Langfuse?

[Langfuse](https://langfuse.com) is an open-source LLM engineering platform that provides:

- **Trace Analysis**: Detailed trace visualization for LLM applications
- **Prompt Management**: Version control and testing for prompts
- **Evaluation**: Automated and manual evaluation of LLM outputs
- **Metrics & Analytics**: Cost tracking, latency monitoring, quality metrics
- **Datasets**: Test case management and evaluation datasets
- **OpenTelemetry Support**: Native OTLP endpoint for unified observability

## Prerequisites

Before deploying Langfuse, ensure you have:

1. **Kubernetes or OpenShift CLI** installed
   - **Kubernetes**: `kubectl` - https://kubernetes.io/docs/tasks/tools/
   - **OpenShift**: `oc` - https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html
   - Verify: `kubectl version` or `oc version`

2. **Helm 3.x** installed
   - Install: https://helm.sh/docs/intro/install/
   - Verify: `helm version`

3. **Access to cluster** with admin or namespace admin privileges
   - **Kubernetes**: Configure kubectl context
   - **OpenShift**: Login with `oc login <your-cluster-url>`
   - Verify: `kubectl cluster-info` or `oc whoami`

4. **Sufficient cluster resources**:
   - Minimum: 4 CPUs, 8GB RAM
   - Recommended: 8 CPUs, 16GB RAM for production

## Quick Start

### 1. Deploy Langfuse

```bash
# Clone or download this directory
cd langfuse-on-k8s

# Run the deployment script (auto-detects platform)
./deploy.sh

# Or force a specific platform:
./deploy.sh --openshift   # Force OpenShift mode (use oc, create Route)
./deploy.sh --kubernetes  # Force Kubernetes mode (use kubectl, create Ingress)
```

**Platform Auto-Detection:**
- Automatically detects OpenShift (checks for `route.openshift.io` API group)
- Falls back to Kubernetes if OpenShift features not available
- Uses `oc` on OpenShift, `kubectl` on Kubernetes
- Creates Route (OpenShift) or Ingress (Kubernetes) automatically

**The script will:**
- ✅ Detect platform (or use --openshift/--kubernetes flag)
- ✅ Check prerequisites (Helm, kubectl/oc CLI)
- ✅ Prompt for credential preferences (test vs. production)
- ✅ Add Langfuse Helm repository
- ✅ Create `langfuse` namespace
- ✅ Deploy Langfuse with PostgreSQL, ClickHouse, Redis, and MinIO
- ✅ Apply S3 credential fixes
- ✅ Create Route (OpenShift) or Ingress (Kubernetes) for external access
- ✅ Save credentials to `langfuse-credentials.env`

**Expected deployment time**: 5-10 minutes

### Platform-Specific Differences

| Feature | Kubernetes | OpenShift |
|---------|-----------|-----------|
| **CLI Tool** | `kubectl` | `oc` (backwards compatible with kubectl) |
| **External Access** | Ingress (requires Ingress controller) | Route (built-in, TLS automatic) |
| **Default Host** | `langfuse.local` (needs DNS/hosts file) | Auto-generated route (e.g., `langfuse-langfuse.apps.<cluster>`) |
| **TLS** | Requires cert-manager or manual cert | Automatic edge termination |

**Kubernetes Notes:**
- Requires an Ingress controller (nginx, traefik, etc.)
- Default Ingress uses `langfuse.local` - update `/etc/hosts` or configure DNS
- May need to manually configure TLS certificates

**OpenShift Notes:**
- Routes are built-in, no additional controller needed
- Automatic TLS edge termination
- Hostname auto-generated based on cluster domain

### 2. Access Langfuse UI

After deployment completes, you'll see output like:

**OpenShift:**
```
✅ Langfuse deployment complete!

Access Langfuse UI:
   External URL: https://langfuse-langfuse.apps.<your-cluster>
```

**Kubernetes:**
```
✅ Langfuse deployment complete!

Access Langfuse UI:
   External URL: https://langfuse.local

⚠️  Note: For local access, add to /etc/hosts:
   127.0.0.1 langfuse.local
```

Open the URL in your browser to access Langfuse.

### 3. Initial Setup

1. **Create an account**
   - Sign up with email/password or SSO
   - Verify email if required

2. **Create an organization**
   - Choose organization name
   - Configure settings

3. **Create a project**
   - Project name (e.g., "production", "staging", "my-app")
   - Projects provide isolation for traces and metrics

4. **Generate API keys**
   - Navigate to: Settings → API Keys → Create new key pair
   - Save your keys securely:
     - `LANGFUSE_PUBLIC_KEY`: `pk-lf-...`
     - `LANGFUSE_SECRET_KEY`: `sk-lf-...` (⚠️ shown only once!)

## Configuration Options

### Production vs. Test Credentials

The deployment script offers two credential modes:

**Test Mode** (default):
- Simple passwords for quick testing
- PostgreSQL: `postgres123`
- ClickHouse: `clickhouse123`
- Redis: `redis123`
- ⚠️ **NOT secure for production**

**Production Mode**:
- Cryptographically secure random credentials
- Auto-generated using OpenSSL
- Saved to `langfuse-credentials.env`
- File permissions automatically set to `600`

### Resource Limits

Default resource allocations (suitable for small-medium workloads):

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Langfuse Web | 500m | 1000m | 1Gi | 2Gi |
| ClickHouse | 500m | 1 | 512Mi | 1Gi |
| PostgreSQL | (default) | (default) | (default) | (default) |
| Redis | (default) | (default) | (default) | (default) |
| Zookeeper | 250m | 500m | 256Mi | 512Mi |

To customize resources, edit `deploy.sh` and modify the `--set` parameters.

### High Availability

The default deployment uses single replicas for simplicity. For production HA:

1. **Increase replicas**:
   ```bash
   --set clickhouse.replicaCount=3 \
   --set zookeeper.replicas=3
   ```

2. **Enable anti-affinity** (requires multi-node cluster):
   ```bash
   --set clickhouse.podAntiAffinityPreset=hard \
   --set postgresql.primary.podAntiAffinityPreset=hard \
   --set redis.master.podAntiAffinityPreset=hard
   ```

3. **Use external databases** (recommended for production):
   - Managed PostgreSQL (e.g., AWS RDS, Azure Database)
   - Managed Redis (e.g., ElastiCache, Azure Cache)
   - See: https://langfuse.com/docs/deployment/self-host

## Using Langfuse

### Integrating Your Application

Once deployed, configure your LLM application to send traces to Langfuse:

**Python (Langfuse SDK)**:
```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="https://langfuse-langfuse.apps.<your-cluster>"
)

# For internal cluster access (faster):
# host="http://langfuse-web.langfuse.svc.cluster.local:3000"
```

**OpenTelemetry Traces** (any language):
```bash
# Environment variables
export OTEL_EXPORTER_OTLP_ENDPOINT="https://langfuse-langfuse.apps.<your-cluster>/api/public/otel/v1/traces"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic $(echo -n 'pk-lf-...:sk-lf-...' | base64)"
```

See: https://langfuse.com/docs/integrations for framework-specific guides.

### Accessing from Within OpenShift

For applications running inside the same OpenShift cluster, use the internal service URL for better performance:

```
http://langfuse-web.langfuse.svc.cluster.local:3000
```

No TLS required for internal cluster communication.

## Monitoring and Operations

### Check Deployment Status

```bash
# All pods running and ready
oc get pods -n langfuse

# Services and endpoints
oc get svc -n langfuse

# Route status and URL
oc get route -n langfuse

# PersistentVolumeClaims (data storage)
oc get pvc -n langfuse
```

### View Logs

```bash
# Langfuse web application logs
oc logs -n langfuse -l app.kubernetes.io/name=langfuse -c langfuse-web --tail=100 -f

# Langfuse worker logs (background jobs)
oc logs -n langfuse -l app.kubernetes.io/component=worker --tail=100 -f

# PostgreSQL logs
oc logs -n langfuse -l app.kubernetes.io/name=postgresql --tail=100

# ClickHouse logs
oc logs -n langfuse -l app.kubernetes.io/name=clickhouse --tail=100
```

## Uninstalling

**⚠️ WARNING: This permanently deletes all Langfuse data!**

```bash
# Delete everything (namespace, data, routes)
oc delete namespace langfuse

# Or remove Helm release only (keeps PVCs)
helm uninstall langfuse --namespace langfuse
```

To keep data for future reinstallation, do NOT delete the namespace. Instead:

```bash
# Scale down deployments
oc scale deployment --all --replicas=0 -n langfuse
oc scale statefulset --all --replicas=0 -n langfuse
```

## Additional Resources

- **Langfuse Documentation**: https://langfuse.com/docs
- **Langfuse GitHub**: https://github.com/langfuse/langfuse
- **Helm Chart**: https://github.com/langfuse/langfuse-k8s
- **OpenShift Documentation**: https://docs.openshift.com
- **Community Support**: https://langfuse.com/discord

## License

Langfuse is licensed under the MIT License. See: https://github.com/langfuse/langfuse/blob/main/LICENSE
