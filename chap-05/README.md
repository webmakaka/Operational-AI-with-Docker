# Chapter 5: Running ML Container Models on Kubernetes

Code examples for Chapter 5 

## Structure

```
chap-05/
├── manifests/              # Core chatbot stack (apply all at once)
│   ├── storage.yaml        # PersistentVolumeClaim for model files
│   ├── config.yaml         # ConfigMap + Secret
│   ├── dmr-deployment.yaml # Docker Model Runner Deployment + Service
│   ├── backend-deployment.yaml   # Go backend Deployment + Service
│   └── frontend-deployment.yaml  # React frontend Deployment + Service
├── scaling/
│   └── hpa.yaml            # Horizontal Pod Autoscaler for go-backend
└── ml-ecosystem/
    ├── kuberay/
    │   └── hello-ray.yaml  # Minimal RayJob to verify KubeRay
    ├── kubeflow/
    │   └── pipeline.py     # Minimal two-step Kubeflow Pipeline
    ├── kserve/
    │   └── sklearn-iris.yaml  # InferenceService example
    └── mlflow/
        ├── mlflow.yaml     # MLflow Tracking server Deployment + Service
        └── log_example.py  # Python snippet showing mlflow.log_*
```

## Prerequisites

- Docker Desktop 4.38 or later
- Kubernetes enabled via Settings → Kubernetes → kind (2 worker nodes)
- `kubectl` available (`kubectl version --client`)

## Quick start

```bash
# 1. Create the namespace
kubectl create namespace ai-app

# 2. Deploy everything
kubectl apply -f manifests/

# 3. Watch deployments become ready (DMR takes ~60-90s)
kubectl get deployments -n ai-app --watch

# 4. Access the chatbot
kubectl port-forward svc/react-frontend 3000:3000 -n ai-app
# Open http://localhost:3000

# 5. Clean up when done
kubectl delete namespace ai-app
```
