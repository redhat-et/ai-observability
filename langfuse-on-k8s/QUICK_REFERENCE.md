# Langfuse - Quick Reference

## Deployment

```bash
# Initial deployment
./deploy.sh

# Upgrade to latest version
helm repo update
helm upgrade langfuse langfuse/langfuse --namespace langfuse --reuse-values

# Check deployment status
oc get pods -n langfuse
```

## Access

```bash
# Get Langfuse URL
oc get route langfuse -n langfuse -o jsonpath='{.spec.host}'

# Access from within cluster
# http://langfuse-web.langfuse.svc.cluster.local:3000
```

## Monitoring

```bash
# View all pods
oc get pods -n langfuse

# Follow web app logs
oc logs -n langfuse -l app.kubernetes.io/name=langfuse -c langfuse-web -f

# Follow worker logs
oc logs -n langfuse -l app.kubernetes.io/component=worker -f

# Check resource usage
oc adm top pods -n langfuse
```

## Database Operations

```bash
# PostgreSQL shell
oc exec -it langfuse-postgresql-0 -n langfuse -- psql -U postgres

# ClickHouse shell
oc exec -it langfuse-clickhouse-0 -n langfuse -- clickhouse-client

# Check database connections
oc exec -it langfuse-postgresql-0 -n langfuse -- psql -U postgres -c 'SELECT count(*) FROM pg_stat_activity;'
```

## Configuration

```bash
# View Helm values
helm get values langfuse -n langfuse

# Update configuration
helm upgrade langfuse langfuse/langfuse \
  --namespace langfuse \
  --reuse-values \
  --set <key>=<value>

# View all environment variables
oc set env deployment/langfuse-web -n langfuse --list
```

## Cleanup

```bash
# Scale down (keep data)
oc scale deployment --all --replicas=0 -n langfuse
oc scale statefulset --all --replicas=0 -n langfuse

# Delete everything (⚠️ PERMANENT)
oc delete namespace langfuse
```

## Environment Variables for Applications

**Python (Langfuse SDK)**:
```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://langfuse-<cluster-domain>"
# Or for internal cluster access:
# export LANGFUSE_HOST="http://langfuse-web.langfuse.svc.cluster.local:3000"
```

**OpenTelemetry**:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://langfuse-<cluster-domain>/api/public/otel/v1/traces"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic $(echo -n 'pk-lf-...:sk-lf-...' | base64)"
```

## Useful Links

- Langfuse Docs: https://langfuse.com/docs
- Helm Chart: https://github.com/langfuse/langfuse-k8s
- OpenShift Docs: https://docs.openshift.com
- Discord Community: https://langfuse.com/discord
