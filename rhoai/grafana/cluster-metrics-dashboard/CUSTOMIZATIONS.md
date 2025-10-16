# Customizations Applied to kevchu3's Cluster Metrics Dashboard

This document describes the modifications made to the original kevchu3 OpenShift Grafana dashboard to make it compatible with our cluster setup.

## Source Dashboard
- **Upstream Repository**: https://github.com/kevchu3/openshift4-grafana
- **Current Version**: OCP 4.18 (cluster_metrics.ocp418.json)
- **Last Updated**: 2025-10-16

## Why Customizations Are Needed

The upstream dashboard hardcodes the Prometheus datasource UID as `"Prometheus"`, which may not match the datasource name in your Grafana instance. These customizations make the dashboard portable across different Grafana installations by using a template variable for the datasource.

## Changes Applied

### 1. Added Datasource Template Variable
**Purpose**: Allow users to select the Prometheus datasource from a dropdown in Grafana.

**Location**: `templating.list` section

**Change**:
```json
"templating": {
  "list": [
    {
      "name": "datasource",
      "type": "datasource",
      "query": "prometheus",
      "current": {
        "selected": true,
        "text": "prometheus",
        "value": "prometheus"
      },
      "hide": 0,
      "label": "Datasource",
      "regex": "",
      "refresh": 1,
      "sort": 0
    }
  ]
}
```

### 2. Changed All Datasource UIDs to Use Template Variable
**Purpose**: Reference the datasource template variable instead of hardcoding.

**Location**: All panels and targets throughout the dashboard

**Before**:
```json
"datasource": {
  "type": "prometheus",
  "uid": "Prometheus"
}
```

**After**:
```json
"datasource": {
  "type": "prometheus",
  "uid": "${datasource}"
}
```

### 3. Simplified Annotations Datasource
**Purpose**: Use Grafana's built-in annotation datasource.

**Location**: `annotations.list[0].datasource`

**Before**:
```json
"datasource": {
  "type": "datasource",
  "uid": "grafana"
}
```

**After**:
```json
"datasource": "-- Grafana --"
```

### 4. Simplified Row Panel Datasources
**Purpose**: Use simpler string format for row panels that don't execute queries.

**Location**: Row panels (Cluster Health, Cluster Metrics, Cluster Capacity)

**Before**:
```json
"datasource": {
  "type": "prometheus",
  "uid": "Prometheus"
}
```

**After**:
```json
"datasource": "prometheus"
```

## How to Update to a Newer Version

When a new version is available from kevchu3's repository:

### Manual Method

1. Download the latest version:
   ```bash
   curl -O https://raw.githubusercontent.com/kevchu3/openshift4-grafana/refs/heads/master/dashboards/json_raw/cluster_metrics.ocp4XX.json
   ```

2. Apply the customizations using the Python script below

3. Copy to the cluster-metrics-dashboard directory

### Automated Method

Use this Python script to apply all customizations automatically:

```python
import json

# Read the upstream dashboard
with open('cluster_metrics.ocp4XX.json', 'r') as f:
    dashboard = json.load(f)

# 1. Update annotations datasource
if 'annotations' in dashboard and 'list' in dashboard['annotations']:
    for annotation in dashboard['annotations']['list']:
        if annotation.get('builtIn') == 1:
            annotation['datasource'] = '-- Grafana --'

# 2. Add datasource template variable
dashboard['templating'] = {
    "list": [
        {
            "name": "datasource",
            "type": "datasource",
            "query": "prometheus",
            "current": {
                "selected": True,
                "text": "prometheus",
                "value": "prometheus"
            },
            "hide": 0,
            "label": "Datasource",
            "regex": "",
            "refresh": 1,
            "sort": 0
        }
    ]
}

# 3. Update all datasource UIDs recursively
def update_datasources(obj):
    if isinstance(obj, dict):
        # Check if this is a datasource object
        if 'type' in obj and 'uid' in obj and obj['type'] == 'prometheus':
            if obj['uid'] in ['Prometheus', 'prometheus']:
                obj['uid'] = '${datasource}'

        # Special case for row panels - use simple string format
        if obj.get('type') == 'row' and 'datasource' in obj:
            if isinstance(obj['datasource'], dict):
                obj['datasource'] = 'prometheus'

        # Recurse into all dict values
        for key, value in obj.items():
            update_datasources(value)
    elif isinstance(obj, list):
        # Recurse into all list items
        for item in obj:
            update_datasources(item)

# Apply the transformation
update_datasources(dashboard)

# Write the updated dashboard
with open('cluster_metrics.ocp.json', 'w') as f:
    json.dump(dashboard, f, indent=2)

print("Dashboard updated successfully")
```
