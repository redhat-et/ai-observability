## Collect basic usage stats

The example [deployment](./deployment-with-usage-stats.yaml) includes an init container to collect useful system information.

## Pipeline run

After a successful run, this file structure will be in the Pipeline PVC:

```
/workspace/output/
├── usage_stats/
│   ├── pod-1.json
│   ├── pod-2.json
├── metrics/
│   ├── gpu_hours.json
│   ├── prompt_rate.json
│   ├── generation_rate.json
├── metrics.csv  <- will load this in Jupyter
```
