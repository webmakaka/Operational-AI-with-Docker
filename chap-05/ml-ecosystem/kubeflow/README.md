# Kubeflow Pipelines — ML lifecycle automation

Kubeflow Pipelines automates the full model lifecycle: ingest,
preprocess, train, evaluate, register, deploy — each step as its own
container in Kubernetes, with inputs/outputs tracked automatically.

## Install Kubeflow Pipelines (standalone)

```bash
export PIPELINE_VERSION=2.2.0

kubectl apply -k \
  "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"

kubectl wait --for condition=established \
  --timeout=60s crd/applications.app.k8s.io

kubectl apply -k \
  "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
```

## Open the UI

```bash
# Wait for the UI pod to be ready (2-3 minutes)
kubectl wait pods -l app=ml-pipeline-ui \
  -n kubeflow --for=condition=Ready --timeout=180s

kubectl port-forward svc/ml-pipeline-ui 8080:80 -n kubeflow
# Navigate to http://localhost:8080
```

## Compile and run the example pipeline

```bash
pip install kfp
python pipeline.py        # produces pipeline.yaml
```

Upload `pipeline.yaml` through the Kubeflow UI, create an experiment,
and trigger a run. Both steps execute as individual Pods in the
`kubeflow` namespace, with inputs and outputs tracked in the run history.

## When to use Kubeflow

Reach for Kubeflow when you want to automate the full training lifecycle
with reproducible, tracked experiments. For a simple inference service,
it's overkill. For a production model that retrains weekly on new data,
it's exactly the right tool.
