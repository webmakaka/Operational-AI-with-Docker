# MLflow — experiment tracking and model registry

MLflow answers the question: *which model version is in production, what
data was it trained on, and how does it compare to the three other
versions you tried last Tuesday?*

## Deploy the Tracking server

```bash
kubectl apply -f mlflow.yaml

# Open the UI
kubectl port-forward svc/mlflow 5000:5000 -n ai-app
# Navigate to http://localhost:5000
```

## Log a training run

```bash
# From outside the cluster (via port-forward):
pip install mlflow
python log_example.py

# Or from inside a Pod (use http://mlflow:5000 as the tracking URI):
kubectl run mlflow-client \
  --image=python:3.11-slim \
  --namespace=ai-app \
  --rm -it \
  -- /bin/bash -c "pip install mlflow -q && python /scripts/log_example.py"
```

## Integration with KubeRay and Kubeflow

Any Pod in the `ai-app` namespace — whether a RayJob worker or a
Kubeflow pipeline step — can call `mlflow.log_metric()` and every run
appears in the same MLflow UI, with full parameter and metric history
you can compare across runs.

## When to use MLflow

Reach for MLflow the moment you start running more than one training
experiment. The Model Registry is particularly valuable for gating
production promotions: a model must reach Staging before it can be
promoted to Production, and every promotion is tracked with who did it
and when.
