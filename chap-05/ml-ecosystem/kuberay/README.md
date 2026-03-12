# KubeRay — distributed ML training and serving

KubeRay extends Kubernetes with three custom resource types:
- **RayCluster** — provisions a pool of Ray workers
- **RayJob** — runs a training job, then cleans up all Pods automatically
- **RayService** — deploys a model with Ray Serve behind a stable endpoint

## Install the KubeRay operator

```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm install kuberay-operator kuberay/kuberay-operator \
  --namespace kuberay-system \
  --create-namespace

# Verify
kubectl get pods -n kuberay-system
```

## Run the hello-ray job

```bash
kubectl apply -f hello-ray.yaml
kubectl get rayjob hello-ray -n ai-app --watch
```

Expected lifecycle: `PENDING` → `RUNNING` → `COMPLETE`

When the job completes, KubeRay cleans up all Pods automatically.

## When to use KubeRay

Reach for KubeRay when you need:
- Fine-tuning a model on your own dataset across multiple GPUs
- Distributed hyperparameter search
- Ray Serve for advanced traffic management and A/B testing

For single-model inference (like the chatbot in this chapter), the
standard Deployment approach is simpler and sufficient.
